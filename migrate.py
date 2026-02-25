import firebase_admin
from firebase_admin import credentials, firestore
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client.contactsdb
mongo_collection = mongo_db.contacts

# Firebase setup
# Replace the path below with your Firebase service account JSON
firebase_cred_path = "firebase-contacts-key.json"
cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred)

fs_db = firestore.client()

# ---------------------------
# Migrate Contacts
# ---------------------------
print("Starting migration...")

contacts_ref = fs_db.collection("contacts")  # Firebase collection
contacts = contacts_ref.stream()

count = 0
for contact in contacts:
    data = contact.to_dict()
    mongo_collection.insert_one(data)
    count += 1
    print(f"Inserted: {data}")

print(f"Migration complete! {count} contacts migrated.")
