from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    spoti_clients = db.relationship('SpotiClient',
                                    backref=db.backref('owner', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class SpotiClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), nullable=False)
    client_secret = db.Column(db.String(40), nullable=False)
    client_name = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Spotify Client('{self.client_name}', '{self.client_id}')"