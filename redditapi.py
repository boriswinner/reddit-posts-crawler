import requests
import json

class RedditCrawler:
    def __init__(self):
        self.TOKEN_FILENAME = "TOKEN.TXT"
        self.TOKEN = ""
        self.CLIENT_ID = ""
        self.SECRET_TOKEN = ""
        self.REDDIT_USERNAME = ""
        self.REDDIT_PASSWORD = ""
        self.GET_TOKEN_HEADERS = {'User-Agent': 'BigDataHomework/0.0.1'}
        self.HEADERS = None
        self.__get_new_token__()

    def __update_headers__(self):
        self.HEADERS = {**self.GET_TOKEN_HEADERS, **{'Authorization': f"bearer {self.TOKEN}"}}

    def __check_token__(self):
        res = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.HEADERS)
        if (res.status_code != 200):
            print("WARNING: The request doesn't pass. Trying to retrieve a new token...")
            print(res.status_code)
            return False
        return True

    def __get_new_token__(self):
        auth = requests.auth.HTTPBasicAuth(self.CLIENT_ID, self.SECRET_TOKEN)
        data = {'grant_type': 'password',
                'username': self.REDDIT_USERNAME,
                'password': self.REDDIT_PASSWORD,
                }
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=self.GET_TOKEN_HEADERS)
        self.TOKEN = res.json()['access_token']
        self.__update_headers__()

    def get_comments_of_post(self, subreddit, post_id):
        res = requests.get("https://oauth.reddit.com/r/{}/comments/{}".format(subreddit, post_id),
                           headers=self.HEADERS)
        if (res.status_code != 200):
            print("WARNING: Couldn't retrieve comments. Trying to change token...")
            self.__get_new_token__()
            res = requests.get("https://oauth.reddit.com/r/{}/comments/{}".format(subreddit, post_id),
                               headers=self.HEADERS)
            if (res.status_code == 200):
                try:
                    return res.json()
                except:
                    print("ERROR: Bad result")
                    return []
            else:
                print("ERROR: Couldn't retrieve comments. Code {}".format(res.status_code))
                return []
        else:
            try:
                return res.json()
            except:
                print("ERROR: Bad result")
                return []

    def strip_comments(self, data):
        # data["data"]
        with open('afefef.json', 'w') as f:
            json.dump(data, f, indent=2)


def get_comments_of_post(post_id):
    ...

# while the token is valid (~2 hours) we just add headers=headers to our requests
# res = requests.get('https://oauth.reddit.com/api/v1/me', headers=HEADERS)
# print(res.json())  # let's see what we get
#
# res = requests.get("https://oauth.reddit.com/r/python/hot",
#                    headers=HEADERS)
#
# print(res.json())  # let's see what we get

# res = requests.get("https://oauth.reddit.com/r/CryptoCurrency/comments/nqkz16",
#                    headers=HEADERS)
#
# print(res.json())  # let's see what we get