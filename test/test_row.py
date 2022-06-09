import unittest
from easy_spreadsheet import Cell, Row


class TestRow(unittest.TestCase):
    def setUp(self) -> None:
        cellA1 = Cell(value="test", col_pos="A", row_pos="1")
        cellB1 = Cell(value="test", col_pos="B", row_pos="1")
        self.row = Row(
            cells=[cellA1, cellB1], col_start_pos="A", col_end_pos="B", row_pos="1"
        )
        return super().setUp()

    def test_cells(self):
        cellA1 = Cell(value="test", col_pos="A", row_pos="1")
        cellB1 = Cell(value="test", col_pos="B", row_pos="1")

        self.assertEqual(self.row.cells, [cellA1, cellB1])

    def test_col_start_pos(self):
        self.assertEqual(self.row.col_start_pos, "A")

    def test_col_end_pos(self):
        self.assertEqual(self.row.col_end_pos, "B")

    def test_row_pos(self):
        self.assertEqual(self.row.row_pos, "1")


if __name__ == "__main__":
    unittest.main()
