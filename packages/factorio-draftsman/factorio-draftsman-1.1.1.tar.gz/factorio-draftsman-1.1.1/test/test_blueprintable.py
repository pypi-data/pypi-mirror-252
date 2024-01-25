# test_blueprintable.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.blueprintable import *
from draftsman.error import MalformedBlueprintStringError, IncorrectBlueprintTypeError
from draftsman.utils import JSON_to_string

import sys

if sys.version_info >= (3, 3):  # pragma: no coverage
    import unittest
else:  # pragma: no coverage
    import unittest2 as unittest


class BlueprintableTesting(unittest.TestCase):
    def test_item(self):
        blueprint = Blueprint()
        self.assertEqual(blueprint.item, "blueprint")

        decon_planner = DeconstructionPlanner()
        self.assertEqual(decon_planner.item, "deconstruction-planner")

        upgrade_planner = UpgradePlanner()
        self.assertEqual(upgrade_planner.item, "upgrade-planner")

        blueprint_book = BlueprintBook()
        self.assertEqual(blueprint_book.item, "blueprint-book")


class BlueprintUtilsTesting(unittest.TestCase):
    def test_get_blueprintable_from_string(self):
        # Valid Format (Blueprint)
        blueprintable = get_blueprintable_from_string(
            "0eNqrVkrKKU0tKMrMK1GyqlbKLEnNVbJCEtNRKkstKs7Mz1OyMrIwNDG3NDI3sTQ1MTc1rq0FAHmyE1c="
        )
        self.assertIsInstance(blueprintable, Blueprint)

        # Valid Format (DeconstructionPlanner)
        blueprintable = get_blueprintable_from_string(
            "0eNqrVkpJTc7PKy4pKk0uyczPiy/ISczLSy1SsqpWKk4tKcnMSy9WssorzcnRUcosSc1VskLToAvToKNUllpUDBRRsjKyMDQxtzQyNzUDIhOL2loAsN4j2w=="
        )
        self.assertIsInstance(blueprintable, DeconstructionPlanner)

        # Valid Format (UpgradePlanner)
        blueprintable = get_blueprintable_from_string(
            "0eNqrViotSC9KTEmNL8hJzMtLLVKyqlYqTi0pycxLL1ayyivNydFRyixJzVWygqnUhanUUSpLLSrOzM9TsjKyMDQxtzQyNzUDIhOL2loAhpkdww=="
        )
        self.assertIsInstance(blueprintable, UpgradePlanner)

        # Valid format (BlueprintBook)
        blueprintable = get_blueprintable_from_string(
            "0eNqrVkrKKU0tKMrMK4lPys/PVrKqVsosSc1VskJI6IIldJQSk0syy1LjM/NSUiuUrAx0lMpSi4oz8/OUrIwsDE3MLY3MTSxNTcxNjWtrAVWjHQY="
        )
        self.assertIsInstance(blueprintable, BlueprintBook)

        # Test description key
        blueprintable = get_blueprintable_from_string(
            "0eNqllNuOozAMhl8lytWuBCOgnMqr7FRVAJdaCglKwnQ6Fe8+Tumy2i6jbTWICxLb/+fYxBdeyxEGg8rx6sJbsI3BwaFWvOInYPaoR9myDhw7CaNQdZaJWo+O/ZBwcMxpZrA7up/Vq3pVIRvVoE9goGU1iEYrdkJ3ZEqzXrejBLvm4/e+9r6zwOEAjWMGGsA3MFcXYS30tQSzeJEZB+ABR4q1vPp14RY7JaQ/pDuTqeLooCcPJXq/mjF8ohDVwjuv4mkXcFAOHcKscF2c92rsazDksMSCpJQMNiEoMN05pGKCOYjGJzBoi3M5L5xUwzzfBvxMH2WZEqwe6Txmb/GDhOJoeabgH17yJ1fswoU5aLnKKaLfnIQ4CqhL1Dfjj7LZrchvnpPPv5ZPgnQNkD4HSMvn8s/uW7miWcYv2U212L5k04pM/oBMUf4tE1z/JevtdgBow/n3DTfUtDVG8Qgj+m+q5QMyefS9VLcPMNJvliOOFsjtJtOYCXvRHFH5qDVkdled3Qz1eS7zLOBS1EBXnpMgjSqwfs8PjatUUsZpsU2KLKc3LafpExROpg4="
        )
        self.maxDiff = None
        self.assertEqual(
            blueprintable.to_dict(),
            {
                "blueprint": {
                    "item": "blueprint",
                    "label": "lint test",
                    "description": "we should get warnings about (left to right):\n\n- unpowered beacon with no modules\n- unpowered beacon\n- beacon with no modules\n- beacon with no effect receivers\n- assembler with no recipe",
                    "icons": [
                        {"index": 1, "signal": {"name": "beacon", "type": "item"}}
                    ],
                    "entities": [
                        {
                            "entity_number": 1,
                            "name": "electric-energy-interface",
                            "position": {"x": -669.0, "y": -884.0},
                            "buffer_size": 10000000000,
                        },
                        {
                            "entity_number": 2,
                            "name": "big-electric-pole",
                            "position": {"x": -670.0, "y": -882.0},
                            "neighbours": [3],
                        },
                        {
                            "entity_number": 3,
                            "name": "big-electric-pole",
                            "position": {"x": -660.0, "y": -882.0},
                            "neighbours": [2, 4],
                        },
                        {
                            "entity_number": 4,
                            "name": "big-electric-pole",
                            "position": {"x": -648.0, "y": -882.0},
                            "neighbours": [3],
                        },
                        {
                            "entity_number": 5,
                            "name": "beacon",
                            "position": {"x": -681.5, "y": -879.5},
                        },
                        {
                            "entity_number": 6,
                            "name": "beacon",
                            "position": {"x": -678.5, "y": -879.5},
                            "items": {"speed-module-3": 2},
                        },
                        {
                            "entity_number": 7,
                            "name": "beacon",
                            "position": {"x": -670.5, "y": -879.5},
                        },
                        {
                            "entity_number": 8,
                            "name": "beacon",
                            "position": {"x": -660.5, "y": -879.5},
                            "items": {"speed-module-3": 2},
                        },
                        {
                            "entity_number": 9,
                            "name": "beacon",
                            "position": {"x": -648.5, "y": -879.5},
                            "items": {"speed-module-3": 2},
                        },
                        {
                            "entity_number": 10,
                            "name": "assembling-machine-3",
                            "position": {"x": -645.5, "y": -879.5},
                        },
                    ],
                    "version": 281479275675648,
                }
            },
        )
        # Invalid format
        with self.assertRaises(MalformedBlueprintStringError):
            get_blueprintable_from_string("0lmaothisiswrong")

        example = JSON_to_string({"incorrect": {}})
        with self.assertRaises(IncorrectBlueprintTypeError):
            get_blueprintable_from_string(example)

    def test_get_blueprintable_from_JSON(self):
        # Valid Format (Blueprint)
        json_dict = {"blueprint": {"item": "blueprint"}}
        blueprintable = get_blueprintable_from_JSON(json_dict)
        self.assertIsInstance(blueprintable, Blueprint)

        # Valid Format (DeconstructionPlanner)
        json_dict = {"deconstruction_planner": {"item": "deconstruction-planner"}}
        blueprintable = get_blueprintable_from_JSON(json_dict)
        self.assertIsInstance(blueprintable, DeconstructionPlanner)

        # Valid Format (UpgradePlanner)
        json_dict = {"upgrade_planner": {"item": "upgrade-planner"}}
        blueprintable = get_blueprintable_from_JSON(json_dict)
        self.assertIsInstance(blueprintable, UpgradePlanner)

        # Valid format (BlueprintBook)
        json_dict = {"blueprint_book": {"item": "blueprint-book"}}
        blueprintable = get_blueprintable_from_JSON(json_dict)
        self.assertIsInstance(blueprintable, BlueprintBook)

        example = {"incorrect": {}}
        with self.assertRaises(IncorrectBlueprintTypeError):
            get_blueprintable_from_JSON(example)
