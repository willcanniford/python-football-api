# Import packages
import pandas as pd
from classes.progress_bar import printProgressBar
import classes.helpers as hlp
import argparse
import time

# Handle arguments
a = argparse.ArgumentParser(description='store_api_responses.py')
a.add_argument('--results', dest="results",
               action="store", type=bool, default=False)
a.add_argument("--statistics", dest="statistics",
               action="store", type=int, default=10)

arguments = a.parse_args()
check_results = arguments.results
n_statistics_to_update = arguments.statistics


# Connect to the database
db = hlp.connect_to_mongodb('football')
current_fixtures = db.fixtures.find()

if check_results == True:
    # Call Premier League Endpoint and store all fixtures
    base_url = 'https://api-football-v1.p.rapidapi.com/v2/'
    premier_league_id = '524'
    fixtures_url = base_url + 'fixtures/league/' + premier_league_id
    all_fixtures_response = hlp.api_call(fixtures_url)

    # Check the response is in the format we need
    try:
        all_fixtures = all_fixtures_response['api']['fixtures']
    except BaseException:
        print(
            f"Fixture response not in expected format: {all_fixtures_response}")

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
        printProgressBar(i, total_fixtures, '> Progress: ',
                         '', 3, 30, '#', '\r', '/n')

    print('All fixtures updated.')


fixtures_without_stats = db.fixtures.find(
    {'statistics': {'$exists': False}, 'statusShort': 'FT'})

n_fixtures_without_stats = db.fixtures.count_documents(
    {'statistics': {'$exists': False}, 'statusShort': 'FT'})

if n_statistics_to_update > 0 and n_fixtures_without_stats > 0:
    statistics_url = "https://api-football-v1.p.rapidapi.com/v2/statistics/fixture/%d"

    # Loop through n times - min
    n = min(n_statistics_to_update, n_fixtures_without_stats)
    for i in range(n):
        try:
            fixture_to_update = fixtures_without_stats[i]
        except:
            raise("No fixture to update.")

        # Get statistics
        fixture_stat_response = hlp.api_call(
            statistics_url % fixture_to_update['fixture_id'])
        time.sleep(.250)

        try:
            fixture_stats = fixture_stat_response['api']['statistics']
        except KeyError:
            print(
                f"Cannot find statistics in response: {fixture_stat_response}")
            break

        # Update fixture
        db.fixtures.update_one({'fixture_id': fixture_to_update['fixture_id']},
                               {'$set': {'statistics': fixture_stats}},
                               upsert=True)

        printProgressBar(i, n, 'Statistic updates: ',
                         '', 3, 30, '#', '\r', '/n')


n_fixtures_without_stats = db.fixtures.count_documents(
    {'statistics': {'$exists': False}, 'statusShort': 'FT'})

print(
    f"Finished fixtures missing statistics: {n_fixtures_without_stats}")


fixtures_without_stats = db.fixtures.find(
    {'events': {'$exists': False}, 'statusShort': 'FT'})

print(f"Finished fixtures missing events: {len(list(fixtures_without_stats))}")


fixtures_without_stats = db.fixtures.find(
    {'lineups': {'$exists': False}, 'statusShort': 'FT'})

print(
    f"Finished fixtures missing lineups: {len(list(fixtures_without_stats))}")

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
