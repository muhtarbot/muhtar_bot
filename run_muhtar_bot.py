import time
import json
from datetime import datetime

import praw
from pymongo import MongoClient, InsertOne, UpdateOne
from requests import Session

TOO_MANY_POSTS_PER_DAY_REPORT_MESSAGE = (
    'I am https://github.com/muhtarbot/muhtar_bot\nThis person is posting too much.'
)
SUBREDDIT_NAME = 'istanbul'
DB_NAME = 'mahalle_db_ristanbul'
DB_URL = 'mongodb://localhost:27017/'
ONE_DAY_SECONDS = 86400


def connect_mongodb():
    client = MongoClient(DB_URL)
    mongodb = client[DB_NAME]
    return mongodb[DB_NAME]

def process_submission(db, submission):
    author = submission.author
    last_post = db.find_one({'author_id': author.id})
    post_count = 0
    if last_post is not None:
        post_count = last_post['post_count'] + 1
        submission_time_delta = submission.created_utc - float(last_post['time_posted'])

        if submission_time_delta > ONE_DAY_SECONDS:
            # they last posted 24 hours ago reset count
            post_count = 0
        if post_count > 3 and submission_time_delta < ONE_DAY_SECONDS:
            # too many posts per day
            submission.report(TOO_MANY_POSTS_PER_DAY_REPORT_MESSAGE)

    now = datetime.utcnow().timestamp()

    if last_post:
        return db.update_one({'author_id': author.id}, {"$set": {
            "post_count": post_count,
            "url": submission.url,
            "time_posted_utc": str(submission.created_utc),
            "time_updated": str(now)
        }})

    metadata = {
        "author_id": author.id,
        "post_count": 1 if post_count == 0 else post_count,
        "author": {
            "name": author.name,
            "comment_karma": author.comment_karma,
            "link_karma": author.link_karma,
            },
        "url": submission.url,
        "time_posted": str(submission.created_utc),
        "time_added_to_muhtar": str(now)
    }
    return db.insert_one(metadata)


def read_reddit_info():
    with open('reddit_oauth_info.json') as f:
        data = json.load(f)
    return data

def main():
    reddit_oauth_info = read_reddit_info()
    reddit = praw.Reddit(**reddit_oauth_info)

    print("===========================")
    print(reddit.user.me())
    print("===========================")

    # submissions = reddit.subreddit("istanbul").new() # for non stream loops
    mongo_mahalle_db = connect_mongodb()
    print('-----------------------------------')
    for submission in reddit.subreddit(SUBREDDIT_NAME).stream.submissions():
        print(submission.url)
        print(submission.author.name)
        result = process_submission(mongo_mahalle_db, submission)
        print(result)
        print('-----------------------------------')


if __name__ == '__main__':
    main()

