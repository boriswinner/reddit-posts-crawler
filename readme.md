# [WIP] Reddit crawler

This is a Reddit crawler. It crawls a specific subreddit for posts and comments (plain text) for future analysis and saves them to JSON.

It doesn't have a nice interface yet.

```Redditapi.py``` is not used now, don't touch it!

How to use?
1. ```pip install praw```
2. ```pip install tqdm```
3. Go to ```https://www.reddit.com/prefs/apps```, create an app (```https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c```, section "Getting Access")
4.  In ```psaw_reddit.py``` paste your client id and secret token (lines 4,5) and change user agent (line 11)
5. In ```pushshift.py``` set value of ```SUBREDDIT``` (the subreddit that it will crawl)
6. In main.py set ```DATE_FROM```, ```DATE_TO``` (UTC format)
7. Run main.py

The output should look like:
```
Requesting data starting at Fri Jan  1 03:00:00 2021...
Processing posts within time range... : 100%|██████████| 6/6 [00:34<00:00,  6.52s/it]
Proccessed 4 items.
Requesting data starting at Fri Jan  1 03:30:00 2021...
Processing posts within time range... : 100%|██████████| 1/1 [00:00<00:00, 1000.07it/s]
Proccessed 0 items.
Requesting data starting at Fri Jan  1 04:00:00 2021...
Processing posts within time range... : 100%|██████████| 9/9 [00:18<00:00,  2.09s/it]
Proccessed 2 items.
```

