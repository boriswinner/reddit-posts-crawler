import praw

class PrawRedditApi:
    def __init__(self):
        self.CLIENT_ID = ""
        self.SECRET_TOKEN = ""

        self.reddit = praw.Reddit(
            client_id=self.CLIENT_ID,
            client_secret=self.SECRET_TOKEN,
            user_agent="BigDataHomework/0.0.1",
        )

    def submission_is_deleted(self, submission):
        return (submission.author is None or
                submission.selftext == '[removed]' or
                submission.selftext == '[deleted]' or
                not submission.selftext or
                not submission.author)

    def get_comments_of_post(self, id):
        submission = self.reddit.submission(id=id)
        if not self.submission_is_deleted(submission):
            submission.comments.replace_more(limit=0) # ignore all comments hidden at "Read more..."
            comments = submission.comments.list()
            return comments
        else:
            return []
