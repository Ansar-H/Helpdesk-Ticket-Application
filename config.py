import os
from dotenv import load_dotenv

# To load environment variables form .env file
load_dotenv()

class Config:
    # Secret key for session management
    SECRET_KEY ='dev-secret-key'

    # I am using an SQLite database due to it being a small application
    SQLALCHEMY_DATABASE_URI = 'sqlite:///helpdesk.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    