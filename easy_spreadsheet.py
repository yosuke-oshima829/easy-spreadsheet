from dataclasses import dataclass
import re
import string
from typing import Any, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
COLUMN_PATTERN = r"[A-Z]{1,}"
ROW_PATTERN = r"[0-9]{1,}"


@dataclass
class Cell:
    ###
    # col_pos: A, B, C, ..., AA, AB, AC
    # row_pos: 1, 2, 3, ...
    ###
    value: Any
    col_pos: str
    row_pos: str

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.col_pos == other.col_pos and self.row_pos == other.row_pos


@dataclass
class Row:
    ###
    # col_start_pos: A, B, C, ..., AA, AB, AC
    # col_end_pos: X, Y, Z, ..., AX, AY, AZ
    # row_pos: 1, 2, 3, ...
    ###
    cells: List[Cell]
    col_start_pos: str
    col_end_pos: str
    row_pos: str

    def __getitem__(self, i: int):
        return self.cells[i]


@dataclass
class Rows:
    rows: List[Row]

    def __getitem__(self, i: int):
        return self.rows[i]


@dataclass
class BodyRow:
    header_row: Row
    body_row: Row

    def hoge():
        zip()

    def __iter__(self):
        ...


@dataclass
class Body:
    header_row: Row
    body_rows: Rows

    def __getitem__(self, i: int):
        return BodyRow(self.header_row, self.body_rows[i])


@dataclass
class SpreadSheed:
    header_row: Row
    body_rows: Rows

    def body(self):
        return Body(header_row=self.header_row, body_rows=self.body_rows)


@dataclass
class SpreadSheetService:
    token: dict

    def get_credential(self):
        creds = None
        if self.token is not None:
            creds = Credentials.from_authorized_user_info(
                {
                    "refresh_token": self.token["refresh_token"],
                    "client_id": self.token["client_id"],
                    "client_secret": self.token["client_secret"],
                },
                SCOPES,
            )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        return creds

    def get_spreadsheets_service(self):
        return build("sheets", "v4", credentials=get_credential())


def get_credential(token: dict):
    creds = None
    if token is not None:
        creds = Credentials.from_authorized_user_info(
            {
                "refresh_token": token["refresh_token"],
                "client_id": token["client_id"],
                "client_secret": token["client_secret"],
            },
            SCOPES,
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    return creds


def get_spreadsheets_service():
    return build("sheets", "v4", credentials=get_credential())


def read_batch_spread_sheet(file_id: str, ranges: list):
    spreadsheets_service = get_spreadsheets_service()
    result = (
        spreadsheets_service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=file_id, ranges=ranges, majorDimension="ROWS")
        .execute()
    )
    ranges = result.get("valueRanges", [])
    sheet_rows = []
    if ranges and ranges[0]:
        sheet_rows = ranges[0].get("values", [])

    return sheet_rows


def read_spread_sheet(file_id: str, range: str):
    spreadsheets_service = get_spreadsheets_service()
    result = (
        spreadsheets_service.spreadsheets()
        .values()
        .get(spreadsheetId=file_id, range=range, majorDimension="ROWS")
        .execute()
    )
    range = result.get("range", "")
    values = result.get("values", [])

    return {"range": range, "values": values}


def append_spread_sheet(file_id: str, range: str, data_list: list):
    spreadsheets_service = get_spreadsheets_service()
    resource = {"majorDimension": "ROWS", "values": data_list}
    response = (
        spreadsheets_service.spreadsheets()
        .values()
        .append(
            spreadsheetId=file_id,
            range=range,
            insertDataOption="INSERT_ROWS",
            body=resource,
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )

    return response


def update_spread_sheet(file_id: str, data_list: list):
    spreadsheets_service = get_spreadsheets_service()
    resource = {"valueInputOption": "USER_ENTERED", "data": data_list}
    response = (
        spreadsheets_service.spreadsheets()
        .values()
        .batchUpdate(spreadsheetId=file_id, body=resource)
        .execute()
    )

    return response


def read_header(file_id: str, sheet_page: str):
    result = read_spread_sheet(file_id, f"{sheet_page}!1:1")
    headers = result.get("values")[0]

    range_info = split_range(result.get("range"))
    used_cols = []
    for alphabet in string.ascii_uppercase:
        used_cols.append(alphabet)
        if range_info["end_col"] == alphabet:
            break

    return {**range_info, "headers": dict(zip(headers, used_cols))}


def read_body(file_id: str, cell_range: str, body_start_row: int):
    result = read_spread_sheet(file_id, cell_range)
    body = result.get("values")[body_start_row - 1 :]
    return {"range": result.get("range"), "body": body}


def split_range(range: str) -> dict:
    sheet_page = range.split("!")[0]
    begin = range.split("!")[1].split(":")[0]
    begin_col = re.search(COLUMN_PATTERN, begin).group()
    begin_row = re.search(ROW_PATTERN, begin).group()

    end = range.split("!")[1].split(":")[1]
    end_col = re.search(COLUMN_PATTERN, end).group()
    end_row = re.search(ROW_PATTERN, end).group()

    return {
        "sheet_page": sheet_page,
        "begin_col": begin_col,
        "begin_row": begin_row,
        "end_col": end_col,
        "end_row": end_row,
    }
