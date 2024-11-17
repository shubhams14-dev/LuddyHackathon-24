from pymongo import MongoClient
from faker import Faker
from bson.objectid import ObjectId
from datetime import datetime
import random
import json

fake = Faker()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client['your_database']

PRODUCTS_COLLECTION = 'products'
TEAMS_COLLECTION = 'teams'
CONTACTS_COLLECTION = 'contacts'

# Clear existing data
db[PRODUCTS_COLLECTION].delete_many({})
db[TEAMS_COLLECTION].delete_many({})
db[CONTACTS_COLLECTION].delete_many({})

def generate_teams(num_teams=5):
    teams = []
    for _ in range(num_teams):
        team = {
            "teamId": str(ObjectId()),
            "name": fake.color_name() + " Team",
            "department": fake.job(),
            "location": fake.city(),
            "contacts": []  # Empty list initially
        }
        teams.append(db[TEAMS_COLLECTION].insert_one(team).inserted_id)
    return teams

def generate_contacts(teams, num_contacts=20):
    contacts = []
    for _ in range(num_contacts):
        contact = {
            "contactId": str(ObjectId()),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "chatUsername": fake.user_name(),
            "location": fake.city(),
            "role": fake.job(),
            "title": fake.job(),
            "primaryProductId": random.choice([product['productId'] for product in db[PRODUCTS_COLLECTION].find()]),  # Randomly choose a productId
            "isActive": fake.boolean(),
            "lastActive": fake.date_time_this_year()
        }
        contacts.append(contact)

    # Insert contacts into MongoDB and return the list of ObjectIds
    inserted_contacts = db[CONTACTS_COLLECTION].insert_many(contacts)
    return inserted_contacts.inserted_ids

def generate_products(teams, num_products=10):
    products = []
    for _ in range(num_products):
        product = {
            "productId": str(ObjectId()),
            "name": fake.word(),
            "repositoryName": fake.word() + "-repo",
            "description": fake.sentence(),
            "team": random.choice(teams),
            "createdAt": fake.date_time_this_year(),
            "updatedAt": datetime.now()
        }
        products.append(db[PRODUCTS_COLLECTION].insert_one(product).inserted_id)
    return products

def assign_contacts_to_teams(teams, contacts):
    used_contacts = set()  # Track used contacts

    for team_id in teams:
        num_contacts_for_team = random.randint(0, 4)  # Random number of contacts per team
        team_contacts = random.sample([contact for contact in contacts if contact not in used_contacts], num_contacts_for_team)
        
        # Update team document with assigned contacts
        db[TEAMS_COLLECTION].update_one(
            {"_id": ObjectId(team_id)},
            {"$set": {"contacts": team_contacts}}
        )
        
        # Mark these contacts as used
        used_contacts.update(team_contacts)

def generate_data():
    # Step 1: Generate teams
    teams = generate_teams()
    
    # Step 2: Generate products
    products = generate_products(teams)
    
    # Step 3: Generate contacts, now passing products to assign primaryProductId
    contacts = generate_contacts(teams)
    
    # Step 4: Assign contacts to teams (ensuring each contact is only in one team)
    assign_contacts_to_teams(teams, contacts)
    
    print("Data generated successfully!")

# Function to export data to JSON
def export_data_to_json():
    # Get all teams, products, and contacts from the database
    teams_data = list(db[TEAMS_COLLECTION].find())
    products_data = list(db[PRODUCTS_COLLECTION].find())
    contacts_data = list(db[CONTACTS_COLLECTION].find())

    # Function to recursively convert ObjectId and datetime to string
    def convert_objectid(data):
        if isinstance(data, ObjectId):
            return str(data)  # Convert ObjectId to string
        elif isinstance(data, datetime):
            return data.isoformat()  # Convert datetime to ISO 8601 format string
        elif isinstance(data, dict):
            return {key: convert_objectid(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [convert_objectid(item) for item in data]
        return data

    # Convert ObjectId and datetime fields to strings
    teams_data = [convert_objectid(team) for team in teams_data]
    products_data = [convert_objectid(product) for product in products_data]
    contacts_data = [convert_objectid(contact) for contact in contacts_data]

    # Prepare the final data structure
    final_data = {
        "products": products_data,
        "teams": teams_data,
        "contacts": contacts_data
    }

    # Write to JSON file
    with open("generated_data.json", "w") as f:
        json.dump(final_data, f, indent=4)

    print("Data saved to generated_data.json")


# Run the data generation
generate_data()

# Export the generated data to JSON
export_data_to_json()
