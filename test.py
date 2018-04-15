from pymongo import MongoClient

from datetime import timedelta

client = MongoClient()

db =client.mydb

expires = timedelta(seconds = 8)

db.test_set.create_index('timestamp',expireAfterSeconds = expires.total_seconds())


