import json
from pushshift import PushshiftApi

DATE_FROM = 1612129226
DATE_TO = 1612136426

pushshift_api = PushshiftApi()

data = pushshift_api.request_by_hours(DATE_FROM, DATE_TO)

with open('data.json', 'w') as f:
    print("Success! Writing data to data.json...")
    json.dump(data, f, indent=2)