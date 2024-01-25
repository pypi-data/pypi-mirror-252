# wall.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    CircuitConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
)
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import walls
from draftsman.data.signals import signal_dict

from schema import SchemaError
import six
from typing import Union
import warnings


class Wall(
    CircuitConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    Entity,
):
    """
    A destructable barrier that acts as protection for static structures.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **EnableDisableMixin._exports,
    #     **CircuitConditionMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(ControlBehaviorMixin._exports)
    _exports.update(EnableDisableMixin._exports)
    _exports.update(CircuitConditionMixin._exports)

    def __init__(self, name=walls[0], **kwargs):
        # type: (str, **dict) -> None
        super(Wall, self).__init__(name, walls, **kwargs)

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
            self._control_behavior = signatures.WALL_CONTROL_BEHAVIOR.validate(value)
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def enable_disable(self):
        # type: () -> bool
        return self.control_behavior.get("circuit_open_gate", None)

    @enable_disable.setter
    def enable_disable(self, value):
        # type: (bool) -> None
        if value is None:
            self.control_behavior.pop("circuit_open_gate", None)
        elif isinstance(value, bool):
            self.control_behavior["circuit_open_gate"] = value
        else:
            raise TypeError("'enable_disable' must be a bool or None")

    # =========================================================================

    @property
    def read_gate(self):
        # type: () -> bool
        """
        Whether or not to read the state of an adjacent gate, whether it's
        opened or closed.

        :type: ``bool``
        """
        return self.control_behavior.get("circuit_read_sensor", None)

    @read_gate.setter
    def read_gate(self, value):
        # type: (bool) -> None
        if value is None:
            self.control_behavior.pop("circuit_read_sensor", None)
        elif isinstance(value, bool):
            self.control_behavior["circuit_read_sensor"] = value
        else:
            raise TypeError("'read_gate' must be a bool or None")

    # =========================================================================

    @property
    def output_signal(self):
        # type: () -> dict
        """
        What signal to output the state of the adjacent gate.

        :type: :py:class:`.SIGNAL_ID`
        """
        return self.control_behavior.get("output_signal", None)

    @output_signal.setter
    def output_signal(self, value):
        # type: (Union[str, dict]) -> None
        if value is None:
            self.control_behavior.pop("output_signal", None)
        elif isinstance(value, six.string_types):
            value = six.text_type(value)
            self.control_behavior["output_signal"] = signal_dict(value)
        else:  # dict or other
            try:
                value = signatures.SIGNAL_ID.validate(value)
                self.control_behavior["output_signal"] = value
            except SchemaError:
                raise TypeError("Incorrectly formatted SignalID")
