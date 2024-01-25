# test_group.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman import __factorio_version_info__
from draftsman.classes.association import Association
from draftsman.classes.blueprint import Blueprint
from draftsman.classes.collisionset import CollisionSet
from draftsman.classes.entitylist import EntityList
from draftsman.classes.group import Group
from draftsman.classes.vector import Vector
from draftsman.entity import *
from draftsman.error import (
    DraftsmanError,
    InvalidWireTypeError,
    InvalidConnectionSideError,
    EntityNotPowerConnectableError,
    EntityNotCircuitConnectableError,
    RotationError,
    InvalidAssociationError,
    MalformedBlueprintStringError,
    IncorrectBlueprintTypeError,
)
from draftsman.utils import encode_version, AABB
from draftsman.warning import (
    ConnectionSideWarning,
    ConnectionDistanceWarning,
    RailAlignmentWarning,
    OverlappingObjectsWarning,
)

import sys

if sys.version_info >= (3, 3):  # pragma: no coverage
    import unittest
else:  # pragma: no coverage
    import unittest2 as unittest


class GroupTesting(unittest.TestCase):
    def test_default_constructor(self):
        group = Group("default")
        self.assertEqual(group.id, "default")
        self.assertEqual(group.name, "group")
        self.assertEqual(group.type, "group")
        self.assertEqual(group.tile_width, 0)
        self.assertEqual(group.tile_height, 0)
        self.assertEqual(group.get(), [])

    def test_constructor_init(self):
        entity_list = [
            Furnace("stone-furnace"),
            Container("wooden-chest", tile_position=(4, 0)),
            ProgrammableSpeaker("programmable-speaker", tile_position=(8, 0)),
        ]
        group = Group(
            name="groupA",
            type="custom_type",
            id="test_group",
            position={"x": 124.4, "y": 1.645},
            entities=entity_list,
        )
        self.assertEqual(group.name, "groupA")
        self.assertEqual(group.type, "custom_type")
        self.assertEqual(group.id, "test_group")
        self.assertEqual(group.position, Vector(124.4, 1.645))

        # Initialize from string with entities
        test_string = "0eNqdkttqwzAMht9F187IwVk23/YxSig5aK0gcYLtLAvB7z45ZaW0gbHdGNn6/euT0Ap1N+FoSDtQK1AzaAvquIKls6668OaWEUEBOexBgK76cDNVWxnwAki3+AUq8aUA1I4c4dVguywnPfU1GhY8fBUwDpbVgw412CHNXnIBC6iIA+/Fk0N6cxiHGU1kZ3LNZc9os4kZjrvR2IScDcnDFN+jUQuKtTMZ3OI49HCYkl807HstfbKucszzUXUWd4CzG3CPLU19hB3DGGqicehwBzz9mUDCE3iiT8JhsH3Ek4zEao10vtTDZML4ZbnDI//Kk/2LJ9vhycow222F1N3GCfhEY7eK6Vsii/e0yHMp8+LV+2+Mw9xY"
        group = Group(name="test", position=(1, 1), string=test_string)
        self.assertEqual(group.name, "test")
        self.assertEqual(group.type, "group")
        self.assertEqual(group.id, None)
        self.assertEqual(group.position, Vector(1.0, 1.0))
        # Verify contents
        self.assertEqual(len(group.entities), 4)
        self.assertIsInstance(group.entities[0], Radar)
        self.assertIsInstance(group.entities[1], PowerSwitch)
        self.assertIsInstance(group.entities[2], ElectricPole)
        self.assertIsInstance(group.entities[3], ElectricPole)
        self.assertIs(
            group.entities[2].connections["1"]["red"][0]["entity_id"](),
            group.entities[3],
        )
        self.assertIs(
            group.entities[3].connections["1"]["red"][0]["entity_id"](),
            group.entities[2],
        )
        self.assertIs(group.entities[2].neighbours[0](), group.entities[3])
        self.assertIs(group.entities[3].neighbours[0](), group.entities[2])

        # Initialize from blueprint string with no entities
        empty_blueprint_string = "0eNqrVkrKKU0tKMrMK1GyqlbKLEnNVbJCEtNRKkstKs7Mz1OyMrIwNDG3NDI3NTUxMTU3q60FAHmbE1Y="
        group = Group(string=empty_blueprint_string)
        self.assertEqual(len(group.entities), 0)
        self.assertEqual(group.entities.data, [])

        # Errors
        with self.assertRaises(TypeError):
            Group(unused_keyword="whatever")

        with self.assertRaises(TypeError):
            Group(name=TypeError)

        with self.assertRaises(TypeError):
            Group(type=TypeError)

        with self.assertRaises(TypeError):
            Group(id=TypeError)

        with self.assertRaises(TypeError):
            Group(position="incorrect")

        with self.assertRaises(TypeError):  # TODO: maybe change this?
            Group(entities=InvalidEntityError)

        with self.assertRaises(TypeError):
            Group("test", entities=["incorrect"])

        with self.assertRaises(MalformedBlueprintStringError):
            Group(string="incorrect")
        with self.assertRaises(IncorrectBlueprintTypeError):
            Group(
                string="0eNqrVkrKKU0tKMrMK4lPys/PVrKqRogUK1lFI3FBcpklqblKVkhiOkplqUXFmfl5SlZGFoYm5pZG5qamJiam5ma1OkqZeSmpFUpWBrWxOhg6dcHW6SglJpdklqXGw5TiMa8WAEeOOPY="
            )

    def test_set_name(self):
        group = Group("test")
        group.name = "something other than group"
        self.assertEqual(group.name, "something other than group")

        with self.assertRaises(TypeError):
            group.name = None
        with self.assertRaises(TypeError):
            group.name = TypeError

    def test_set_type(self):
        group = Group("test")
        group.type = "something other than group"
        self.assertEqual(group.type, "something other than group")

        with self.assertRaises(TypeError):
            group.type = None
        with self.assertRaises(TypeError):
            group.type = TypeError

    def test_set_id(self):
        group = Group("test")
        group.id = "something else"
        self.assertEqual(group.id, "something else")

        group.id = None
        self.assertEqual(group.id, None)

        with self.assertRaises(TypeError):
            group.id = TypeError

        # Test key map modification
        blueprint = Blueprint()
        blueprint.entities.append(group)

        blueprint.entities[0].id = "another_thing"
        self.assertEqual(blueprint.entities[0].id, "another_thing")
        self.assertIs(blueprint.entities[0], blueprint.entities["another_thing"])

        # Test key map removal on set to None
        blueprint.entities[0].id = None
        self.assertEqual(blueprint.entities[0].id, None)
        self.assertFalse("another_thing" in blueprint.entities)

    def test_set_position(self):
        group = Group("test")
        group.position = (10, 10)
        self.assertEqual(group.position, Vector(10.0, 10.0))
        group.position = {"x": 1.5, "y": 2.5}
        self.assertEqual(group.position, Vector(1.5, 2.5))

        blueprint = Blueprint()
        blueprint.entities.append(group)

        with self.assertRaises(DraftsmanError):
            blueprint.entities[0].position = (1, 1)

    def test_set_collision_mask(self):
        group = Group("test")
        group.collision_mask = {"entities", "something-else"}
        self.assertEqual(group.collision_mask, {"entities", "something-else"})
        group.collision_mask = None
        self.assertEqual(group.collision_mask, set())

        with self.assertRaises(TypeError):
            group.collision_mask = TypeError

    def test_set_tile_width(self):
        group = Group("test")
        group.tile_width = 10
        self.assertEqual(group.tile_width, 10)

        with self.assertRaises(TypeError):
            group.tile_width = TypeError

    def test_set_tile_height(self):
        group = Group("test")
        group.tile_height = 10
        self.assertEqual(group.tile_height, 10)

        with self.assertRaises(TypeError):
            group.tile_height = TypeError

    def test_set_entities(self):
        group = Group("test")
        # List case
        group.entities = [
            Furnace("stone-furnace"),
            Container("wooden-chest", tile_position=(4, 0)),
            ProgrammableSpeaker("programmable-speaker", tile_position=(8, 0)),
        ]
        self.assertIsInstance(group.entities, EntityList)
        # None case
        group.entities = None
        self.assertIsInstance(group.entities, EntityList)
        self.assertEqual(group.entities.data, [])
        # EntityList case
        group2 = Group("test2")
        group2.entities = group.entities
        self.assertIsInstance(group2.entities, EntityList)
        self.assertEqual(group2.entities.data, [])

        group.entities = [
            Furnace("stone-furnace"),
            Container("wooden-chest", tile_position=(4, 0)),
            ProgrammableSpeaker("programmable-speaker", tile_position=(8, 0)),
        ]
        group2.entities = group.entities
        self.assertIsInstance(group2.entities, EntityList)
        self.assertIsNot(group2.entities, group.entities)

        with self.assertRaises(TypeError):
            group2.entities = TypeError
        with self.assertRaises(TypeError):
            group2.entities = [TypeError]

    def test_insert_entity(self):
        group = Group("test")
        substation1 = ElectricPole("substation", id="A")
        substation2 = ElectricPole("substation", tile_position=(10, 10), id="B")
        power_switch = PowerSwitch("power-switch", tile_position=(5, 5), id="C")
        # substation1.add_power_connection(substation2)
        # substation2.add_circuit_connection("red", substation1)
        # power_switch.add_power_connection(substation2, 2)

        group.entities.append(substation1)
        group.entities.append(substation2)
        group.entities.append(power_switch)

        group.add_power_connection("A", "B")
        group.add_circuit_connection("red", "A", "B")
        group.add_power_connection("C", "B", 2)

        # Ensure that associations remain correct (global)
        self.assertEqual(
            group.entities[0].to_dict(),
            {
                "name": "substation",
                "position": {"x": 1.0, "y": 1.0},
                "neighbours": [Association(group.entities["B"])],
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities["B"])}]}
                },
            },
        )
        self.assertEqual(
            group.entities[1].to_dict(),
            {
                "name": "substation",
                "position": {"x": 11.0, "y": 11.0},
                "neighbours": [Association(group.entities["A"])],
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities["A"])}]},
                },
            },
        )
        self.assertEqual(
            group.entities[2].to_dict(),
            {
                "name": "power-switch",
                "position": {"x": 6.0, "y": 6.0},
                "connections": {
                    "Cu1": [
                        {"entity_id": Association(group.entities["B"]), "wire_id": 0}
                    ]
                },
            },
        )

        # Ensure that popping resolves associations in the returned entities

        with self.assertRaises(TypeError):
            group.entities.append(TypeError)

    def test_set_entity(self):
        group = Group("test")
        group.entities.append(Furnace(id="A"))
        self.assertIsInstance(group.entities["A"], Furnace)
        self.assertIs(group.entities["A"], group.entities[0])

        group.entities[0] = Container(id="B")
        self.assertIsInstance(group.entities[0], Container)
        self.assertIs(group.entities["B"], group.entities[0])

        with self.assertRaises(KeyError):
            group.entities["A"]

    def test_remove_entity(self):
        group = Group("test")
        container_1 = Container("steel-chest", id="A")
        container_2 = Container("steel-chest", tile_position=(3, 0), id="B")
        group.entities.append(container_1)
        group.entities.append(container_2)
        group.add_circuit_connection("red", "A", "B")

        self.assertEqual(
            group.entities[0].to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": 0.5, "y": 0.5},
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities[1])}]}
                },
            },
        )
        result = group.entities.pop()
        self.assertEqual(
            result.to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": 3.5, "y": 0.5},
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities[0])}]}
                },
            },
        )

    def test_power_connections(self):
        group = Group("test")
        substation1 = ElectricPole("substation", id="1")
        substation2 = ElectricPole("substation", id="2", tile_position=(2, 0))
        power_switch = PowerSwitch(id="p", tile_position=(4, 0))
        group.entities = [substation1, substation2, power_switch]

        # Normal operation
        group.add_power_connection("1", "2")
        self.assertEqual(
            group.entities["1"].neighbours, [Association(group.entities["2"])]
        )
        self.assertEqual(
            group.entities["2"].neighbours, [Association(group.entities["1"])]
        )
        # Inverse, but redundant case
        group.add_power_connection("2", "1")
        self.assertEqual(
            group.entities["1"].neighbours, [Association(group.entities["2"])]
        )
        self.assertEqual(
            group.entities["2"].neighbours, [Association(group.entities["1"])]
        )

        # Dual power connectable case
        group.add_power_connection("1", "p")
        self.assertEqual(
            group.entities["1"].neighbours, [Association(group.entities["2"])]
        )
        self.assertEqual(
            group.entities["p"].connections,
            {"Cu0": [{"entity_id": Association(group.entities["1"]), "wire_id": 0}]},
        )
        # Inverse, but redundant case
        group.add_power_connection("p", "1")
        self.assertEqual(
            group.entities["1"].neighbours, [Association(group.entities["2"])]
        )
        self.assertEqual(
            group.entities["p"].connections,
            {"Cu0": [{"entity_id": Association(group.entities["1"]), "wire_id": 0}]},
        )
        # Redundant case
        group.add_power_connection("2", "p")
        group.add_power_connection("2", "p")
        self.assertEqual(
            group.entities["2"].neighbours, [Association(group.entities["1"])]
        )
        self.assertEqual(
            group.entities["p"].connections,
            {
                "Cu0": [
                    {"entity_id": Association(group.entities["1"]), "wire_id": 0},
                    {"entity_id": Association(group.entities["2"]), "wire_id": 0},
                ]
            },
        )
        group.add_power_connection("p", "2", side=2)
        self.assertEqual(
            group.entities["p"].connections,
            {
                "Cu0": [
                    {"entity_id": Association(group.entities["1"]), "wire_id": 0},
                    {"entity_id": Association(group.entities["2"]), "wire_id": 0},
                ],
                "Cu1": [{"entity_id": Association(group.entities["2"]), "wire_id": 0}],
            },
        )

        # Warnings
        with self.assertWarns(ConnectionDistanceWarning):
            other = ElectricPole(position=[100, 0], id="other")
            group.entities.append(other)
            group.add_power_connection("1", "other")

        # Errors
        with self.assertRaises(EntityNotPowerConnectableError):
            group.entities.append(
                "transport-belt", id="whatever", tile_position=(10, 0)
            )
            group.add_power_connection("whatever", "2")

        with self.assertRaises(DraftsmanError):
            group.entities.append("power-switch", id="p2", tile_position=(0, 10))
            group.add_power_connection("p", "p2")

        # Make sure correct even after errors
        self.assertEqual(
            group.entities["1"].neighbours,
            [Association(group.entities["2"]), Association(group.entities["other"])],
        )
        self.assertEqual(
            group.entities["p"].connections,
            {
                "Cu0": [
                    {"entity_id": Association(group.entities["1"]), "wire_id": 0},
                    {"entity_id": Association(group.entities["2"]), "wire_id": 0},
                ],
                "Cu1": [{"entity_id": Association(group.entities["2"]), "wire_id": 0}],
            },
        )

        # Test removing
        # Redundant case
        group.remove_power_connection("1", "2")
        group.remove_power_connection("1", "2")
        self.assertEqual(
            group.entities["1"].neighbours, [Association(group.entities["other"])]
        )
        self.assertEqual(group.entities["2"].neighbours, [])

        # Remove power switch connection that does not exist
        group.remove_power_connection("1", "p")
        group.remove_power_connection("1", "p")
        self.assertEqual(
            group.entities["1"].neighbours, [Association(group.entities["other"])]
        )
        self.assertEqual(
            group.entities["p"].connections,
            {
                "Cu0": [{"entity_id": Association(group.entities["2"]), "wire_id": 0}],
                "Cu1": [{"entity_id": Association(group.entities["2"]), "wire_id": 0}],
            },
        )

        group.add_power_connection("1", "p")
        group.remove_power_connection("p", "2", side=1)
        group.remove_power_connection("p", "2", side=1)
        group.remove_power_connection("p", "1")
        group.remove_power_connection("p", "1")
        self.assertEqual(
            group.entities["p"].connections,
            {"Cu1": [{"entity_id": Association(group.entities["2"]), "wire_id": 0}]},
        )
        group.remove_power_connection("2", "p", 2)
        group.remove_power_connection("2", "p", 2)
        self.assertEqual(power_switch.connections, {})

        # TODO: test setting connection by reference

    def test_add_circuit_connection(self):
        group = Group("test")
        container1 = Container("steel-chest", id="c1", tile_position=[-1, 0])
        container2 = Container("steel-chest", id="c2", tile_position=[1, 0])
        group.entities.append(container1)
        group.entities.append(container2)

        group.add_circuit_connection("red", "c1", "c2")
        self.assertEqual(
            group.entities["c1"].to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": -0.5, "y": 0.5},
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities["c2"])}]}
                },
            },
        )
        self.assertEqual(
            group.entities["c2"].to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": 1.5, "y": 0.5},
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities["c1"])}]}
                },
            },
        )
        # Test duplicate connection
        group.add_circuit_connection("red", "c1", "c2")
        self.assertEqual(
            group.entities["c1"].to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": -0.5, "y": 0.5},
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities["c2"])}]}
                },
            },
        )
        self.assertEqual(
            group.entities["c2"].to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": 1.5, "y": 0.5},
                "connections": {
                    "1": {"red": [{"entity_id": Association(group.entities["c1"])}]}
                },
            },
        )

        # set_connections to None
        group.entities["c1"].connections = {}
        self.assertEqual(group.entities["c1"].connections, {})

        # Test when the same side and color dict already exists
        container3 = Container("wooden-chest", id="test")
        group.entities.append(container3)
        group.add_circuit_connection("red", "c2", "test")
        self.assertEqual(
            group.entities["c2"].to_dict(),
            {
                "name": "steel-chest",
                "position": {"x": 1.5, "y": 0.5},
                "connections": {
                    "1": {
                        "red": [
                            {"entity_id": Association(group.entities["c1"])},
                            {"entity_id": Association(group.entities["test"])},
                        ]
                    }
                },
            },
        )

        # Test multiple connection points
        group2 = Group("test2")
        arithmetic_combinator = ArithmeticCombinator(id="a")
        decider_combinator = DeciderCombinator(id="d", tile_position=(1, 0))
        group2.entities.append(arithmetic_combinator)
        group2.entities.append(decider_combinator)

        group2.add_circuit_connection("green", "a", "a", 1, 2)
        group2.add_circuit_connection("red", "d", "a", 1, 2)
        self.assertEqual(
            group2.entities["a"].connections,
            {
                "1": {
                    "green": [
                        {
                            "entity_id": Association(group2.entities["a"]),
                            "circuit_id": 2,
                        }
                    ]
                },
                "2": {
                    "green": [
                        {
                            "entity_id": Association(group2.entities["a"]),
                            "circuit_id": 1,
                        }
                    ],
                    "red": [
                        {
                            "entity_id": Association(group2.entities["d"]),
                            "circuit_id": 1,
                        }
                    ],
                },
            },
        )
        self.assertEqual(
            group2.entities["d"].connections,
            {
                "1": {
                    "red": [
                        {
                            "entity_id": Association(group2.entities["a"]),
                            "circuit_id": 2,
                        }
                    ]
                }
            },
        )

        # Warnings
        # Warn if source or target side is not 1 on entity that is not dual
        # connectable
        with self.assertWarns(ConnectionSideWarning):
            group.add_circuit_connection("green", "c1", "c2", 1, 2)
        with self.assertWarns(ConnectionSideWarning):
            group.add_circuit_connection("green", "c1", "c2", 2, 1)
        # Warn if connection being made is over too long a distance
        with self.assertWarns(ConnectionDistanceWarning):
            group.entities.append("wooden-chest", tile_position=(100, 100))
            group.add_circuit_connection("green", "c2", -1)

        # Errors
        with self.assertRaises(InvalidWireTypeError):
            group.add_circuit_connection("wrong", "c1", "c2")

        with self.assertRaises(KeyError):
            group.add_circuit_connection("red", KeyError, "c2")
        with self.assertRaises(KeyError):
            group.add_circuit_connection("red", "c1", KeyError)

        # with self.assertRaises(ValueError):
        #     container_with_no_id = Container()
        #     container1.add_circuit_connection("red", container_with_no_id)

        with self.assertRaises(InvalidConnectionSideError):
            group.add_circuit_connection("red", "c1", "c2", "fish", 2)
        with self.assertRaises(InvalidConnectionSideError):
            group.add_circuit_connection("red", "c1", "c2", 2, "fish")

        with self.assertRaises(EntityNotCircuitConnectableError):
            not_circuit_connectable = Splitter(
                "fast-splitter", id="no error pls", tile_position=(0, 5)
            )
            group.entities.append(not_circuit_connectable)
            group.add_circuit_connection("red", "c1", "no error pls")

        # TODO: test setting connection by reference

    def test_remove_circuit_connection(self):
        group = Group("test")
        container1 = Container("wooden-chest", id="testing1", tile_position=[0, 0])
        container2 = Container("wooden-chest", id="testing2", tile_position=[1, 0])
        group.entities = [container1, container2]

        # Null case
        group.remove_circuit_connection("red", "testing1", "testing2")
        self.assertEqual(
            container1.to_dict(),
            {
                "name": "wooden-chest",
                "position": {"x": 0.5, "y": 0.5},
            },
        )
        self.assertEqual(
            container2.to_dict(),
            {
                "name": "wooden-chest",
                "position": {"x": 1.5, "y": 0.5},
            },
        )

        # Normal Operation
        group.add_circuit_connection("red", "testing1", "testing2")
        group.add_circuit_connection("green", "testing2", "testing1")
        group.remove_circuit_connection("red", "testing1", "testing2")
        self.assertEqual(
            group.entities["testing1"].to_dict(),
            {
                "name": "wooden-chest",
                "position": {"x": 0.5, "y": 0.5},
                "connections": {
                    "1": {
                        "green": [
                            {"entity_id": Association(group.entities["testing2"])}
                        ]
                    }
                },
            },
        )
        self.assertEqual(
            group.entities["testing2"].to_dict(),
            {
                "name": "wooden-chest",
                "position": {"x": 1.5, "y": 0.5},
                "connections": {
                    "1": {
                        "green": [
                            {"entity_id": Association(group.entities["testing1"])}
                        ]
                    }
                },
            },
        )

        # Redundant operation
        group.remove_circuit_connection("red", "testing1", "testing1")
        self.assertEqual(
            group.entities["testing1"].to_dict(),
            {
                "name": "wooden-chest",
                "position": {"x": 0.5, "y": 0.5},
                "connections": {
                    "1": {
                        "green": [
                            {"entity_id": Association(group.entities["testing2"])}
                        ]
                    }
                },
            },
        )
        # Test multiple connection points
        group2 = Group("test")
        arithmetic_combinator = ArithmeticCombinator(id="a")
        decider_combinator = DeciderCombinator(id="d", tile_position=(1, 0))
        constant_combinator = ConstantCombinator(id="c", tile_position=(2, 0))
        group2.entities = [
            arithmetic_combinator,
            decider_combinator,
            constant_combinator,
        ]

        group2.add_circuit_connection("green", "a", "d")
        group2.add_circuit_connection("green", "a", "d", 1, 2)
        group2.add_circuit_connection("green", "a", "a", 1, 2)
        group2.add_circuit_connection("red", "a", "d", 2, 1)
        group2.add_circuit_connection("red", "a", "d", 2, 2)
        group2.add_circuit_connection("red", "c", "d", 1, 2)

        group2.remove_circuit_connection("green", "a", "d")
        group2.remove_circuit_connection("green", "a", "d", 1, 2)
        group2.remove_circuit_connection("green", "a", "a", 1, 2)
        group2.remove_circuit_connection("red", "a", "d", 2, 1)
        group2.remove_circuit_connection("red", "a", "d", 2, 2)

        self.assertEqual(group2.entities["a"].connections, {})
        self.assertEqual(
            group2.entities["d"].connections,
            {"2": {"red": [{"entity_id": Association(group2.entities["c"])}]}},
        )
        self.assertEqual(
            group2.entities["c"].connections,
            {
                "1": {
                    "red": [
                        {
                            "entity_id": Association(group2.entities["d"]),
                            "circuit_id": 2,
                        }
                    ]
                }
            },
        )

        # Errors
        with self.assertRaises(InvalidWireTypeError):
            group.remove_circuit_connection("wrong", "testing1", "testing2")

        with self.assertRaises(KeyError):
            group.remove_circuit_connection("red", KeyError, "testing2")
        with self.assertRaises(KeyError):
            group.remove_circuit_connection("red", "testing1", KeyError)

        with self.assertRaises(InvalidConnectionSideError):
            group.remove_circuit_connection("red", "testing1", "testing2", "fish", 2)
        with self.assertRaises(InvalidConnectionSideError):
            group.remove_circuit_connection("red", "testing2", "testing1", 2, "fish")

        # TODO: test setting connection by reference

    def test_global_position(self):
        group = Group("test")
        group.entities.append("transport-belt")
        self.assertEqual(group.position, Vector(0, 0))
        self.assertEqual(group.position.to_dict(), {"x": 0, "y": 0})
        self.assertEqual(group.entities[0].position, Vector(0.5, 0.5))
        self.assertEqual(group.entities[0].position.to_dict(), {"x": 0.5, "y": 0.5})
        self.assertEqual(group.entities[0].global_position, Vector(0.5, 0.5))
        self.assertEqual(
            group.entities[0].global_position.to_dict(), {"x": 0.5, "y": 0.5}
        )
        group.position = (4, 4)
        self.assertEqual(group.position, Vector(4, 4))
        self.assertEqual(group.entities[0].position, Vector(0.5, 0.5))
        self.assertEqual(group.entities[0].global_position, Vector(4.5, 4.5))

    def test_get_world_bounding_box(self):
        group = Group("test")
        group.entities.append("transport-belt")
        group.entities.append("transport-belt", tile_position=(5, 5))
        bounding_box = group.get_world_bounding_box()
        self.assertAlmostEqual(bounding_box.top_left[0], 0.1)
        self.assertAlmostEqual(bounding_box.top_left[1], 0.1)
        self.assertAlmostEqual(bounding_box.bot_right[0], 5.9)
        self.assertAlmostEqual(bounding_box.bot_right[1], 5.9)
        group.entities.pop()
        group.position = (3, 3)
        bounding_box = group.get_world_bounding_box()
        self.assertAlmostEqual(bounding_box.top_left[0], 3.1)
        self.assertAlmostEqual(bounding_box.top_left[1], 3.1)
        self.assertAlmostEqual(bounding_box.bot_right[0], 3.9)
        self.assertAlmostEqual(bounding_box.bot_right[1], 3.9)
        group.entities.pop()
        bounding_box = group.get_world_bounding_box()
        self.assertEqual(group.collision_set, CollisionSet([]))
        self.assertAlmostEqual(bounding_box, None)

    def test_entity_overlapping(self):
        group = Group("test")
        group.entities.append("transport-belt")
        # 2 entities in the same Group
        with self.assertWarns(OverlappingObjectsWarning):
            group.entities.append("transport-belt")
        group.entities.pop()  # Remove the extra transport belt

        # Group in Blueprint
        blueprint = Blueprint()
        blueprint.entities.append("transport-belt")

        with self.assertWarns(OverlappingObjectsWarning):
            blueprint.entities.append(group)
        blueprint.entities.pop()

        # Group in Group
        group2 = Group("test2")
        group2.entities.append("transport-belt")
        with self.assertWarns(OverlappingObjectsWarning):
            group.entities.append(group2)

        # Group in Group in Blueprint
        with self.assertWarns(OverlappingObjectsWarning):
            blueprint.entities.append(group)

    def test_double_grid_aligned(self):
        group = Group("test")
        group.entities.append("transport-belt")
        self.assertEqual(group.double_grid_aligned, False)

        group.entities.append("straight-rail", tile_position=(2, 0))
        self.assertEqual(group.double_grid_aligned, True)

    def test_rotatable(self):
        group = Group("test")
        self.assertEqual(group.rotatable, True)

    def test_flippable(self):
        group = Group("test")
        group.entities.append("transport-belt")
        self.assertEqual(group.flippable, True)

        # TODO
        # group.entities.append("pumpjack", tile_position = (10, 10))
        # self.assertEqual(group.flippable, False)

    def test_mergable_with(self):
        group1 = Group()
        group2 = Group()
        self.assertFalse(group1.mergable_with(group2))  # Always false

    def test_merge(self):
        # Test group merging
        group1 = Group()
        group2 = Group()
        group1.merge(group2)  # Should do nothing

        # Test subentity merging
        group = Group()
        group.entities.append("accumulator")
        group.entities.append("accumulator", merge=True)
        self.assertEqual(len(group.entities), 1)
        self.assertEqual(
            group.entities[0].to_dict(),
            {"name": "accumulator", "position": {"x": 1.0, "y": 1.0}},
        )

        # Single entity in group overlap case
        blueprint = Blueprint()
        group = Group()
        group.entities.append("accumulator")
        blueprint.entities.append(group)

        self.assertEqual(len(group.entities), 1)
        self.assertEqual(group.entities.data, [group.entities[0]])
        self.assertEqual(len(blueprint.entities), 1)
        self.assertEqual(blueprint.entities.data, [blueprint.entities[0]])
        self.assertEqual(
            blueprint.to_dict()["blueprint"],
            {
                "item": "blueprint",
                "entities": [
                    {
                        "entity_number": 1,
                        "name": "accumulator",
                        "position": {"x": 1.0, "y": 1.0},
                    }
                ],
                "version": encode_version(*__factorio_version_info__),
            },
        )

        blueprint.entities.append(group, merge=True)
        self.assertEqual(len(blueprint.entities), 2)
        self.assertEqual(
            blueprint.area, AABB(0.09999999999999998, 0.09999999999999998, 1.9, 1.9)
        )
        self.assertIsInstance(blueprint.entities[0], Group)
        self.assertEqual(len(blueprint.entities[0].entities), 1)
        self.assertEqual(
            blueprint.entities[0].get_world_bounding_box(),
            AABB(0.09999999999999998, 0.09999999999999998, 1.9, 1.9),
        )
        self.assertIsInstance(blueprint.entities[1], Group)
        self.assertEqual(len(blueprint.entities[1].entities), 0)
        self.assertEqual(blueprint.entities[1].get_world_bounding_box(), None)

        self.assertEqual(
            blueprint.to_dict()["blueprint"],
            {
                "item": "blueprint",
                "entities": [
                    {
                        "entity_number": 1,
                        "name": "accumulator",
                        "position": {"x": 1.0, "y": 1.0},
                    }
                ],
                "version": encode_version(*__factorio_version_info__),
            },
        )

    def test_get(self):
        # Regular case
        # TODO

        # Nested group case
        subgroup = Group("subgroup")
        subgroup.entities.append("express-transport-belt", id="test")
        group = Group("parent")
        group.entities.append(subgroup)
        self.assertEqual(group.get(), [group.entities[("subgroup", "test")]])
        # Note that this messes with the entities position afterward:
        # this is prevented in Blueprint.to_dict by making a copy of itself and
        # using that instead of the original data

    def test_deepcopy(self):
        group = Group()
        group.entities.append("wooden-chest")
        group.entities.append("inserter", tile_position=(0, 1))
        group.entities.append("small-electric-pole", tile_position=(1, 0))
        group.add_circuit_connection("red", 0, 1)
        group.entities.append("power-switch", tile_position=(1, 1))
        group.add_power_connection(2, 3, side=1)

        blueprint = Blueprint()
        blueprint.entities.append(group, copy=False)

        # Make sure entities' parents are correct
        self.assertIs(group.entities[0].parent, group)
        self.assertIs(group.entities[1].parent, group)
        self.assertIs(group.entities[2].parent, group)
        # Make sure connections are preserved
        self.assertIs(
            group.entities[0].connections["1"]["red"][0]["entity_id"](),
            group.entities[1],
        )
        self.assertIs(
            group.entities[1].connections["1"]["red"][0]["entity_id"](),
            group.entities[0],
        )
        self.assertIs(
            group.entities[3].connections["Cu0"][0]["entity_id"](), group.entities[2]
        )
        # Make sure the parent is correct
        self.assertIs(group.parent, blueprint)

        import copy

        group_copy = copy.deepcopy(group)

        # Make sure entities' parents are correct
        self.assertIs(group_copy.entities[0].parent, group_copy)
        self.assertIs(group_copy.entities[1].parent, group_copy)
        self.assertIs(group_copy.entities[2].parent, group_copy)
        # Make sure connections are preserved
        self.assertIs(
            group_copy.entities[0].connections["1"]["red"][0]["entity_id"](),
            group_copy.entities[1],
        )
        self.assertIs(
            group_copy.entities[1].connections["1"]["red"][0]["entity_id"](),
            group_copy.entities[0],
        )
        self.assertIs(
            group_copy.entities[3].connections["Cu0"][0]["entity_id"](),
            group_copy.entities[2],
        )
        # Make sure parent of the copied group is reset to None
        self.assertIs(group_copy.parent, None)
        # Make sure the hashmap was copied properly and are not equivalent
        self.assertIsNot(group.entity_map, group_copy.entity_map)

        # Test invalid association
        blueprint.entities.append("steel-chest", tile_position=(5, 5))
        blueprint.add_circuit_connection("red", (0, 1), 1)
        with self.assertRaises(InvalidAssociationError):
            copy.deepcopy(group)

    def test_with_blueprint(self):
        blueprint = Blueprint()
        blueprint.entities.append("inserter")

        group = Group("test")
        group.entities.append("inserter", tile_position=(1, 1))
        group2 = Group("test2")
        group2.entities.append(group)
        blueprint.entities.append(group2)

        blueprint.add_circuit_connection("red", 0, ("test2", "test", 0))
        self.maxDiff = None
        self.assertEqual(
            blueprint.to_dict(),
            {
                "blueprint": {
                    "item": "blueprint",
                    "entities": [
                        {
                            "name": "inserter",
                            "position": {"x": 0.5, "y": 0.5},
                            "connections": {"1": {"red": [{"entity_id": 2}]}},
                            "entity_number": 1,
                        },
                        {
                            "name": "inserter",
                            "position": {"x": 1.5, "y": 1.5},
                            "connections": {"1": {"red": [{"entity_id": 1}]}},
                            "entity_number": 2,
                        },
                    ],
                    "version": encode_version(*__factorio_version_info__),
                }
            },
        )

    # =========================================================================

    def test_translate(self):
        group = Group("test")
        group.entities.append("wooden-chest", tile_position=(10, 10))

        group.translate(-5, -5)

        self.assertEqual(group.entities[0].tile_position, Vector(5, 5))

        group.entities.append("straight-rail")
        self.assertEqual(group.double_grid_aligned, True)

        with self.assertWarns(RailAlignmentWarning):
            group.translate(1, 1)

    def test_rotate(self):
        group = Group("test")
        group.entities.append("wooden-chest")
        group.entities.append("wooden-chest", tile_position=(4, 4))
        group.entities.append("boiler", tile_position=(1, 1))  # looking North

        group.rotate(2)

        self.assertEqual(group.entities[0].tile_position, Vector(-1, 0))
        self.assertEqual(group.entities[1].tile_position, Vector(-5, 4))
        self.assertEqual(group.entities[2].tile_position, Vector(-3, 1))
        self.assertEqual(group.entities[2].direction, 2)

        with self.assertRaises(RotationError):
            group.rotate(1)

    def test_flip(self):
        group = Group("test")
        group.entities.append("wooden-chest")
        group.entities.append("wooden-chest", tile_position=(4, 4))
        group.entities.append("boiler", tile_position=(1, 1))  # looking North

        group.flip()  # horizontal

        self.assertEqual(group.entities[0].tile_position, Vector(-1, 0))
        self.assertEqual(group.entities[1].tile_position, Vector(-5, 4))
        self.assertEqual(group.entities[2].tile_position, Vector(-4, 1))
        self.assertEqual(group.entities[2].direction, 0)

        group.flip("vertical")

        self.assertEqual(group.entities[0].tile_position, Vector(-1, -1))
        self.assertEqual(group.entities[1].tile_position, Vector(-5, -5))
        self.assertEqual(group.entities[2].tile_position, Vector(-4, -3))
        self.assertEqual(group.entities[2].direction, 4)

        with self.assertRaises(ValueError):
            group.flip("incorrectly")
