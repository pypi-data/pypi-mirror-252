# boiler.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import RequestItemsMixin, DirectionalMixin
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import boilers

import warnings


class Boiler(RequestItemsMixin, DirectionalMixin, Entity):
    """
    An entity that uses a fuel to convert a fluid (usually water) to another
    fluid (usually steam).
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports,
    #     **DirectionalMixin._exports,
    #     **RequestItemsMixin._exports,
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)
    _exports.update(DirectionalMixin._exports)
    _exports.update(RequestItemsMixin._exports)

    def __init__(self, name=boilers[0], **kwargs):
        # type: (str, **dict) -> None
        """
        TODO
        """

        super(Boiler, self).__init__(name, boilers, **kwargs)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )
