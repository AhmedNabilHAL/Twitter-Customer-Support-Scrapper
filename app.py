from sqlalchemy.orm import sessionmaker
import tweepy as tw
import pandas as pd
import time
from dotenv import load_dotenv
import os
# Session = sessionmaker(bind=engine)
# session = Session()



# session.close()
load_dotenv()

api_key = os.environ.get("api_key")
api_secret = os.environ.get("api_secret")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")

auth = tw.OAuthHandler(api_key , api_secret)
auth.set_access_token(access_token , access_token_secret)

api = tw.API(auth , wait_on_rate_limit=True)

search_words = "#amazon"
date_since = "2020-2-17"

# Collect tweets
tweets = tw.Cursor(api.search_tweets ,
              q=search_words,
              lang="en",
              since=date_since).items(1000)


for tweet in tweets:
    print(tweet.text)


