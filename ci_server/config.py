import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

BASE_PATH = (
    Path(__file__).resolve(strict=True).parent.parent
)  # strict=True makes it an absolute path
ENV_PATH = BASE_PATH / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# so i can work with path as string instead of pathlib paths, need to change it to still use Pathlibs later
# since pathlibs are now the standard
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: Optional[bool] = None
    OAUTH_PROVIDERS: List[str] = []


class DevelopmentConfig(Config):
    CLIENT_ID: Optional[str] = os.environ.get("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = os.environ.get("CLIENT_SECRET")
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///" + os.path.join(
        base_dir, "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = "constantinople"
    OAUTH_PROVIDERS: List[str] = ["github"]  # will change how this works later on


class ProductionConfig(Config):
    DEBUG: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    CLIENT_ID: Optional[str] = os.environ.get("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = os.environ.get("CLIENT_SECRET")
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.environ.get("DATABASE_URL")


configuration_environment = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
