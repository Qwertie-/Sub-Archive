import praw
import time
import redis

import config

r = praw.Reddit(user_agent=config.USER_AGENT) #Make connection to reddit

class Archiver():
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

    def fetch(self):
        #Used to find posts within a time frame
        current_time = int(time.time())
        #Try to get the newest posts. There should be a better way to do this
        submissions = r.get_subreddit(config.SUBREDDIT).get_new(limit=config.LIMIT)
        post_ids_in_timeframe = [] #Using posts from 1 day ago to avoid archiveing spam and other junk
        for submission in submissions:
            sub_age = (current_time - submission.created_utc) / 60 / 60 / 24
            if sub_age > 1 and sub_age < 2:
                post_ids_in_timeframe.append(submission.id)
                print(submission.id)

def main():
    archive = Archiver()
    while True:
        archive.fetch()
        time.sleep(10)

if __name__ == "__main__":
    main()
