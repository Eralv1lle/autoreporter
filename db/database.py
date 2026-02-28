from config import config
from peewee import PostgresqlDatabase


db = PostgresqlDatabase(config.DATABASE, user=config.DB_USER, password=config.PASSWORD, host=config.HOST, port=config.PORT)