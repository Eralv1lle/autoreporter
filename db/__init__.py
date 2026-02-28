from .models import User, Document
from .database import db


def init_db():
    db.connect()
    db.create_tables([User, Document])