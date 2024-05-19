from pymongo import MongoClient
import os

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI')


def get_database():
    if not MONGO_URI:
        raise Exception("MONGO_URI is not set")

    client = MongoClient(MONGO_URI)
    return client.get_default_database()

db = get_database()
collection = db.scores

def update_player_score(user_name, score):
    collection.update_one({'name': user_name}, {'$max': {'record': score}}, upsert=True)

def get_player_data(user_name):
    return collection.find_one({'name': user_name})
