# radar.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes.entity import Entity
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import radars

import warnings


class Radar(Entity):
    """
    An entity that scans neighbouring chunks periodically.
    """

    # fmt: off
    # _exports = {
    #     **Entity._exports
    # }
    # fmt: on

    _exports = {}
    _exports.update(Entity._exports)

    def __init__(self, name=radars[0], **kwargs):
        # type: (str, **dict) -> None
        super(Radar, self).__init__(name, radars, **kwargs)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )
