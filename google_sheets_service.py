#Form Data Automation (Task 3)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.config import Config
from app.utils.logger import log
import traceback

class GoogleSheetsService:
    def __init__(self):
        self.scope = Config.GOOGLE_SHEETS_SCOPE
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            Config.GOOGLE_SHEETS_CREDENTIALS, self.scope
        )
        self.sheet_id = Config.GOOGLE_SHEETS_ID
        self.client = gspread.authorize(self.credentials)
    
    def append_application(self, application_data):
        try:
            sheet = self.client.open_by_key(self.sheet_id).sheet1
            row = [
                application_data['applicant_name'],
                application_data['email'],
                application_data['phone'],
                application_data['university'],
                application_data['major'],
                application_data['graduation_year'],
                application_data['domain'],
                application_data['start_date'],
                application_data['end_date'],
                application_data['duration_weeks'],
                application_data['status'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            sheet.append_row(row)
            log.info(f"Application data synced to Google Sheets: {application_data['email']}")
            return True
        except Exception as e:
            log.error(f"Error syncing to Google Sheets: {str(e)}\n{traceback.format_exc()}")
            return False