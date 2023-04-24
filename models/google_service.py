from typing import List

from google.oauth2 import service_account
from googleapiclient.discovery import build

from settings import GOOGLE_CREDENTIAL


class GoogleSheetService:
    def __init__(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_info(
            GOOGLE_CREDENTIAL, scopes=scope
        )
        self.service = build('sheets', 'v4', credentials=creds)

    def upsert_rows(self, spreadsheet_id: str, sheet_range: str, rows: List[List[str]], to_append: bool = False) -> int:
        '''
        Insert or update rows to a sheet

        Args:
            spreadsheet_id: ID of the sheet
            sheet_range: Range of the sheet in the format 'Sheet1!A1:B2'
            rows: List of rows to insert or update

        Returns:
            Number of updated rows
        '''

        if to_append:
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_range,
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body={'values': rows},
                )
                .execute()
            )
            return result['updates'].get('updatedRows', 0)
        
        else:
            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_range,
                    valueInputOption='USER_ENTERED',
                    body={'values': rows},
                )
                .execute()
            )

            return result.get('updatedCells', 0)
