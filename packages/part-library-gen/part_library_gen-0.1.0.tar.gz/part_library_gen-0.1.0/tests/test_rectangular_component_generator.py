import unittest
from src.part_library_gen.generators.rectangular_symbol_generator import rectangular_symbol_generator


class TestRectangularComponentGenerator(unittest.TestCase):
    def test_symbol_generation(self):
        symbol_dict = {
            "designator": "U?",
            "manufacturer": "Test Manufacturer Name",
            "part": "Test Part Name",
            "pins": {
                "la": {"no": 1, "func": "In", "desc": "ddl"},
                "ba": {"no": 2, "func": "InAnalog", "desc": "ddl"},
                "da": {"no": 3, "func": "InDigital", "desc": "ddl"},
                "cc": {"no": 4, "func": "Out", "desc": "ddl"}
            }
        }
        generator_data = {
            "left_side": ["la", "ba", "da"],
            "right_side": ["cc"]
        }
        generated_symbol = rectangular_symbol_generator(symbol_dict, generator_data)

        self.assertEqual(generated_symbol.designator.designator, "U?")
        self.assertEqual(generated_symbol.part_number.text, "Test Part Name")
        self.assertEqual(len(generated_symbol.pins), 4)

        self.assertEqual(generated_symbol.pins[0].name, 'la')
        self.assertEqual(generated_symbol.pins[1].name, 'ba')
        self.assertEqual(generated_symbol.pins[2].name, 'da')
        self.assertEqual(generated_symbol.pins[3].name, 'cc')

        self.assertEqual(generated_symbol.pins[0].number, 1)
        self.assertEqual(generated_symbol.pins[1].number, 2)
        self.assertEqual(generated_symbol.pins[2].number, 3)
        self.assertEqual(generated_symbol.pins[3].number, 4)

        self.assertEqual(generated_symbol.pins[0].function, 'In')
        self.assertEqual(generated_symbol.pins[1].function, 'InAnalog')
        self.assertEqual(generated_symbol.pins[2].function, 'InDigital')
        self.assertEqual(generated_symbol.pins[3].function, 'Out')
