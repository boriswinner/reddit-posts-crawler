import pmaw
from pmaw import PushshiftAPI
import pandas as pd
import sys
from tqdm import tqdm
import json
from datetime import datetime, timedelta

SUBREDDIT = "SatoshiStreetBets"
# UTC
DATE_FROM = 1619827200
DATE_TO = 1622505600

class PmawRedditApi:
    def __init__(self):
        self.CLIENT_ID = "UxFxm6wVgTGqPA"
        self.SECRET_TOKEN = "ryHh-ei7doqRC3OSHGyL1557QZSCVQ"

        self.api = PushshiftAPI()

    def clean_comments(selfself, comments):
        cleaned_comments = []
        for comment in comments:
            if (not comment or comment['body'] == '[removed]' or comment['body'] == '[deleted]'):
                continue
            cleaned_comment = {
                'body': comment['body'],
                'created_utc': comment['created_utc'],
                'id': comment['id'],
                'permalink': comment['permalink'],
                'subreddit': comment['subreddit'],
                'subreddit_id': comment['subreddit_id'],
                'score': comment['score'],
            }
            cleaned_comments.append(cleaned_comment)
        return cleaned_comments

    def process_posts(self, data):
        #clips unneccessary keys
        res = []
        wanted_keys = ['created_utc', 'title', 'selftext', 'num_comments', 'full_link', 'subreddit', 'subreddit_subscribers', 'id']
        for item in tqdm(data.responses, desc="Processing posts within time range... ", file=sys.stdout):
            if item['selftext'] == "" or item['selftext'] == "[removed]" or item['selftext'] == "[deleted]":
                continue
            temp_dict = dict((k, item[k]) for k in wanted_keys if k in item)
            comments = self.get_comments_for_post(temp_dict['id'])
            cleaned_comments = self.clean_comments(comments)
            temp_dict["comments"] = cleaned_comments
            res.append(temp_dict)
        return res

    def get_comments_for_post(self, submission_id):
        comment_ids = self.api.search_submission_comment_ids(ids=[submission_id])
        comment_ids = list(comment_ids)
        comments = self.api.search_comments(ids=comment_ids)
        return comments


    def get_submissions_with_comments_by_date(self, DATE_FROM, DATE_TO):
        submissions = self.api.search_submissions(subreddit=SUBREDDIT, limit=300000, after=DATE_FROM, before=DATE_TO)
        submissions = self.process_posts(submissions)
        return submissions

    def request_by_hours(self, start_timestamp, end_timestamp):
        res_array = []

        while start_timestamp <= end_timestamp:
            temp_start_timestamp = start_timestamp
            temp_end_timestamp = datetime.timestamp(datetime.fromtimestamp(start_timestamp) + timedelta(minutes=30))
            print("Requesting data starting at {}...".format(datetime.fromtimestamp(temp_start_timestamp).ctime()))
            try:
                res = self.get_submissions_with_comments_by_date(temp_start_timestamp, temp_end_timestamp)
                res_array.extend(res)
                print("Proccessed {} items.".format(len(res)))
            except Exception as e:
                print("Unknown Error when requesting: {}".format(e))
            start_timestamp = temp_end_timestamp

        return res_array

    def request_comments(self):
        comments = self.api.search_comments(subreddit=SUBREDDIT,limit=300000, after=DATE_FROM, before=DATE_TO)
        cleaned_comments = self.clean_comments(comments)
        return cleaned_comments

test = PmawRedditApi()
# data = test.get_submissions_with_comments_by_date(DATE_FROM, DATE_TO)
data = test.request_comments()
filename = 'data_{}_{}_{}.json'.format(SUBREDDIT, DATE_FROM, DATE_TO)
with open(filename, 'w') as f:
    print("Success! Writing data to{}...".format(filename))
    json.dump(data, f)
