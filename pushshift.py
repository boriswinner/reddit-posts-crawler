import requests
from datetime import datetime, timedelta
import json

SUBREDDIT = "CryptoCurrency"
SEARCH_WORDS = ["BTT", "BitTorrent Token"]
DATE_FROM = 1612129226
DATE_TO = 1612215626

def clean_responce_data(data):
    res = []
    wanted_keys = ['created_utc', 'title', 'selftext', 'num_comments', 'full_link', 'subreddit', 'subreddit_subscribers']
    for item in data:
        res.append(dict((k, item[k]) for k in wanted_keys if k in item))
    return res

def request_data(subreddit, start_timestamp, end_timestamp):
    res = requests.get("https://api.pushshift.io/reddit/search/submission/"
                       "?subreddit={}&"
                       "sort=desc&"
                       "sort_type=created_utc&"
                       "after={}&"
                       "before={}&"
                       "size=100".format(subreddit, str(int(start_timestamp)), str(int(end_timestamp))))  # max size = 100
    if (res.status_code != 200):
        print("WARNING! Incorrect request! Skipping...")
        print(res.request)
        print(res.status_code)
    else:
        try:
            data = clean_responce_data(res.json()["data"])
            return data
        except:
            print("Error! Illegal response! Skipping...")
            return []

def request_by_hours(start_timestamp, end_timestamp):
    res_array = []

    while start_timestamp <= end_timestamp:
        temp_start_timestamp = start_timestamp
        temp_end_timestamp = datetime.timestamp(datetime.fromtimestamp(start_timestamp) + timedelta(minutes=30))
        print("Requesting data starting at {}...".format(datetime.fromtimestamp(temp_start_timestamp).ctime()))
        res = request_data(SUBREDDIT, temp_start_timestamp, temp_end_timestamp)
        print("Got {} items.".format(len(res)))
        res_array.extend(res)
        start_timestamp = temp_end_timestamp

    return res_array

data = request_by_hours(DATE_FROM, DATE_TO)

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

import pandas as pd
df = pd.DataFrame(data)
print(df)
