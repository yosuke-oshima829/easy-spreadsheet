import unittest
from easy_spreadsheet import Cell


class TestCell(unittest.TestCase):
    def setUp(self) -> None:
        self.str_cell = Cell(value="test", col_pos="A", row_pos="1")
        self.int_cell = Cell(value=50, col_pos="B", row_pos="2")
        return super().setUp()

    def test_value(self):
        self.assertEqual(self.str_cell.value, "test")
        self.assertEqual(self.int_cell.value, 50)

    def test_value_type(self):
        self.assertEqual(type(self.str_cell.value), str)
        self.assertEqual(type(self.int_cell.value), int)

    def test_col_pos(self):
        self.assertEqual(self.str_cell.col_pos, "A")
        self.assertEqual(self.int_cell.col_pos, "B")

    def test_row_pos(self):
        self.assertEqual(self.str_cell.row_pos, "1")
        self.assertEqual(self.int_cell.row_pos, "2")


if __name__ == "__main__":
    unittest.main()
