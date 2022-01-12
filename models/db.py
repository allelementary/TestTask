from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    access = db.Column(db.Integer, default=0)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name, last_name, password, access):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.access = access

    def __repr__(self):
        return f'User email: {self.email}'
