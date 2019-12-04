import os 
import pymongo

class League():
    def __init__(self, league_name = 'Premier League'):
        mongodb_password = os.environ.get("mongodb_password")
        mongodb_user = os.environ.get("mongodb_user")
        client = pymongo.MongoClient("mongodb+srv://" + mongodb_user + ":" + mongodb_password + "@basiccluster-6s0er.mongodb.net/test?retryWrites=true&w=majority")
        self.db = client.football
        self.name = league_name
        
    def fixtures(self):
        '''Get all fixtures for a given league using the name'''
        fixtures = self.db.fixtures.find({'league.name':self.name})
        return(fixtures)