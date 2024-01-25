# logistic_buffer_container.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    RequestItemsMixin,
    LogisticModeOfOperationMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    RequestFiltersMixin,
    InventoryMixin,
)
from draftsman.constants import LogisticModeOfOperation
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import logistic_buffer_containers

from schema import SchemaError
import six
import warnings


class LogisticBufferContainer(
    InventoryMixin,
    RequestItemsMixin,
    LogisticModeOfOperationMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    RequestFiltersMixin,
    Entity,
):
    """
    A logistics container that requests items on a secondary priority.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **RequestFiltersMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **LogisticModeOfOperationMixin._exports,
    #     **RequestItemsMixin._exports,
    #     **InventoryMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(RequestFiltersMixin._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(ControlBehaviorMixin._exports)
    _exports.update(LogisticModeOfOperationMixin._exports)
    _exports.update(RequestItemsMixin._exports)
    _exports.update(InventoryMixin._exports)

    def __init__(self, name=logistic_buffer_containers[0], **kwargs):
        # type: (str, **dict) -> None
        # Set the mode of operation type for this entity
        self._mode_of_operation_type = LogisticModeOfOperation

        super(LogisticBufferContainer, self).__init__(
            name, logistic_buffer_containers, **kwargs
        )

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
                signatures.LOGISTIC_BUFFER_CONTROL_BEHAVIOR.validate(value)
            )
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)
