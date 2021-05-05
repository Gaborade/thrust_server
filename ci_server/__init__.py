from typing import Callable

from authlib.integrations.flask_client import OAuth
from flask import Flask, Response, jsonify, url_for

from . import config

__version__: str = "0.1.0"

app: Flask = Flask(__name__)
app.config.from_object(config.TestConfig)
app.secret_key = app.config["SECRET_KEY"]
oauth: OAuth = OAuth(app)


oauth.register(
    name="github",
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={
        "scope": "read:user user:email repo:status repo"
    }  # user:email to get get user email to send ci and build notifications
    # repo:status scope to update status of commit after pull request and test
    # repo scope to provide access to code
)


@app.route("/")
def home() -> str:
    return "Thrust the ci service"


@app.route("/login")
def login() -> Callable:
    github = oauth.create_client("github")
    redirect_uri = url_for("authorize", _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route("/callback")
def authorize() -> Response:  # for json
    token = oauth.github.authorize_access_token()
    response = oauth.github.get("user", token=token)
    response.raise_for_status()
    profile = response.json()
    return jsonify(profile)
