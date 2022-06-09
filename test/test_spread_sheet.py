import unittest
from easy_spreadsheet import Cell, Row, Rows, SpreadSheed


class TestSpreadSheet(unittest.TestCase):
    def setUp(self) -> None:
        cellA1 = Cell(value="header1", col_pos="A", row_pos="1")
        cellB1 = Cell(value="header2", col_pos="B", row_pos="1")
        cellA2 = Cell(value=50, col_pos="A", row_pos="2")
        cellB2 = Cell(value=50, col_pos="B", row_pos="2")
        cellA3 = Cell(value=50, col_pos="A", row_pos="3")
        cellB3 = Cell(value=50, col_pos="B", row_pos="3")

        header = Row(
            cells=[cellA1, cellB1], col_start_pos="A", col_end_pos="B", row_pos="1"
        )
        row1 = Row(
            cells=[cellA2, cellB2], col_start_pos="A", col_end_pos="B", row_pos="2"
        )
        row2 = Row(
            cells=[cellA3, cellB3], col_start_pos="A", col_end_pos="B", row_pos="3"
        )
        rows = Rows(rows=[row1, row2])

        self.spread_sheet = SpreadSheed(header_row=header, body_rows=rows)
        return super().setUp()

    def test_value(self):
        print(self.spread_sheet.body())


if __name__ == "__main__":
    unittest.main()
