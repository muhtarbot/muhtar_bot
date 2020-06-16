import praw
import pymongo


reddit_oauth_info = {
    "client_id": "UPcRJVXl5F2lcw",
    "client_secret": "XE-u8C4aQa2invI8CDMfvKVrUoo",
    "password": "wassup_89MUHTAR",
    "user_agent": "ubuntu:muhtar_bot:0.0.1 (by u/Salyangoz)",
    "username": "muhtar_bot"
}
 /home/snn/.pyenv/shims/python
def connect_mongodb():
# default port 27017
    pass

def main():
    session = Session
    path_to_certificate = "/mnt/c/Users/snn/Documents/projects/muhtar_bot/certificates/certfile.pem"
    session.verify = path_to_certificate

    reddit_oauth_info['requestor_kwargs'] = {"session": session}

    import pdb; pdb.set_trace()  # breakpoint 6a4608ad //
    reddit = praw.Reddit( **reddit_oauth_info
    #     client_id="CLIENT_ID", client_secret="CLIENT_SECRET",
    #     password="PASSWORD", user_agent="USERAGENT",
    #     username="USERNAME"
    )

    # ======= debug
    for moderator in reddit.subreddit("redditdev").moderator():
        print(moderator)
    # ======= debug


if name == "__main__":
    main()
