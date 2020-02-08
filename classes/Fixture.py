import os
import pymongo
from .helpers import *


class Fixture():
    def __init__(self, fixture_id):
        self.fixture_id = fixture_id
        db = connect_to_mongodb('football')
        self.response = db.fixtures.find_one({'fixture_id': fixture_id})
