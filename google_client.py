import pathlib
from typing import Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSpreadsheetClient:
    # If modifying these scopes, delete the file coin.json.

    def __init__(self, spreadsheet_id: str, scopes: list | str) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.scopes = scopes if isinstance(scopes, list) else [scopes]
        self._credentials = None

    @property
    def credentials(self) -> Any:
        if not self._credentials or not self._credentials.valid:
            self._credentials = self._google_sheets_auth()
        return self._credentials

    @property
    def service(self) -> Any:
        return build("sheets", "v4", credentials=self.credentials)

    def _google_sheets_auth(self) -> Any:
        creds = None
        if pathlib.Path("coin.json").exists:
            creds = Credentials.from_authorized_user_file("coin.json", self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=3090)
            with open("coin.json", "w") as coin:
                coin.write(creds.to_json())
        return creds

    def read_spreadsheet(
        self,
        range: str,
        print_result: bool = False,
    ) -> list:
        result = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range=range,
            )
            .execute()
        )
        rows = result.get("values", [])
        if print_result:
            for row in rows:
                print(row[0])
        return rows

    def update_spreadsheet(
        self,
        range: str,
        values: list[list],
    ) -> None:
        payload = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": range,
                    "values": values,
                }
            ],
        }

        print(payload)

        self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=payload,
        ).execute()
