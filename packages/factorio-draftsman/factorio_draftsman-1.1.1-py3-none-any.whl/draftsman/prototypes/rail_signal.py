# rail_signal.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    ReadRailSignalMixin,
    CircuitConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    EightWayDirectionalMixin,
)
from draftsman.error import DataFormatError
from draftsman import signatures
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import rail_signals
from draftsman.data import entities

from schema import SchemaError
import six
import warnings


class RailSignal(
    ReadRailSignalMixin,
    CircuitConditionMixin,
    EnableDisableMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    EightWayDirectionalMixin,
    Entity,
):
    """
    A rail signal that determines whether or not trains can pass along their
    rail block.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **EightWayDirectionalMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **ControlBehaviorMixin._exports,
    #     **EnableDisableMixin._exports,
    #     **CircuitConditionMixin._exports,
    #     **ReadRailSignalMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(EightWayDirectionalMixin._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(ControlBehaviorMixin._exports)
    _exports.update(EnableDisableMixin._exports)
    _exports.update(CircuitConditionMixin._exports)
    _exports.update(ReadRailSignalMixin._exports)

    def __init__(self, name=rail_signals[0], **kwargs):
        # type: (str, **dict) -> None
        """
        TODO
        """

        # Set a (private) flag to indicate to the constructor to not generate
        # rotations, and rather just use the same collision set regardless of
        # rotation
        self._disable_collision_set_rotation = True

        super(RailSignal, self).__init__(name, rail_signals, **kwargs)

        if "collision_mask" in entities.raw[self.name]:  # pragma: no coverage
            self._collision_mask = set(entities.raw[self.name]["collision_mask"])
        else:  # pragma: no coverage
            self._collision_mask = {"floor-layer", "rail-layer", "item-layer"}

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
            self._control_behavior = signatures.RAIL_SIGNAL_CONTROL_BEHAVIOR.validate(
                value
            )
        except SchemaError as e:
            six.raise_from(DataFormatError(e), None)

    # =========================================================================

    @property
    def read_signal(self):
        # type: () -> bool
        """
        Whether or not to read the state of the rail signal as their output
        signals.

        :getter: Gets whether or not to read the signal, or ``None`` if not set.
        :setter: Sets whether or not to read the signal. Removes the key if set
            to ``None``.
        :type: ``bool``

        :exception TypeError: If set to anything other than a ``bool`` or ``None``.
        """
        return self.control_behavior.get("circuit_read_signal", None)

    @read_signal.setter
    def read_signal(self, value):
        # type: (bool) -> None
        if value is None:
            self.control_behavior.pop("circuit_read_signal", None)
        elif isinstance(value, bool):
            self.control_behavior["circuit_read_signal"] = value
        else:
            raise TypeError("'read_signal' must be a bool or None")

    # =========================================================================

    @property
    def enable_disable(self):
        # type: () -> bool
        return self.control_behavior.get("circuit_close_signal", None)

    @enable_disable.setter
    def enable_disable(self, value):
        # type: (bool) -> None
        if value is None:
            self.control_behavior.pop("circuit_close_signal", None)
        elif isinstance(value, bool):
            self.control_behavior["circuit_close_signal"] = value
        else:
            raise TypeError("'enable_disable' must be a bool or None")

    # =========================================================================

    # def on_insert(self, parent):
    #     # Check if the rail_signal is adjacent to a rail
    #     # This test has to be more sophisticated than just testing for adjacent
    #     # entities; we also must consider the orientation of signal to ensure
    #     # it is facing the correct direction (must be on the right side of the
    #     # track, unless there exists another signal on the opposite side)
    #     pass
