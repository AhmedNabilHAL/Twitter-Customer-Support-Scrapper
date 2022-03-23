import pandas as pd

from TwitterScrapper import TwitterScrapper



class ScrapperDriver:
    def __init__(self):
        self.df = pd.DataFrame()
    
    def scrape(self):
        # fields = ['id', 'text', 'author_id', 'created_at', 'conversation_id',
        #  'in_reply_to_user_id', 'context_annotations', 'entities', 'public_metrics']

        fields = ['id', 'text', 'author_id', 'created_at', 'conversation_id',
         'in_reply_to_user_id','public_metrics']

        twitter_scrapper = TwitterScrapper(fields)
        query = '@AmazonHelp'

        self.df = twitter_scrapper.scrapeData(query)

    def save(self, filename='twitter'):
        self.df.to_csv(f'./{filename}.csv', index=False)

def main():
    scrapper = ScrapperDriver()
    scrapper.scrape()
    scrapper.save()

if __name__ == "__main__":
    main()
        

    

