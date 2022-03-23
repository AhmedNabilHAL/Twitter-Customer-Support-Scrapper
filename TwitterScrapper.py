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

    def constructRowDict(self, message, reply):

        return {
            'message': message['text'],
            'created_at': message['created_at'],
            'conversation_id': message['conversation_id'],
            'reply': reply['text'],
            'reply_created_at': reply['created_at']
        }

    def scrapeData(self, query, start_time=None, end_time=None):
        client = tw.Client(bearer_token=self.bearer_token, consumer_key=self.consumer_key,
         consumer_secret=self.consumer_secret, access_token=self.access_token,
          access_token_secret=self.access_token_secret)

        df = pd.DataFrame()
        
        try:
            tweets = client.search_recent_tweets(query=f'@{query}',
             tweet_fields=self.fields,
              sort_order='relevancy', start_time=start_time, end_time=end_time)

            replier_id = client.get_user(username=query).data['id']

            if tweets.data is None:
                return df
            
            for tweet in tweets.data:
                # tweet_dict = self.extractTweetDict(tweet)

                if tweet['in_reply_to_user_id'] is not None:
                    continue

                conversation_id = tweet['conversation_id']
                author_id = tweet['author_id']
                conversation = client.search_recent_tweets(query=f'conversation_id:{conversation_id}', 
                    tweet_fields=self.fields)
                
                if conversation.data is None:
                    continue 

                # df = pd.concat([df, pd.DataFrame(tweet_dict, index=[0])], ignore_index=True)
                foundAuthorMsg = True
                authorMsg = tweet
                for reply in reversed(conversation.data):
                    # tweet_dict = self.extractTweetDict(reply)

                    # df = pd.concat([df, pd.DataFrame(tweet_dict, index=[0])], ignore_index=True)
                    if foundAuthorMsg is True and reply['author_id'] == replier_id:
                        row = self.constructRowDict(authorMsg, reply)
                        df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)
                        foundAuthorMsg = False
                    elif foundAuthorMsg is False and reply['author_id'] == author_id:
                        foundAuthorMsg = True
                        authorMsg = reply

                    

        except BaseException as e:
            print('failed on_status, ', str(e))
        
        return df

