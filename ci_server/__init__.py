import sys
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

from .config import configuration_environment

# instantiate classes
app: Flask = Flask(__name__)
if not app.debug:
    app.config.from_object(configuration_environment["production"])
else:
    app.config.from_object(configuration_environment["development"])
app.secret_key = app.config["SECRET_KEY"]
oauth: OAuth = OAuth(app)
db: SQLAlchemy = SQLAlchemy(app)
migrate: Migrate = Migrate(app, db)
login: LoginManager = LoginManager(app)


# to avoid circular imports
from ci_server.models import OAuth2Token as Token  # noqa: E402
from ci_server.models import User  # noqa: E402


def fetch_token(oauth_provider: str = "github") -> dict:
    if oauth_provider in app.config["OAUTH_PROVIDERS"]:
        token_model = Token
    elif oauth_provider not in app.config["OAUTH_PROVIDERS"]:
        print("OAuth Provider does not exist", file=sys.stderr)
        sys.exit(1)
    token = token_model.query.filter_by(
        name=oauth_provider, user_id=current_user.id
    ).first()
    if token is None:
        print("Token does not exist", file=sys.stderr)
        sys.exit(1)
    return token.to_token()


def update_token(
    token: Dict[str, Any],
    name: str = "github",
    refresh_token: Optional[str] = None,
    access_token: Optional[str] = None,
) -> None:

    if refresh_token:
        token_model = Token.query.filter_by(
            name=name, refresh_token=refresh_token
        ).first()
    elif access_token:
        token_model = Token.query.filter_by(
            name=name, access_token=access_token
        ).first()
    else:
        return

    token_model.access_token = token.get("access_token")
    token_model.refresh_token = token.get("refresh_token")
    # was thinking in case expires_in was given i could do something like this
    # token_model.expires_in = token.get('expires_in', datetime.datetime.now())
    # but this will do for now
    token_model.timestamp = datetime.utcnow()
    # seems i may not need the update_token cause github oauth apps don't do that
    db.session.commit()


# i may have to add compliance hooks


# register 3rd party integrations
oauth.register(
    name="github",
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    fetch_token=fetch_token,
    client_kwargs={
        "scope": "read:user user:email repo:status repo"
    }  # user:email to get get user email to send ci and build notifications
    # repo:status scope to update status of commit after pull request and test
    # repo scope to provide access to code
)


# routes
@app.route("/")
def home() -> str:
    return "Thrust the ci service rocks"


@app.route("/signup")
def zarathustra_signup() -> Callable:
    if current_user.is_authenticated:
        return redirect(url_for("user_dashboard"))
    github = oauth.create_client("github")
    redirect_uri = url_for("github_authorization", _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route("/callback")
def github_authorization() -> Callable:
    token = oauth.github.authorize_access_token()
    response = oauth.github.get("user", token=token)
    response.raise_for_status()
    user_profile = response.json()
    try:
        user = User.query.filter_by(id=user_profile["id"]).first_or_404()
    except NotFound:
        user = User(
            id=user_profile["id"],
            username=user_profile.get("login") or user_profile.get("name"),
            email=user_profile["email"],
            avatar_url=user_profile["avatar_url"],
        )
        db.session.add(user)
        db.session.commit()

        user_token = Token(
            name="github",
            user_id=user_profile["id"],
            access_token=token["access_token"],
            token_type=token["token_type"],
            scope=token["scope"],
        )
        db.session.add(user_token)
        db.session.commit()
    finally:
        login_user(user, remember=True)
        return redirect(url_for("user_dashboard"))
    # return jsonify(message="You are logged in")


@app.route("/login")
def zarathustra_login():
    return redirect(url_for("zarathustra_signup"))


@app.route("/dashboard")
@login_required
def user_dashboard() -> str:
    return f"Hello {current_user.username}. Behold, Feast your eyes on the dazzle of the not so distant cyberfuture"


@app.route("/repositories")
@login_required
def get_repositories():
    res = oauth.github.get(f"users/{current_user.username}/repos")
    res.raise_for_status()
    return f"{res.json()}"


@app.route("/show-profile")
@login_required
def show_profile():
    response = oauth.github.get("user")
    response.raise_for_status()
    return response.json()


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
