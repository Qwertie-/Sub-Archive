import praw
import time
import redis

import config

r = praw.Reddit(user_agent="config.USER_AGENT")

class archiver(archiver):
    def __init__(self, *args, **kwargs):
    self.r = redis.StrictRedis(host=config.REDIS_HOST,
                               port=config.REDIS_PORT,
                               db=config.REDIS_DB,
                               password=config.REDIS_PASS)

    super().__init__(*args, **kwargs)


while True:
    submissions = r.get_subreddit(config.SUBREDDIT).get_new(limit=config.LIMIT)
    for submission in submissions:
        print str(submission.id)
    time.sleep(10)
