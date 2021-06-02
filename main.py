import requests
TOKEN_FILENAME = "TOKEN.TXT"
TOKEN = ""
CLIENT_ID = ""
SECRET_TOKEN = ""
REDDIT_USERNAME = ""
REDDIT_PASSWORD = ""
GET_TOKEN_HEADERS = {'User-Agent': 'BigDataHomework/0.0.1'}
HEADERS = None

def update_headers():
    global HEADERS
    HEADERS = {**GET_TOKEN_HEADERS, **{'Authorization': f"bearer {TOKEN}"}}

def check_token():
    res = requests.get('https://oauth.reddit.com/api/v1/me', headers=HEADERS)
    if (res.status_code != 200):
        print("WARNING: The request doesn't pass. Trying to retrieve a new token...")
        print(res.status_code)
        return False
    return True

def get_new_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
    data = {'grant_type': 'password',
            'username': REDDIT_USERNAME,
            'password': REDDIT_PASSWORD,
            }
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=GET_TOKEN_HEADERS)
    global TOKEN
    TOKEN = res.json()['access_token']
    update_headers()
    with open(TOKEN_FILENAME, 'w') as file:
        file.write(TOKEN)

def retrieve_token():
    import os.path

    if os.path.isfile(TOKEN_FILENAME):
        with open(TOKEN_FILENAME, 'r') as file:
            global TOKEN
            TOKEN = file.read().replace('\n', '')
            update_headers()
            if not check_token():
                get_new_token()
    else:
        get_new_token()


retrieve_token()

# while the token is valid (~2 hours) we just add headers=headers to our requests
res = requests.get('https://oauth.reddit.com/api/v1/me', headers=HEADERS)
print(res.json())  # let's see what we get

res = requests.get("https://oauth.reddit.com/r/python/hot",
                   headers=HEADERS)

print(res.json())  # let's see what we get