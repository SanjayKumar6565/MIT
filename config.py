#Configuration
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mit_internship.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_SHEETS_CREDENTIALS = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    GOOGLE_SHEETS_SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    GOOGLE_SHEETS_ID = 'your-google-sheet-id'