from sqlalchemy import create_engine

# Connect to the database
DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/twitter_scrapper'
engine = create_engine(DATABASE_URI)