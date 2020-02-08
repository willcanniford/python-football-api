# Import packages
import json
import os
import pandas as pd
import pymongo
import requests


def connect_to_mongodb(database_name):
    '''
    Get connection to database

    Parameters
    ----------
    database_name: string
        Define the name of the database to get from the client
    '''
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

    db = client[database_name]
    return(db)


def api_call(url, headers=False):
    '''
    Call the given API endpoint and load the resulting JSON object

    Parameters
    ----------
    url: string
        The API endpoint to call with a GET request
    '''

    if not headers:
        # Get the API details from the conda environment
        header_dict = {
            'x-rapidapi-host': os.environ.get("api_host"),
            'x-rapidapi-key': os.environ.get("api_key")
        }

    response = requests.request("GET", url, headers=header_dict)

    try:
        response = json.loads(response.text)
    except BaseException:
        print(f"Response {response.text} isn't valid JSON format.")

    return(response)
