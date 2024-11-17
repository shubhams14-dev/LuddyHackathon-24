from flask import Flask, request, jsonify
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute(query, args)
    results = cursor.fetchall()
    conn.close()
    return (results[0] if results else None) if one else results

# Route to insert data from JSON into the database
@app.route("/load_contacts", methods=["POST"])
def load_contacts():
    # Read the JSON file
    try:
        with open("contacts.json", "r") as file:
            contacts_data = json.load(file)
    except Exception as e:
        return jsonify({"error": f"Failed to load JSON file: {str(e)}"}), 500
    
    # Insert data into the database
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    for contact in contacts_data:
        # Prepare the SQL query to insert data into the Contacts table
        query = """
        INSERT INTO Contacts (firstName, lastName, email, chatUsername, location, title, primaryProductId)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            contact['firstName'],
            contact['lastName'],
            contact['email'],
            contact['chatUsername'],
            contact['location'],
            contact['title'],
            contact['primaryProductId']
        ))
    
    conn.commit()  # Commit the transaction
    conn.close()  # Close the connection

    return jsonify({"message": "Contacts loaded successfully!"})

@app.route("/contacts", methods=["GET"])
def get_contact():
    product_name = request.args.get("product_name")
    repository_name = request.args.get("repository_name")

    if not product_name and not repository_name:
        return jsonify({"error": "Provide product_name or repository_name"}), 400

    query = """
        SELECT c.firstName, c.lastName, c.email, c.chatUsername, c.location, c.title
        FROM Contacts c
        JOIN Products p ON c.primaryProductId = p.productId
        WHERE {}
    """.format(
        "p.name = ?" if product_name else "p.repositoryName = ?"
    )

    contacts = query_db(query, (product_name or repository_name,))
    if not contacts:
        return jsonify({"error": "Contact not found"}), 404
    contact1 = contacts[0]
    print(contact1)
    contact = {
        "firstName": contact1[0],
        "lastName": contact1[1],
        "email": contact1[2],
        "chatUsername": contact1[3],
        "location": contact1[4],
        "title": contact1[5],
    }
    return jsonify(contact)

if __name__ == "__main__":
    app.run(debug=True)
