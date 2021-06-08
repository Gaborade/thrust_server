from datetime import datetime, timedelta

from ci_server import db

TOKEN_EXPIRES_IN: int = 3600 * 8


class OAuth2Token(db.Model):
    "OAuth Token class for storing access tokens of logged users"
    __tablename__ = "oauth2token"

    name = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    access_token = db.Column(db.String(200), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    token_type = db.Column(db.String(20))
    scope = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"<Token {self.access_token}"

    def is_expired(self) -> bool:
        global TOKEN_EXPIRES_IN
        return datetime.utcnow() > self.timestamp + timedelta(seconds=TOKEN_EXPIRES_IN)

    def to_token(self) -> dict:
        return dict(
            access_token=self.access_token, scope=self.scope, token_type=self.token_type
        )
