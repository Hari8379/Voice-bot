from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from nlp_processing import extract_name

app = Flask(__name__)

# Allow CORS for a specific frontend URL
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to MongoDB
client = MongoClient("mongodb+srv://MongoVoiceAssistant1:MongoVoiceAssistant1@clusterdbvoicebot.vfdos.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDbVoicebot")
db = client["College_department"]
collection = db["AIDS"]

def get_student_details(student_name):
    """
    Search for a student using case-insensitive partial matching
    and return their Block, Floor, and Room Number.
    """
    student_name = student_name.strip().lower()  # Normalize input
    year_fields = ["SECONDYEAR", "THIRDYEAR", "FOURTHYEAR"]

    for year_field in year_fields:
        sample_doc = collection.find_one({year_field: {"$exists": True}})
        if sample_doc and year_field in sample_doc:
            student_records = sample_doc[year_field]
            
            # Search for a matching student (case-insensitive)
            matched_students = [
                {
                    "name": s["NAME"],
                    "block": s.get("BLOCK", "Unknown"),
                    "floor": s.get("FLOOR", "Unknown"),
                    "room_no": s.get("ROOM NO", "Unknown"),
                    "year": year_field,  # Include year for reference
                    "department": s.get("DEPARTMENT", "Unknown")
                }
                for s in student_records
                if "NAME" in s and student_name in s["NAME"].strip().lower()
            ]
            
            if matched_students:
                return matched_students  # Return all matching students

    return []  # Return empty list if no match found

@app.route("/")
def home():
    return jsonify({"message": "Voice Search Backend is Running!"})

@app.route('/process_voice', methods=['POST'])
def process_voice():
    """
    Extract the name from text and retrieve student details from the database.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Try again"}), 400

    user_input = data['text']
    extracted_name = extract_name(user_input)

    if not extracted_name:
        return jsonify({"error": "No name found"}), 404

    students = get_student_details(extracted_name.lower())  # Ensure lowercase matching
    
    if not students:
        return jsonify([]), 200  # Return an empty list with HTTP 200 OK
    
    return jsonify(students)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
