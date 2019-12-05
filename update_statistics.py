# Import packages 
import json
import os
import pandas as pd
import pymongo
import requests
from pprint import pprint

# Get the database details from the conda environment 
mongodb_password = os.environ.get("mongodb_password")
mongodb_user = os.environ.get("mongodb_user")

# Define max requests for this run 
api_max_requests = 10
request_counter = 0

# Access the database client and define database 
client = pymongo.MongoClient("mongodb+srv://" + mongodb_user + ":" + mongodb_password + "@basiccluster-6s0er.mongodb.net/test?retryWrites=true&w=majority")
db = client.football

# Get the API details from the conda environment 
headers = {
    'x-rapidapi-host': os.environ.get("api_host"), 
    'x-rapidapi-key': os.environ.get("api_key") 
    }

# Define a function that calls a given request
def api_call(url):
    response = requests.request("GET", url, headers=headers)
    
    # Return a dictionary of the response text
    return json.loads(response.text)

#current_fixtures = db.fixtures.find()

# Find those completed fixtures that don't have statistics 
fixtures_without_stats = db.fixtures.find({'statistics': { '$exists' : False }, 'statusShort':'FT'})

# Loop through a given number of times and update the fixture with statistics
for i in range(0,5):
    # Break the loop if you can't find the fixture to update
    try:
        fixture_to_update = fixtures_without_stats[i]
    except:
        print('No fixture to update.')
        break
        
    # Call the statistics api using the fixture_id
    fixture_statistics = api_call("https://api-football-v1.p.rapidapi.com/v2/statistics/fixture/%d" % fixture_to_update['fixture_id'])

    # Update the fixture document using the api results 
    db.fixtures.update_one({'fixture_id': fixture_to_update['fixture_id']}, {'$set': {'statistics': fixture_statistics['api']['statistics']}}, upsert=True)
    
    # Have a command line tracker for reference
    print("API call %s : %s" % (i + 1, fixture_to_update['fixture_id']))