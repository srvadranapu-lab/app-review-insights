import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
