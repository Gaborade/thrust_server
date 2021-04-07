import os
from dotenv import load_dotenv
from pathlib import Path


BASE_PATH: Path = Path(__file__).resolve(strict=True).parent.parent  # strict=True makes it an absolute path
ENV_PATH: Path = base_path /'.env'
load_dotenv(dotenv_path=env_path)

class TestConfig:
    CLIENT_ID: str = os.environ.get('CLIENT_ID')
    CLIENT_SECRET: str = os.environ.get('CLIENT_SECRET')

