from peewee import *
from datetime import datetime

from .database import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = BigIntegerField(unique=True, primary_key=True)
    name = CharField()
    username = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)


class Document(BaseModel):
    user = ForeignKeyField(User, backref="documents", on_delete="CASCADE")
    filename = CharField()
    filepath = CharField()
    created_at = DateTimeField(default=datetime.now)
