import os

class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'data/uploads'
    S3_BUCKET = 'your-master-audio-bucket'
    DATABASE_PATH = 'data/index.db'
