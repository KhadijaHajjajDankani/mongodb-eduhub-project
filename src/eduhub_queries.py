from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["eduhub_db"]

with open("data/sample_data.json") as file:
    data = json.load(file)

for collection, docs in data.items():
    if docs:
        db[collection].insert_many(docs)
        print(f"Inserted {len(docs)} into {collection}")