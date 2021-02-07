import random
from datetime import datetime
from sqlalchemy.orm import backref
from webapp import db, login_manager
from webapp.config import Config
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pin = db.Column(db.String(4), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, default=False)
    date_created = db.Column(db.DateTime, unique=False,
                             default=datetime.utcnow)
    prediction = db.relationship(
        'Prediction', cascade="all,delete", backref='parent')

    def __init__(self, username):
        self.username = username
        self.pin = self.create_pin()
        self.is_admin = self.admin_status()

    def create_pin(self):
        if self.username == 'admin':
            return Config.ADMIN_PIN
        else:
            return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def admin_status(self):
        if self.username == 'admin':
            return True
        else:
            False

    def __repr__(self):
        return f'<User({self.id}, {self.pin}, {self.is_admin})>'


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    username = db.Column(db.String(20), unique=True, nullable=False)
    ed_1 = db.Column(db.String(50), nullable=False)
    ed_2 = db.Column(db.String(50), nullable=False)
    ed_3 = db.Column(db.String(50), nullable=False)
    ed_4 = db.Column(db.String(50), nullable=False)
    ed_5 = db.Column(db.String(50), nullable=False)
    ed_6 = db.Column(db.String(50), nullable=False)
    ed_7 = db.Column(db.String(50), nullable=False)
    ed_8 = db.Column(db.String(50), nullable=False)
    ed_9 = db.Column(db.String(50), nullable=False)
    ed_10 = db.Column(db.String(50), nullable=False)
    ed_11 = db.Column(db.String(50), nullable=False)
    ed_12 = db.Column(db.String(50), nullable=False)
    ed_13 = db.Column(db.String(50), nullable=False)
    ed_14 = db.Column(db.String(50), nullable=False)
    ed_15 = db.Column(db.String(50), nullable=False)
    ed_16 = db.Column(db.String(50), nullable=False)
    ed_17 = db.Column(db.String(50), nullable=False)
    ed_18 = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, username, ed_1, ed_2, ed_3, ed_4, ed_5, ed_6, ed_7, ed_8, ed_9,
                 ed_10, ed_11, ed_12, ed_13, ed_14, ed_15, ed_16, ed_17, ed_18):
        self.user_id = user_id
        self.username = username
        self.ed_1 = ed_1
        self.ed_2 = ed_2
        self.ed_3 = ed_3
        self.ed_4 = ed_4
        self.ed_5 = ed_5
        self.ed_6 = ed_6
        self.ed_7 = ed_7
        self.ed_8 = ed_8
        self.ed_9 = ed_9
        self.ed_10 = ed_10
        self.ed_11 = ed_11
        self.ed_12 = ed_12
        self.ed_13 = ed_13
        self.ed_14 = ed_14
        self.ed_15 = ed_15
        self.ed_16 = ed_16
        self.ed_17 = ed_17
        self.ed_18 = ed_18

    def __repr__(self):
        return f"Prediction('{self.user_id}')"
