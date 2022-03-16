from config import engine
from models import Base, Tweet
from sqlalchemy.orm import sessionmaker
import tweepy
from tweepy import OAuthHandler
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

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)





