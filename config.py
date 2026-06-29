import os
from dotenv import load_dotenv
 
load_dotenv()
 
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")