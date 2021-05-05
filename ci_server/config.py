import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

BASE_PATH = (
    Path(__file__).resolve(strict=True).parent.parent
)  # strict=True makes it an absolute path
ENV_PATH = BASE_PATH / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: Optional[bool] = None


class TestConfig(Config):
    CLIENT_ID: Optional[str] = os.environ.get("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = os.environ.get("CLIENT_SECRET")
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:memory//"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = "constantinople"
