import requests
from flask_login import UserMixin

from ci_server import db, login


class User(db.Model, UserMixin):
    """A model for the User class.

    Key Pointers:
        :token is a one-to-one relationship which takes effect by setting uselist to False.

        :repository is a one-to-many relationship with cascade parameter.
        Cascade is a comma-separated list of rules which determines how session operations should be
        "cascaded" from parent to child. 'all', 'delete' to indicate that related objects should follow with
        the parent object in all cases and should be deleted when de-associated. See flask_sqlalchemy documentation

        :organization is a many-to-many relationship.
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=True)
    avatar_url = db.Column(db.String(100), nullable=True)
    token = db.relationship(
        "OAuth2Token", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    """#repository = db.relationship(
        "Repository", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    organization = db.relationship(
        "Organization",
        secondary="organization",
        backref=db.backref("user", lazy="dynamic"),
    )"""

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    @staticmethod
    def get_avatar(self):
        response = requests.get(self.avatar_url)
        response.raise_for_status()
        return response.content  # need to know what .content attribute
        # or what if in case user has no avatar i replace with some sort of placeholder image from my statics template\
        # and also to use tenacity which has retries and backoffs

    """#def save(self):
        # to send signals to other models that User is saved
        model_saved.send(self) """


@login.user_loader
def login_user(id: int) -> User:
    return User.query.get(int(id))
