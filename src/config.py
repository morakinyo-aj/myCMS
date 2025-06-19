import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    ALLOWED_EXTENSIONS = {'mp4', 'mov', 'jpg', 'jpeg', 'png'}
    MAX_FILE_SIZE = 100 * 1024 * 1024
    VIDEODB_API_KEY = os.environ['VIDEODB_API_KEY']