import praw
import time
import redis

import config

r = praw.Reddit(user_agent=config.USER_AGENT) #Make connection to reddit

class archiver():
    '''
    *   Redis is used to find the IPFS hash for a post using its post ID
    *   Connection to redis made here
    '''
    def __init__(self, *args, **kwargs):
        self.r = redis.StrictRedis(host=config.REDIS_HOST,
                               port=config.REDIS_PORT,
                               db=config.REDIS_DB,
                               password=config.REDIS_PASS)

        super().__init__(*args, **kwargs)


while True:
    #Try to get the newest posts. There should be a better way to do this
    submissions = r.get_subreddit(config.SUBREDDIT).get_new(limit=config.LIMIT)
    for submission in submissions:
        print str(submission.id) #Just used for debuging now
    time.sleep(10)
