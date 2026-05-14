import os
from dotenv import load_dotenv

load_dotenv()

# Detect Vercel serverless environment
_on_vercel = bool(os.environ.get('VERCEL'))

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')

    # Gemini AI
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

    # Database — use /tmp on Vercel (ephemeral), local file otherwise
    _db_default = 'sqlite:////tmp/resumes.db' if _on_vercel else 'sqlite:///resumes.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', _db_default)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload — /tmp is the only writable dir on Vercel serverless
    UPLOAD_FOLDER = '/tmp' if _on_vercel else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

    # CORS – comma-separated origins in env var
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
