# logistic_storage_container.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    RequestItemsMixin,
    CircuitConnectableMixin,
    RequestFiltersMixin,
    InventoryMixin,
)
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import logistic_storage_containers

import warnings


class LogisticStorageContainer(
    InventoryMixin,
    RequestItemsMixin,
    CircuitConnectableMixin,
    RequestFiltersMixin,
    Entity,
):
    """
    A logistics container that stores items not currently being used in the
    logistic network.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **RequestFiltersMixin._exports,
    #     **CircuitConnectableMixin._exports,
    #     **RequestItemsMixin._exports,
    #     **InventoryMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(RequestFiltersMixin._exports)
    _exports.update(CircuitConnectableMixin._exports)
    _exports.update(RequestItemsMixin._exports)
    _exports.update(InventoryMixin._exports)

    def __init__(self, name=logistic_storage_containers[0], **kwargs):
        # type: (str, **dict) -> None
        super(LogisticStorageContainer, self).__init__(
            name, logistic_storage_containers, **kwargs
        )

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )
