import os
from dotenv import load_dotenv
from pathlib import Path


BASE_PATH = Path(__file__).resolve(strict=True).parent.parent  # strict=True makes it an absolute path
ENV_PATH = BASE_PATH /'.env'
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = None


class TestConfig(Config):
    CLIENT_ID: str = os.environ.get('CLIENT_ID')
    CLIENT_SECRET: str = os.environ.get('CLIENT_SECRET')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:memory//'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

