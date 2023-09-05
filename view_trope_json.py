from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client['json_database']
collection = db['json_collection']

with open('\data\test_all_examples_only_pairs.json') as f:
    file_data = json.load(f)

if isinstance(file_data, dict):
    collection.insert_one(file_data)
else:
    collection.insert_many(file_data)

for doc in collection.find():
    print(doc)