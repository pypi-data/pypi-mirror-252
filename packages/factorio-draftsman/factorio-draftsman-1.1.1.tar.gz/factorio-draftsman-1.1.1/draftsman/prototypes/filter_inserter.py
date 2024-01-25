# filter_inserter.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    FiltersMixin,
    StackSizeMixin,
    CircuitReadHandMixin,
    InserterModeOfOperationMixin,
    CircuitConditionMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
)
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import filter_inserters

from schema import SchemaError
import six
import warnings


class FilterInserter(
    FiltersMixin,
    StackSizeMixin,
    CircuitReadHandMixin,
    InserterModeOfOperationMixin,
    CircuitConditionMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
    Entity,
):
    """
    An entity that can move items between machines, and has the ability to only
    move specific items.

    .. NOTE::

        In Factorio, the ``Inserter`` prototype includes both regular and filter
        inserters. In Draftsman, inserters are split into two different classes,
        :py:class:`~.Inserter` and :py:class:`~.FilterInserter`
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **DirectionalMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **LogisticConditionMixin._exports,
    #     **CircuitConditionMixin._exports,
    #     **InserterModeOfOperationMixin._exports,
    #     **CircuitReadHandMixin._exports,
    #     **StackSizeMixin._exports,
    #     **FiltersMixin._exports,
    #     "filter_mode": {
    #         "format": "'whitelist' or 'blacklist'",
    #         "description": "Whether or not to invert the item filters specified",
    #         "required": lambda x: x is not None,
    #     },
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(DirectionalMixin._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(ControlBehaviorMixin._exports)
    _exports.update(LogisticConditionMixin._exports)
    _exports.update(CircuitConditionMixin._exports)
    _exports.update(InserterModeOfOperationMixin._exports)
    _exports.update(CircuitReadHandMixin._exports)
    _exports.update(StackSizeMixin._exports)
    _exports.update(FiltersMixin._exports)
    _exports.update(
        {
            "filter_mode": {
                "format": "'whitelist' or 'blacklist'",
                "description": "Whether or not to invert the item filters specified",
                "required": lambda x: x is not None,
            }
        }
    )

    def __init__(self, name=filter_inserters[0], **kwargs):
        # type: (str, **dict) -> None
        super(FilterInserter, self).__init__(name, filter_inserters, **kwargs)

        self.filter_mode = None
        if "filter_mode" in kwargs:
            self.filter_mode = kwargs["filter_mode"]
            self.unused_args.pop("filter_mode")
        # self._add_export("filter_mode", lambda x: x is not None)

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
                signatures.FILTER_INSERTER_CONTROL_BEHAVIOR.validate(value)
            )
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def filter_mode(self):
        # type: () -> str
        """
        The mode that the filter is set to. Can be either ``"whitelist"`` or
        ``"blacklist"``.

        :getter: Gets the filter mode.
        :setter: Sets the filter mode.
        :type: ``str``

        :exception ValueError: If set to a ``str`` that is neither ``"whitelist"``
            nor ``"blacklist"``.
        :exception TypeError: If set to anything other than a ``str`` or ``None``.
        """
        return self._filter_mode

    @filter_mode.setter
    def filter_mode(self, value):
        # type: (str) -> None
        if value is None:
            self._filter_mode = value
        elif isinstance(value, six.string_types):
            value = six.text_type(value)
            valid_modes = {"whitelist", "blacklist"}
            if value not in valid_modes:
                raise ValueError("'filter_mode' must be one of {}".format(valid_modes))
            self._filter_mode = value
        else:
            raise TypeError("'filter_mode' must be a str or None")

    # =========================================================================

    def merge(self, other):
        # type: (FilterInserter) -> None
        super(FilterInserter, self).merge(other)

        self.filter_mode = other.filter_mode
