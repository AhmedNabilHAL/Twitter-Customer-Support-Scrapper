from dotenv import load_dotenv
import tweepy as tw
import pandas as pd
import os



class TwitterScrapper:
    def __init__(self, fields):
        load_dotenv()
        self.consumer_key = os.environ.get('consumer_key')
        self.consumer_secret = os.environ.get('consumer_secret')
        self.access_token = os.environ.get('access_token')
        self.access_token_secret = os.environ.get('access_token_secret')
        self.bearer_token = os.environ.get('bearer_token')
        self.fields = fields

    def extractTweetDict(self, tweet):
        tweet_dict = {}
        
        for field in self.fields:
            if isinstance(tweet[field], dict):
                for key in tweet[field]:
                    tweet_dict[key] = tweet[field][key]
            
            else:
                tweet_dict[field] = tweet[field]
        
        return tweet_dict

    def scrapeData(self, query, start_time=None, end_time=None):
        client = tw.Client(bearer_token=self.bearer_token, consumer_key=self.consumer_key,
         consumer_secret=self.consumer_secret, access_token=self.access_token,
          access_token_secret=self.access_token_secret)

        df = pd.DataFrame()
        
        try:
            tweets = client.search_recent_tweets(query=query,
             tweet_fields=self.fields,
              sort_order='relevancy', start_time=start_time, end_time=end_time, max_results=10)

            if tweets.data is None:
                return df
            
            for tweet in tweets.data:
                tweet_dict = self.extractTweetDict(tweet)

                conversation_id = tweet_dict['conversation_id']
                conversation = client.search_recent_tweets(query=f'conversation_id:{conversation_id}', 
                    tweet_fields=self.fields)
                
                if conversation.data is None:
                    continue 

                df = pd.concat([df, pd.DataFrame(tweet_dict, index=[0])], ignore_index=True)

                for reply in conversation.data:
                    tweet_dict = self.extractTweetDict(reply)

                    df = pd.concat([df, pd.DataFrame(tweet_dict, index=[0])], ignore_index=True)

        except BaseException as e:
            print('failed on_status, ', str(e))
        
        return df

