import os
from typing import List, Optional

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
    # to work around heroku postgres debacle since you cannot change the url on their dashboard
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "posgresql://", 1)  # type: ignore
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")


configuration_environment = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
