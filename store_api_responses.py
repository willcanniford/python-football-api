# Import packages
import json
import os
import pandas as pd
import pymongo
import requests
from classes.progress_bar import printProgressBar

# Get the database details from the conda environment
mongodb_password = os.environ.get("mongodb_password")
mongodb_user = os.environ.get("mongodb_user")

# Access the database client and define database
client = pymongo.MongoClient(
    "mongodb+srv://" +
    mongodb_user +
    ":" +
    mongodb_password +
    "@basiccluster-6s0er.mongodb.net/test?retryWrites=true&w=majority")
db = client.football

# Get the API details from the conda environment
headers = {
    'x-rapidapi-host': os.environ.get("api_host"),
    'x-rapidapi-key': os.environ.get("api_key")
}

# Define a function that calls a given endpoint


def api_call(url):
    '''
    Call the given url and load the resulting JSON object

    Parameters
    ----------
    url: string
        The API endpoint to call with a GET request
    '''
    response = requests.request("GET", url, headers=headers)

    try:
        response = json.loads(response.text)
    except BaseException:
        print(f"Response {response.text} isn't valid JSON format.")

    return(response)


# Call Premier League Endpoint and store all fixtures
base_url = 'https://api-football-v1.p.rapidapi.com/v2/'
premier_league_id = '524'
fixtures_url = base_url + 'fixtures/league/' + premier_league_id
all_fixtures_response = api_call(fixtures_url)

# Check the response is in the format we need
try:
    all_fixtures = all_fixtures_response['api']['fixtures']
except BaseException:
    print(f"Fixture response not in expected format: {all_fixtures_response}")

# Get current fixtures stored in MongoDB
current_fixtures = db.fixtures.find()

# Progress bar counter
total_fixtures = len(all_fixtures)
i = 0

# Loop through the fixtures and update all the records with the base
# information
for nf in all_fixtures:
    # Join on fixture_id and update/insert all data
    db.fixtures.update_many({'fixture_id': nf['fixture_id']}, {
                            '$set': nf}, upsert=True)
    
    i = i + 1
    printProgressBar(i, total_fixtures, '> Progress: ', '', 3, 30)

print('All fixtures updated.')


fixtures_without_stats = db.fixtures.find(
    {'statistics': {'$exists': False}, 'statusShort': 'FT'})

print(f"Fixtures missing statistics: {len(list(fixtures_without_stats))}")


# while request_counter < api_max_requests: # Won't increment properly
#    fixture = fixtures_without_stats['api']['statistics'][i]
#    statistics_url = "https://api-football-v1.p.rapidapi.com/v2/statistics/fixture/%d"
#    fixture_statistics = api_call(statistics_url % fixture['fixture_id'])
#    request_counter = request_counter + 1
#    db.test.update_one({'fixture_id': fixture['fixture_id']}, {'$set': {'statistics': fixture_statistics}}, upsert=True)

#fixtures_without_events = db.fixtures.find({'events': { '$exists' : False }, 'statusShort':'FT'})

# while request_counter < api_max_requests:
#    fixture = fixtures_without_events['api']['events'][i]
#    events_url = ''
#    fixture_events = api_call(events_url % fixture['fixture_id'])
#    request_counter = request_counter + 1
#    db.test.update_one({'fixture_id': 2}, {'$set': {'events': fixture_events}}, upsert=True)
