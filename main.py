import json
from pushshift import PushshiftApi

# UTC
DATE_FROM = 1609459200
DATE_TO = 1622505600

pushshift_api = PushshiftApi()

data = pushshift_api.request_by_hours(DATE_FROM, DATE_TO)

with open('data_{}_{}.json'.format(DATE_FROM, DATE_TO), 'w') as f:
    print("Success! Writing data to data.json...")
    json.dump(data, f, indent=2)