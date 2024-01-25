# constant_combinator.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
)
from draftsman.error import DataFormatError
import draftsman.signatures as signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import constant_combinators
from draftsman.data import entities
from draftsman.data import signals

from schema import SchemaError
import six
import warnings


class ConstantCombinator(
    ControlBehaviorMixin, CircuitConnectableMixin, DirectionalMixin, Entity
):
    """
    A combinator that holds a number of constant signals that can be output to
    the circuit network.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **DirectionalMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(DirectionalMixin._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(ControlBehaviorMixin._exports)

    def __init__(self, name=constant_combinators[0], **kwargs):
        # type: (str, **dict) -> None
        super(ConstantCombinator, self).__init__(name, constant_combinators, **kwargs)

        self._item_slot_count = entities.raw[self.name]["item_slot_count"]

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

    # =========================================================================

    @ControlBehaviorMixin.control_behavior.setter
    def control_behavior(self, value):
        # type: (dict) -> None
        try:
            self._control_behavior = (
                signatures.CONSTANT_COMBINATOR_CONTROL_BEHAVIOR.validate(value)
            )
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def item_slot_count(self):
        # type: () -> int
        """
        The total number of signal slots that this ``ConstantCombinator`` can
        hold. Equivalent to ``"item_slot_count"`` from Factorio's ``data.raw``.
        Not exported; read only.

        :type: ``int``
        """
        return self._item_slot_count

    # =========================================================================

    @property
    def signals(self):
        # type: () -> list
        """
        The list of signals that this :py:class:`.ConstantCombinator` currently
        holds. Aliases ``control_behavior["filter"]``. Can be set to one of two
        formats:

        .. code-block:: python

            [{"index": int, "signal": SIGNAL_ID, "count": int}, ...]
            # Or
            [(signal_name, signal_value), (str, int), ...]

        If the data is set to the latter, it is converted to the former.

        Raises :py:class:`.DraftsmanWarning` if a signal is set to one of the
        pure virtual signals ("signal-everything", "signal-anything", or
        "signal-each").

        :getter: Gets the signals of the combinators, or an empty list if not
            set.
        :setter: Sets the signals of the combinators. Removes the key if set to
            ``None``.
        :type: :py:data:`.SIGNAL_FILTERS`

        :exception DataFormatError: If set to anything that does not match the
            format specified above.
        """
        return self.control_behavior.get("filters", [])

    @signals.setter
    def signals(self, value):
        # type: (list) -> None
        if value is None:
            self.control_behavior.pop("filters", None)
        else:
            try:
                value = signatures.SIGNAL_FILTERS.validate(value)
                # Check for pure virtual signals
                # APPARENTLY this is allowed, but because this is not "endorsed"
                # by Factorio we issue warnings if we find one
                for filter in value:
                    if filter["signal"]["name"] in signals.pure_virtual:
                        warnings.warn(
                            "Set signal in index {} to '{}'; is this intentional?".format(
                                filter["index"], filter["signal"]["name"]
                            ),
                            DraftsmanWarning,
                            stacklevel=2,
                        )
                self.control_behavior["filters"] = value
            except SchemaError as e:
                six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def is_on(self):
        """
        Whether or not this Constant combinator is "on" and currently outputting
        it's contents to connected wires. Default state is enabled.

        :getter: Gets whether or not this combinator is enabled, or ``None`` if
            not set.
        :setter: Sets whether or not this combinator is enabled. Removes the key
            if set to ``None``.
        :type: ``bool``
        """
        return self.control_behavior.get("is_on", None)

    @is_on.setter
    def is_on(self, value):
        if value is None:
            self.control_behavior.pop("is_on", None)
        elif isinstance(value, bool):
            self.control_behavior["is_on"] = value
        else:
            raise TypeError("'is_on' must be a bool or None")

    # =========================================================================

    def set_signal(self, index, signal, count=0):
        # type: (int, str, int) -> None
        """
        Set the signal of the ``ConstantCombinator`` at a particular index with
        a particular value.

        :param index: The index of the signal.
        :param signal: The name of the signal.
        :param count: The value of the signal.

        :exception TypeError: If ``index`` is not an ``int``, if ``name`` is not
            a ``str``, or if ``count`` is not an ``int``.
        """
        # Check validity before modifying self
        try:
            index = signatures.INTEGER.validate(index)
            signal = signatures.SIGNAL_ID_OR_NONE.validate(signal)
            # signal = signals.signal_dict(signal) if signal is not None else None
            count = signatures.INTEGER.validate(count)
        except SchemaError as e:
            six.raise_from(TypeError(e), None)

        if not 0 <= index < self.item_slot_count:
            raise IndexError(
                "Signal 'index' ({}) must be in the range [0, {})".format(
                    index, self.item_slot_count
                )
            )

        if "filters" not in self.control_behavior:
            self.control_behavior["filters"] = []

        # Check to see if filters already contains an entry with the same index
        for i, filter in enumerate(self.control_behavior["filters"]):
            if index + 1 == filter["index"]:  # Index already exists in the list
                if signal is None:  # Delete the entry
                    del self.control_behavior["filters"][i]
                else:  # Set the new value
                    self.control_behavior["filters"][i] = {
                        "index": index + 1,
                        "signal": signal,
                        "count": count,
                    }
                return

        # If no entry with the same index was found, create a new one
        self.control_behavior["filters"].append(
            {"index": index + 1, "signal": signal, "count": count}
        )

    def get_signal(self, index):
        # type: (int) -> dict
        """
        Get the :py:data:`.SIGNAL_FILTER` ``dict`` entry at a particular index,
        if it exists.

        :param index: The index of the signal to analyze.

        :returns: A ``dict`` that conforms to :py:data:`.SIGNAL_FILTER`, or
            ``None`` if nothing was found at that index.
        """
        filters = self.control_behavior.get("filters", None)
        if not filters:
            return None

        return next((item for item in filters if item["index"] == index + 1), None)

    # def set_signals(self, signals):
    #     # type: (list) -> None
    #     """
    #     Set all the signals of the ``ConstantCombinator``.

    #     ``signals`` can be specified as one of two formats:

    #     where the location of each tuple in the parent list is equivalent to the
    #     ``index`` of the entry in the ``ConstantCombinator``.

    #     :param signals: The signals to set the data to, in the format
    #         :py:data:`.SIGNAL_FILTERS` specified above.

    #     :exception DataFormatError: If ``signals`` does not match the format
    #         specified in :py:data:`.SIGNAL_FILTERS`.
    #     """
    #     if signals is None:
    #         self.control_behavior.pop("filters", None)
    #     else:
    #         try:
    #             signals = signatures.SIGNAL_FILTERS.validate(signals)
    #             self.control_behavior["filters"] = signals
    #         except SchemaError as e:
    #             six.raise_from(DataFormatError(e), None)
