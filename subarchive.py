import praw
import time
import redis
import subprocess
import os

import config

r = praw.Reddit(user_agent=config.USER_AGENT) #Make connection to reddit

class Archiver():
    '''
    *   Redis is used to find the IPFS hash for a post using its post ID
    *   Connection to redis made here
    *   Disabled for now
    def __init__(self, *args, **kwargs):
        self.r = redis.StrictRedis(host=config.REDIS_HOST,
                               port=config.REDIS_PORT,
                               db=config.REDIS_DB,
                               password=config.REDIS_PASS)

        super().__init__(*args, **kwargs)
    '''

    def fetch(self):
        #Used to find posts within a time frame
        current_time = int(time.time())
        #Try to get the newest posts. There should be a better way to do this
        submissions = r.get_subreddit(config.SUBREDDIT).get_new(limit=config.LIMIT)
        posts_in_timeframe = [] #Using posts from 1 day ago to avoid archiveing spam and other junk
        for submission in submissions:
            sub_age = (current_time - submission.created_utc) / 60 / 60 / 24
            if sub_age > 1 and sub_age < 2:
                posts_in_timeframe.append([submission.id,submission.url])
        self.download(posts_in_timeframe)

    '''
    Downloads the page linked on reddit
    Input: [reddit post id, url]
    '''
    def download(self, posts_in_timeframe):
        if not os.path.exists("/tmp/subarchive"):
            os.mkdir("/tmp/subarchive")
        for post in posts_in_timeframe:
            if not os.path.exists("/tmp/subarchive/" + post[0]):
                os.mkdir("/tmp/subarchive/" + post[0])
                subprocess.call("wget -q --show-progress --page-requisites --html-extension --convert-links --random-wait -e robots=off -nd --span-hosts -P /tmp/subarchive/" + post[0] + " " + post[1], shell=True)
            self.publish(post[0])

    def publish(self, ID):
        subprocess.call("ipfs add -r /tmp/subarchive/" + ID, shell=True)

def main():
    archive = Archiver()
    while True:
        archive.fetch()
        time.sleep(config.REFRESH_TIME)

if __name__ == "__main__":
    main()
