from config import config
from peewee import PostgresqlDatabase


db = PostgresqlDatabase(config.DATABASE, user=config.USER, password=config.PASSWORD, host=config.HOST, port=config.PORT)