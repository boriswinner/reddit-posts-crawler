import requests
from datetime import datetime, timedelta
from praw_reddit_api import PrawRedditApi
from tqdm import tqdm
import sys
import time

SUBREDDIT = "CryptoCurrency"
PRAW = PrawRedditApi()

class PushshiftApi:
    def __init__(self):
        ...

    def clean_comments(selfself, comments):
        cleaned_comments = []
        for comment in comments:
            if (not comment or comment.body == '[removed]' or comment.body == '[deleted]'):
                continue
            cleaned_comment = {
                'body': comment.body,
                'created_utc': comment.created_utc,
                'ups': comment.ups,
                'downs': comment.downs,
            }
            cleaned_comments.append(cleaned_comment)
        return cleaned_comments

    def process_posts(self, data):
        #clips unneccessary keys and obtains comments
        res = []
        wanted_keys = ['created_utc', 'title', 'selftext', 'num_comments', 'full_link', 'subreddit', 'subreddit_subscribers', 'id']
        for item in tqdm(data, desc="Processing posts within time range... ", file=sys.stdout):
            if item['selftext'] == "" or item['selftext'] == "[removed]" or item['selftext'] == "[deleted]":
                continue
            temp_dict = dict((k, item[k]) for k in wanted_keys if k in item)
            comments = PRAW.get_comments_of_post(temp_dict['id'])
            cleaned_comments = self.clean_comments(comments)
            temp_dict["comments"] = cleaned_comments
            res.append(temp_dict)
        return res

    def request_data(self, subreddit, start_timestamp, end_timestamp):
        res = requests.get("https://api.pushshift.io/reddit/search/submission/"
                           "?subreddit={}&"
                           "sort=desc&"
                           "sort_type=created_utc&"
                           "after={}&"
                           "before={}&"
                           "selftext:not='[removed]'&"
                           "q:not='[deleted]'&"
                           "size=100".format(subreddit, str(int(start_timestamp)), str(int(end_timestamp))))  # max size = 100
        if (res.status_code == 429):
            print("Too many requests. Waiting 1 minute...")
            time.sleep(60)
            return []
        elif (res.status_code != 200):
            print("WARNING! Incorrect request! Skipping...")
            print(res.request)
            print(res.status_code)
            return []
        else:
            try:
                data = self.process_posts(res.json()["data"])
                return data
            except:
                print("Error! Illegal response! Skipping...")
                return []

    def request_by_hours(self, start_timestamp, end_timestamp):
        res_array = []

        while start_timestamp <= end_timestamp:
            temp_start_timestamp = start_timestamp
            temp_end_timestamp = datetime.timestamp(datetime.fromtimestamp(start_timestamp) + timedelta(minutes=30))
            print("Requesting data starting at {}...".format(datetime.fromtimestamp(temp_start_timestamp).ctime()))
            try:
                res = self.request_data(SUBREDDIT, temp_start_timestamp, temp_end_timestamp)
                res_array.extend(res)
                print("Proccessed {} items.".format(len(res)))
            except Exception as e:
                print("Unknown Error when requesting: {}".format(e))
            start_timestamp = temp_end_timestamp

        return res_array


