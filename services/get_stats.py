from db import User, Document
from peewee import fn, JOIN


def get_stats():
    top_3 = User.select(User, fn.COUNT(Document.id).alias("cnt")).join(Document, JOIN.LEFT_OUTER).group_by(User.user_id).order_by(fn.COUNT(Document.id).desc()).limit(3)
    return {
        "count_users": User.select().count(),
        "count_docs": Document.select().count(),
        "top_3": top_3
    }