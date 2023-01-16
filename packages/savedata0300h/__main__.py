# Standard library imports
import os
import datetime

from urllib.parse import quote_plus

# Third party imports
import pymongo
import requests

from bs4 import BeautifulSoup


def getcreds():
    """
    Get the credentials from environment variables.
    """

    ### Environment variables ###
    # GitHub credentials
    GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

    # MongoDB credentials
    MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
    MONGODB_HOST = os.environ.get("MONGODB_HOST")

    # Connect to MongoDB
    _mongodb_client = pymongo.MongoClient(
        f"mongodb+srv://{quote_plus(MONGODB_USERNAME)}:{quote_plus(MONGODB_PASSWORD)}@{MONGODB_HOST}"
    )

    # Get database mystats
    mongodb_database = _mongodb_client["mystats"]

    return mongodb_database, GITHUB_USERNAME


def get_ghcommits(github_username, mongodb_database):
    """
    Get the number of commits made on GitHub for a given user on the
    previous day from when the function is called.
    """

    # Get the date for yesterday
    yesterdate = datetime.date.today() - datetime.timedelta(days=1)

    # Convert the date to a string in the format YYYY-MM-DD
    yesterday = yesterdate.strftime("%Y-%m-%d")

    # Get the HTML for the GitHub profile page
    data = requests.get(f"https://github.com/{github_username}/")

    # Parse HTML and save to BeautifulSoup object
    html = BeautifulSoup(data.text, "html.parser")

    # Select the rect element with the data-date attribute equal to yesterday
    commit_element = html.find_all("rect", attrs={"data-date": yesterday})
    commit_count = int(commit_element[0]["data-level"])

    mongodb_database["gh_commits"].insert_one(
        {"date": yesterdate, "commit_count": commit_count}
    )


def main(args):
    mongodb_database, github_username = getcreds()
    get_ghcommits(github_username, mongodb_database)

    return {"body": "Success: Saved the data for GitHub commits."}
