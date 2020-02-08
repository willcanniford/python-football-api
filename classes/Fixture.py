# Imports 
import os
import pymongo


class Fixture():
    def __init__(self, fixture_id):
        self.fixture_id = fixture_id
        mongodb_password = os.environ.get("mongodb_password")
        mongodb_user = os.environ.get("mongodb_user")
        client = pymongo.MongoClient(
            "mongodb+srv://" +
            mongodb_user +
            ":" +
            mongodb_password +
            "@basiccluster-6s0er.mongodb.net/test?retryWrites=true&w=majority")
        db = client.football
        self.response = db.fixtures.find_one({'fixture_id': fixture_id})
