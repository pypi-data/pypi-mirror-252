# test_upgrade_planner.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman import __factorio_version_info__
from draftsman.classes.upgrade_planner import UpgradePlanner
from draftsman.error import (
    IncorrectBlueprintTypeError,
    MalformedBlueprintStringError,
    DataFormatError,
)
from draftsman import utils
from draftsman.warning import DraftsmanWarning, ValueWarning

import sys

if sys.version_info >= (3, 3):  # pragma: no coverage
    import unittest
else:  # pragma: no coverage
    import unittest2 as unittest


class UpgradePlannerTesting(unittest.TestCase):
    def test_constructor(self):
        # Empty
        upgrade_planner = UpgradePlanner()
        self.assertEqual(
            upgrade_planner.to_dict()["upgrade_planner"],
            {
                "item": "upgrade-planner",
                "settings": None,
                "version": utils.encode_version(*__factorio_version_info__),
            },
        )

        # String
        upgrade_planner = UpgradePlanner(
            "0eNqrViotSC9KTEmNL8hJzMtLLVKyqlYqTi0pycxLL1ayyivNydFRyixJzVWygqnUhanUUSpLLSrOzM9TsjKyMDQxtzQyNzUDIhOL2loAhpkdww=="
        )
        self.assertEqual(
            upgrade_planner.to_dict()["upgrade_planner"],
            {
                "item": "upgrade-planner",
                "settings": None,
                "version": utils.encode_version(1, 1, 61),
            },
        )

        # Dict
        test_planner = {
            "upgrade_planner": {
                "settings": {
                    "mappers": [
                        {
                            "from": "transport-belt",
                            "to": "fast-transport-belt",
                            "index": 0,
                        }
                    ]
                }
            }
        }
        upgrade_planner = UpgradePlanner(test_planner)
        self.assertEqual(
            upgrade_planner.to_dict()["upgrade_planner"],
            {
                "item": "upgrade-planner",
                "settings": {
                    "mappers": [
                        {
                            "from": {"name": "transport-belt", "type": "item"},
                            "to": {"name": "fast-transport-belt", "type": "item"},
                            "index": 0,
                        }
                    ]
                },
                "version": utils.encode_version(*__factorio_version_info__),
            },
        )

        # Warnings
        with self.assertWarns(DraftsmanWarning):
            UpgradePlanner({"upgrade_planner": {"unused": "keyword"}})

        # TypeError
        with self.assertRaises(TypeError):
            UpgradePlanner(TypeError)

        # Correct format, but incorrect type
        with self.assertRaises(IncorrectBlueprintTypeError):
            UpgradePlanner(
                "0eNqrVkrKKU0tKMrMK1GyqlbKLEnNVbJCEtNRKkstKs7Mz1OyMrIwNDG3NDI3sTQ1MTc1rq0FAHmyE1c="
            )

        # Incorrect format
        with self.assertRaises(MalformedBlueprintStringError):
            UpgradePlanner("0lmaothisiswrong")

    def test_set_mappers(self):
        upgrade_planner = UpgradePlanner()

        # Test full format
        upgrade_planner.mappers = [
            {
                "from": {"name": "transport-belt", "type": "item"},
                "to": {"name": "fast-transport-belt", "type": "item"},
                "index": 0,
            },
            {
                "from": {"name": "transport-belt", "type": "item"},
                "to": {"name": "express-transport-belt", "type": "item"},
                "index": 23,
            },
        ]
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "fast-transport-belt", "type": "item"},
                    "index": 0,
                },
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 23,
                },
            ],
        )

        # Test abridged format
        upgrade_planner.mappers = [
            ("transport-belt", "fast-transport-belt"),
            ("transport-belt", "express-transport-belt"),
        ]
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "fast-transport-belt", "type": "item"},
                    "index": 0,
                },
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
            ],
        )

        # Test None
        upgrade_planner.mappers = None
        self.assertEqual(upgrade_planner.mappers, None)
        self.assertNotIn("mappers", upgrade_planner._root["settings"])

        # Warnings
        # Index out of range warning
        with self.assertWarns(ValueWarning):
            upgrade_planner.mappers = [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "fast-transport-belt", "type": "item"},
                    "index": 24,
                },
            ]

        # Errors
        with self.assertRaises(DataFormatError):
            upgrade_planner.mappers = ("incorrect", "incorrect")

        with self.assertRaises(DataFormatError):
            upgrade_planner.mappers = [TypeError, TypeError]

    def test_mapping(self):
        upgrade_planner = UpgradePlanner()
        upgrade_planner.set_mapping("transport-belt", "fast-transport-belt", 0)
        upgrade_planner.set_mapping("transport-belt", "express-transport-belt", 1)
        self.assertEqual(len(upgrade_planner.mappers), 2)
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "fast-transport-belt", "type": "item"},
                    "index": 0,
                },
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
            ],
        )

        # Test no index
        upgrade_planner.set_mapping("inserter", "fast-inserter", 2)
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "fast-transport-belt", "type": "item"},
                    "index": 0,
                },
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
                {
                    "from": {"name": "inserter", "type": "item"},
                    "to": {"name": "fast-inserter", "type": "item"},
                    "index": 2,
                },
            ],
        )

        # Test duplicate mapping
        upgrade_planner.set_mapping("transport-belt", "fast-transport-belt", 0)
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "fast-transport-belt", "type": "item"},
                    "index": 0,
                },
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
                {
                    "from": {"name": "inserter", "type": "item"},
                    "to": {"name": "fast-inserter", "type": "item"},
                    "index": 2,
                },
            ],
        )

        # Warnings

        # Duplicate indices
        # TODO

        # Errors
        with self.assertRaises(DataFormatError):
            upgrade_planner.set_mapping(TypeError, TypeError, TypeError)

        # =====================================================================
        # remove_mapping()
        # =====================================================================

        # Normal
        upgrade_planner.remove_mapping("transport-belt", "fast-transport-belt", 0)
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
                {
                    "from": {"name": "inserter", "type": "item"},
                    "to": {"name": "fast-inserter", "type": "item"},
                    "index": 2,
                },
            ],
        )

        # Remove no longer existing
        upgrade_planner.remove_mapping("transport-belt", "fast-transport-belt", 0)
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
                {
                    "from": {"name": "inserter", "type": "item"},
                    "to": {"name": "fast-inserter", "type": "item"},
                    "index": 2,
                },
            ],
        )

        # Remove first occurence of duplicates
        upgrade_planner.set_mapping("inserter", "fast-inserter", 3)
        upgrade_planner.remove_mapping("inserter", "fast-inserter")
        self.assertEqual(
            upgrade_planner.mappers,
            [
                {
                    "from": {"name": "transport-belt", "type": "item"},
                    "to": {"name": "express-transport-belt", "type": "item"},
                    "index": 1,
                },
                {
                    "from": {"name": "inserter", "type": "item"},
                    "to": {"name": "fast-inserter", "type": "item"},
                    "index": 3,
                },
            ],
        )

        # Warnings
        with self.assertWarns(ValueWarning):
            upgrade_planner.remove_mapping("inserter", "fast-inserter", -1)
        with self.assertWarns(ValueWarning):
            upgrade_planner.remove_mapping("inserter", "fast-inserter", 24)

        # Errors
        with self.assertRaises(DataFormatError):
            upgrade_planner.remove_mapping("inserter", "incorrect")
