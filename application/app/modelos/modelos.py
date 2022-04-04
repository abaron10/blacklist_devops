from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password1 = db.Column(db.String(50))
    email = db.Column(db.String(100))
    tasks = relationship('BlackList')

class BlackList(db.Model):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    uuid = db.Column(db.String(50))
    reason = db.Column(db.String(255))
    created_by = db.Column(db.Integer, ForeignKey('user.id'))
    created_on = db.Column(db.String(100))
    ip_addr = db.Column(db.String(100))
