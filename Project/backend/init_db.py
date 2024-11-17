import sqlite3
import json
from datetime import datetime

# Load the JSON file with the dataset
def load_json_file():
    with open("generated_data.json") as f:
        return json.load(f)

# Initialize the database with the new schema and insert data
def init_db(data):
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Contacts")
    cursor.execute("DROP TABLE IF EXISTS Products")
    cursor.execute("DROP TABLE IF EXISTS Team")

    # Create the Product table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            productId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            repositoryName TEXT NOT NULL,
            description TEXT,
            createdAt TEXT,
            updatedAt TEXT
        )
    """)

    # Create the Team table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teams (
            teamId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    # Create the Contact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contacts (
            contactId TEXT PRIMARY KEY,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            email TEXT NOT NULL,
            chatUsername TEXT NOT NULL,
            location TEXT NOT NULL,
            role TEXT NOT NULL,
            title TEXT NOT NULL,
            primaryProductId TEXT,
            isActive BOOLEAN,
            lastActive TEXT,
            FOREIGN KEY (primaryProductId) REFERENCES Products (productId)
        )
    """)

    # Insert Product data
    for product in data['products']:
        cursor.execute("""
            INSERT OR REPLACE INTO Products (productId, name, repositoryName, description, createdAt, updatedAt)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product["productId"], product["name"], product["repositoryName"], product["description"],
            product["createdAt"], product["updatedAt"]
        ))

    # Insert Team data (after ensuring Products are inserted)
    for team in data['teams']:
        cursor.execute("""
            INSERT OR REPLACE INTO Teams (teamId, name, department, location)
            VALUES (?, ?, ?, ?)
        """, (
            team["teamId"], team["name"], team["department"], team["location"]
        ))

    # Insert Contact data (after ensuring Products and Teams are inserted)
    for contact in data['contacts']:
        cursor.execute("""
            INSERT OR REPLACE INTO Contacts (contactId, firstName, lastName, email, chatUsername, location, role, title,
                                             primaryProductId, isActive, lastActive)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            contact["contactId"], contact["firstName"], contact["lastName"], contact["email"], contact["chatUsername"],
            contact["location"], contact["role"], contact["title"], contact["primaryProductId"],
            contact["isActive"], contact["lastActive"]
        ))

    # Commit and close
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Load the data from the JSON file
    data = load_json_file()
    # Initialize the database with the data
    init_db(data)
