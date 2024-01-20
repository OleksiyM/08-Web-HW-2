from pymongo.mongo_client import MongoClient
import os

from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')


URI = f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority'

# uri = "mongodb+srv://<username>:<password>@cluster0.vhirvg8.mongodb.net/?retryWrites=true&w=majority"


if __name__ == '__main__':
    client = MongoClient(URI)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
