# offshore_pump.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    CircuitConditionMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
)
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import offshore_pumps

from schema import SchemaError
import six
import warnings


class OffshorePump(
    CircuitConditionMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
    Entity,
):
    """
    An entity that pumps a fluid from the environment.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **DirectionalMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **LogisticConditionMixin._exports,
    #     **CircuitConditionMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(DirectionalMixin._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(ControlBehaviorMixin._exports)
    _exports.update(LogisticConditionMixin._exports)
    _exports.update(CircuitConditionMixin._exports)

    def __init__(self, name=offshore_pumps[0], **kwargs):
        # type: (str, **dict) -> None
        super(OffshorePump, self).__init__(name, offshore_pumps, **kwargs)

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
            self._control_behavior = signatures.OFFSHORE_PUMP_CONTROL_BEHAVIOR.validate(
                value
            )
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)
