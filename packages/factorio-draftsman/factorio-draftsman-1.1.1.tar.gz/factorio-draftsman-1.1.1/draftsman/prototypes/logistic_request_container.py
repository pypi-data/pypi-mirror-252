# logistic_request_container.py
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
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import logistic_request_containers

from schema import SchemaError
import six
import warnings


class LogisticRequestContainer(
    InventoryMixin,
    RequestItemsMixin,
    LogisticModeOfOperationMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    RequestFiltersMixin,
    Entity,
):
    """
    A logistics container that requests items with a primary priority.
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
    #     "request_from_buffers": {
    #         "format": "bool",
    #         "description": "Whether or not to request from buffer chests",
    #         "required": lambda x: x is not None,
    #     },
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
    _exports.update(
        {
            "request_from_buffers": {
                "format": "bool",
                "description": "Whether or not to request from buffer chests",
                "required": lambda x: x is not None,
            }
        }
    )

    def __init__(self, name=logistic_request_containers[0], **kwargs):
        # type: (str, **dict) -> None
        super(LogisticRequestContainer, self).__init__(
            name, logistic_request_containers, **kwargs
        )

        self.request_from_buffers = None
        if "request_from_buffers" in kwargs:
            self.request_from_buffers = kwargs["request_from_buffers"]
            self.unused_args.pop("request_from_buffers")
        # self._add_export("request_from_buffers", lambda x: x is not None)

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
                signatures.LOGISTIC_REQUESTER_CONTROL_BEHAVIOR.validate(value)
            )
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def request_from_buffers(self):
        # type: () -> bool
        """
        Whether or not this requester can request from buffer chests.

        :getter: Gets whether or not to recieve from buffers.
        :setter: Sets whether or not to recieve from buffers.
        :type: ``bool``

        :exception TypeError: If set to anything other than a ``bool`` or ``None``.
        """
        return self._request_from_buffers

    @request_from_buffers.setter
    def request_from_buffers(self, value):
        # type: (bool) -> None
        if value is None or isinstance(value, bool):
            self._request_from_buffers = value
        else:
            raise TypeError("'request_from_buffers' must be a bool or None")
