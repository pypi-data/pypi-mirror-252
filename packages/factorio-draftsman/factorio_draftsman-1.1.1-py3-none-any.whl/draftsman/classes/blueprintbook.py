# blueprintbook.py
# -*- encoding: utf-8 -*-

"""
.. code-block:: python

    {
        "blueprint_book": {
            "item": "blueprint-book", # The associated item with this structure
            "label": str, # A user given name for this blueprint book planner
            "label_color": { # The overall color of the label
                "r": float[0.0, 1.0] or int[0, 255], # red
                "g": float[0.0, 1.0] or int[0, 255], # green
                "b": float[0.0, 1.0] or int[0, 255], # blue
                "a": float[0.0, 1.0] or int[0, 255]  # alpha (optional)
            }
            "icons": [ # A set of signals to act as visual identification
                {
                    "signal": {"name": str, "type": str}, # Name and type of signal
                    "index": int, # In range [1, 4], starting top-left and moving across
                },
                ... # Up to 4 icons total
            ],
            "description": str, # A user given description for this blueprint book
            "version": int, # The encoded version of Factorio this planner was created 
                            # with/designed for (64 bits)
            "active_index": int, # The currently selected blueprint in "blueprints"
            "blueprints": [ # A list of all Blueprintable objects this book contains
                {
                    "item": "blueprint",
                    ... # Any associated Blueprint key/values
                }, # or
                {
                    "item": "deconstruction-planner",
                    ... # Any associated DeconstructionPlanner key/values
                }, # or
                {
                    "item": "upgrade-planner",
                    ... # Any associated UpgradePlanner key/values
                }, # or
                {
                    "item": "blueprint-book",
                    ... # Any above key/values
                }
            ]
        }
    }
"""

from __future__ import unicode_literals

from draftsman._factorio_version import __factorio_version_info__
from draftsman.classes.blueprint import Blueprint
from draftsman.classes.blueprintable import Blueprintable
from draftsman.classes.deconstruction_planner import DeconstructionPlanner
from draftsman.classes.upgrade_planner import UpgradePlanner
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman import utils
from draftsman.warning import DraftsmanWarning, IndexWarning

from builtins import int
import copy
from schema import SchemaError
import six
from typing import Union
import warnings

try:  # pragma: no coverage
    from collections.abc import MutableSequence
except ImportError:  # pragma: no coverage
    from collections import MutableSequence


class BlueprintableList(MutableSequence):
    """
    List of Blueprintable instances. "Blueprintable" in this context means
    either a Blueprint object or a BlueprintBook, as BlueprintBook objects
    can exist inside other BlueprintBook instances.
    """

    def __init__(self, initlist=None):
        # type: (list[Blueprint]) -> None
        self.data = []
        if initlist is not None:
            for elem in initlist:
                if isinstance(elem, dict):
                    # TODO: this would be way cleaner, but circuilar imports
                    # self.append(get_blueprintable_from_JSON(elem))
                    # fmt: off
                    if "blueprint" in elem:
                        self.append(Blueprint(elem))
                    elif "deconstruction_planner" in elem:
                        self.append(DeconstructionPlanner(elem))
                    elif "upgrade_planner" in elem:
                        self.append(UpgradePlanner(elem))
                    elif "blueprint_book" in elem:
                        self.append(BlueprintBook(elem))
                    else:
                        raise TypeError(
                            "Dictionary input cannot be resolve to a blueprintable"
                        )
                    # fmt: on
                else:
                    self.append(elem)

    def insert(self, idx, value):
        # type: (int, Blueprintable) -> None
        # Make sure the blueprintable is valid
        self.check_blueprintable(value)

        self.data.insert(idx, value)

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        # type: (int, Union[Blueprint, BlueprintBook]) -> None
        # Make sure the blueprintable is valid
        self.check_blueprintable(value)

        self.data[idx] = value

    def __delitem__(self, idx):
        del self.data[idx]

    def __len__(self):
        return len(self.data)

    def check_blueprintable(self, blueprintable):
        if not isinstance(
            blueprintable,
            (Blueprint, DeconstructionPlanner, UpgradePlanner, BlueprintBook),
        ):
            raise TypeError(
                "Entry into BlueprintableList must be one of (Blueprint, "
                "DeconstructionPlanner, UpgradePlanner, BlueprintBook)"
            )


class BlueprintBook(Blueprintable):
    """
    Factorio Blueprint Book class. Contains a list of :py:class:`.Blueprintable`
    objects as well as some of it's own metadata.
    """

    @utils.reissue_warnings
    def __init__(self, blueprint_book=None):
        # type: (str, Union[str, dict]) -> None
        """
        Creates a ``BlueprintBook`` class. Will load the data from
        ``blueprint_book`` if provided, otherwise initializes with defaults.

        :param blueprint_book: Either a Factorio-format blueprint string or a
            ``dict`` object with the desired keys in the correct format.
        """
        super(BlueprintBook, self).__init__(
            root_item="blueprint_book", item="blueprint-book", init_data=blueprint_book
        )

    @utils.reissue_warnings
    def setup(self, **kwargs):
        self._root = {}

        self._root["item"] = "blueprint-book"
        kwargs.pop("item", None)

        self.label = kwargs.pop("label", None)
        self.label_color = kwargs.pop("label_color", None)
        self.description = kwargs.pop("description", None)
        self.icons = kwargs.pop("icons", None)
        self.active_index = kwargs.pop("active_index", 0)

        if "version" in kwargs:
            self.version = kwargs.pop("version")
        else:
            self.version = utils.encode_version(*__factorio_version_info__)

        if "blueprints" in kwargs:
            self._root["blueprints"] = BlueprintableList(kwargs.pop("blueprints"))
        else:
            self._root["blueprints"] = BlueprintableList()

        # Issue warnings for any keyword not recognized by BlueprintBook
        for unused_arg in kwargs:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

    # =========================================================================
    # BlueprintBook properties
    # =========================================================================

    @property
    def label_color(self):
        # type: () -> dict
        """
        The color of the BlueprintBook's label.

        The ``label_color`` parameter exists in a dict format with the "r", "g",
        "b", and an optional "a" keys. The color can be specified like that, or
        it can be specified more succinctly as a sequence of 3-4 numbers,
        representing the colors in that order.

        The value of each of the numbers (according to Factorio spec) can be
        either in the range of [0.0, 1.0] or [0, 255]; if all the numbers are
        <= 1.0, the former range is used, and the latter otherwise. If "a" is
        omitted, it defaults to 1.0 or 255 when imported, depending on the
        range of the other numbers.

        :getter: Gets the color of the label, or ``None`` if not set.
        :setter: Sets the label color of the BlueprintBook.
        :type: ``dict{"r": number, "g": number, "b": number, Optional("a"): number}``

        :exception DataFormatError: If the input ``label_color`` does not match
            the above specification.

        :example:

        .. code-block:: python

            blueprint.label_color = (127, 127, 127)
            print(blueprint.label_color)
            # {'r': 127.0, 'g': 127.0, 'b': 127.0}
        """
        return self._root.get("label_color", None)

    @label_color.setter
    def label_color(self, value):
        # type: (dict) -> None
        if value is None:
            self._root.pop("label_color", None)
            return
        try:
            self._root["label_color"] = signatures.COLOR.validate(value)
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def active_index(self):
        # type: () -> int
        """
        The currently selected Blueprintable in the BlueprintBook. Zero-indexed,
        from ``0`` to ``len(blueprint_book.blueprints) - 1``.

        :getter: Gets the index of the currently selected blueprint or blueprint
            book.
        :setter: Sets the index of the currently selected blueprint or blueprint
            book. If the value is ``None``, ``active_index`` defaults to ``0``.
        :type: ``int``

        :exception TypeError: If set to anything other than an ``int`` or
            ``None``.
        """
        return self._root.get("active_index", None)

    @active_index.setter
    def active_index(self, value):
        # type: (int) -> None
        if value is None:
            self._root["active_index"] = 0
        elif isinstance(value, int):
            if not 0 <= value < 65536:
                raise IndexError(
                    "'active_index' ({}) not in range [0, 65536)".format(value)
                )
            elif self.blueprints is not None and value >= len(self.blueprints):
                warnings.warn(
                    "'active_index' ({}) not in range [0, {})".format(
                        value, len(self.blueprints)
                    ),
                    IndexWarning,
                    stacklevel=2,
                )
            self._root["active_index"] = value
        else:
            raise TypeError("'active_index' must be a int or None")

    # =========================================================================

    @property
    def blueprints(self):
        # type: () -> BlueprintableList
        """
        The list of Blueprints or BlueprintBooks contained within this
        BlueprintBook.

        :getter: Gets the list of Blueprintables.
        :setter: Sets the list of Blueprintables. The list is initialized empty
            if set to ``None``.
        :type: ``BlueprintableList``

        :exception TypeError: If set to anything other than ``list`` or
            ``None``.
        """
        return self._root.get("blueprints", None)

    @blueprints.setter
    def blueprints(self, value):
        if value is None:
            self._root["blueprints"] = BlueprintableList()
        elif isinstance(value, list):
            self._root["blueprints"] = BlueprintableList(value)
        else:
            raise TypeError("'blueprints' must be a list or None")

    # =========================================================================
    # Utility functions
    # =========================================================================

    def to_dict(self):
        # type: () -> dict
        """
        Returns the blueprint as a dictionary. Intended for getting the
        precursor to a Factorio blueprint string before encoding and compression
        takes place.

        :returns: The dict representation of the BlueprintBook.
        """
        # Get the root dicts from each blueprint and insert them into blueprints
        out_dict = copy.deepcopy(self._root)

        out_dict["blueprints"] = []
        for i, blueprintable in enumerate(self.blueprints):
            blueprintable_entry = blueprintable.to_dict()
            blueprintable_entry["index"] = i
            out_dict["blueprints"].append(blueprintable_entry)

        if len(out_dict["blueprints"]) == 0:
            del out_dict["blueprints"]

        return {"blueprint_book": out_dict}
