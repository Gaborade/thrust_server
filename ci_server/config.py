import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

from ci_server import app

if app.debug:
    BASE_PATH = (
        Path(__file__).resolve(strict=True).parent.parent
    )  # strict=True makes it an absolute path
    ENV_PATH = BASE_PATH / ".env"
    load_dotenv(dotenv_path=ENV_PATH)

    # so i can work with path as string instead of pathlib paths, need to change it to still use Pathlibs later
    # since pathlibs are now the standard
    base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    OAUTH_PROVIDERS: List[str] = []


class DevelopmentConfig(Config):
    CLIENT_ID: Optional[str] = os.environ.get("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = os.environ.get("CLIENT_SECRET")
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///" + os.path.join(base_dir, "app.db")
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")
    OAUTH_PROVIDERS: List[str] = ["github"]  # will change how this works later on


class ProductionConfig(Config):
    CLIENT_ID: Optional[str] = os.environ.get("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = os.environ.get("CLIENT_SECRET")
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.environ.get("DATABASE_URL")
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")


configuration_environment = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
