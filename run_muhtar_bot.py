import time
from datetime import datetime

import praw
from pymongo import MongoClient, InsertOne, UpdateOne
from requests import Session


reddit_oauth_info = {
    "client_id": "x1P4KVO8nIt1gw",
    "client_secret": "3m7cQ6ZH9xjLpE40ywpdlBDy8FE",
    "password": "wassup_89MUHTAR",
    "user_agent": "ubuntu:muhtar_bot:0.0.1 (by u/Salyangoz)",
    "username": "muhtar_bot"
}

DB_NAME = 'mahalle_db_ristanbul'
DB_URL = 'mongodb://localhost:27017/'

def connect_mongodb():
    client = MongoClient(DB_URL)
    mongodb = client[DB_NAME]
    return mongodb

def bulk_write(db, submissions):
    bulk_op_counter = 0

    bulk_write_list = []
    # author_ids = [submission.author.id for submission in submissions]

    for submission in submissions:
        author = submission.author
        url = submission.url
        now = datetime.utcnow().timestamp()

        metadata = {
            "author_id": author.id,
            "post_count": 1,
            "author": {
                "name": author.name,
                "comment_karma": author.comment_karma,
                "link_karma": author.link_karma,
                },
            "time_posted": str(submission.created_utc),
            "time_added_to_muhtar": str(now)
        }

        bulk_write_list.append(InsertOne(metadata))

    # UpdateOne({'author_id': 4}, {'$inc': {'post_count': 1}}),
    # # UpdateOne({'author_id': 4}, {}, upsert=True)
    # InsertOne({})

    import pdb; pdb.set_trace()  # breakpoint 7dcab235 //

    # for moderator in reddit.subreddit("redditdev").moderator():
    #     print(moderator)
    # ======= debug
    result = db[DB_NAME].bulk_write(bulk_write_list)

    # for a_id in ids:
    #     {'author_id': a_id}, {'$inc': {'item': 1}}
    #     # process in bulk
    #     bulk.find({ '_id': id }).update({ '$set': { 'isBad': 'N' } })
    #     bulk_op_counter += 1

    #     if (bulk_op_counter % 500 == 0):
    #         bulk.execute()
    #         bulk = db.testdata.initialize_ordered_bulk_op()

    # if (bulk_op_counter % 500 != 0):
    #     bulk.execute()


def main():
    # session = Session
    # path_to_certificate = "/mnt/c/Users/snn/Documents/projects/muhtar_bot/certificates/certfile.pem"
    # session.verify = path_to_certificate

    mongodb = connect_mongodb()
    reddit = praw.Reddit(**reddit_oauth_info)

    # ======= debug
    print("===========================")
    print(reddit.user.me())

    submissions = reddit.subreddit("istanbul").new()

    author_inserts = []
    author_updates = []
    archive_upserts = []

    result = bulk_write(mongodb, submissions)
    import pdb; pdb.set_trace()  # breakpoint bafa1701 //

    # mongodb.bulk_write(InsertOne(author_inserts))
    # mongodb.bulk_write(UpdateOne(author_updates))

if __name__ == '__main__':
    main()

