import unittest
from easy_spreadsheet import Cell, Row, Rows


class TestRows(unittest.TestCase):
    def setUp(self) -> None:
        cellA1 = Cell(value="test", col_pos="A", row_pos="1")
        cellB1 = Cell(value="test", col_pos="B", row_pos="1")
        cellA2 = Cell(value=50, col_pos="A", row_pos="2")
        cellB2 = Cell(value=50, col_pos="B", row_pos="2")

        row = Row(
            cells=[cellA1, cellB1], col_start_pos="A", col_end_pos="B", row_pos="1"
        )
        row2 = Row(
            cells=[cellA2, cellB2], col_start_pos="A", col_end_pos="B", row_pos="2"
        )
        self.rows = Rows(rows=[row, row2])

        return super().setUp()

    def test_value(self):
        cellA1 = Cell(value="test", col_pos="A", row_pos="1")
        cellB1 = Cell(value="test", col_pos="B", row_pos="1")
        cellA2 = Cell(value=50, col_pos="A", row_pos="2")
        cellB2 = Cell(value=50, col_pos="B", row_pos="2")

        row = Row(
            cells=[cellA1, cellB1], col_start_pos="A", col_end_pos="B", row_pos="1"
        )
        row2 = Row(
            cells=[cellA2, cellB2], col_start_pos="A", col_end_pos="B", row_pos="2"
        )

        self.assertEqual(self.rows.rows, [row, row2])


if __name__ == "__main__":
    unittest.main()
