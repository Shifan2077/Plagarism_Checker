from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    print("Connection successful!")
    print("Databases:", client.list_database_names())
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
