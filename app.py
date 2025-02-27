import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb+srv://MongoVoiceAssistant1:MongoVoiceAssistant1@clusterdbvoicebot.vfdos.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDbVoicebot")
db = client["College_department"]
collection = db["AIDS"]

class InputText(BaseModel):
    text: str

def extract_name_and_reg_no(text):
    """
    Extracts a potential name and register number from the given text.
    """
    # Define regex patterns
    name_pattern = r"\b(?!where|is|who|what|when|why|how)[A-Za-z]+\b"
    reg_no_pattern = r"\b\d{12}\b"  # Example: 810423243047

    # Find matches
    name_matches = re.findall(name_pattern, text, re.IGNORECASE)
    reg_no_match = re.search(reg_no_pattern, text)
    
    # Extract values
    extracted_name = name_matches[-1].capitalize() if name_matches else None
    extracted_reg_no = reg_no_match.group() if reg_no_match else None
    
    return extracted_name, extracted_reg_no

def get_student_details(name, reg_no):
    """
    Search for a student using name or register number and return their details.
    """
    query = {}
    if reg_no:
        query["REGISTER_NUMBER"] = reg_no
    elif name:
        query["NAME"] = {"$regex": name, "$options": "i"}  # Case-insensitive search
    
    student = collection.find_one(query)
    
    if student:
        return {
            "name": student.get("NAME", "Unknown"),
            "register_number": student.get("REGISTER_NUMBER", "Unknown"),
            "floor": student.get("FLOOR", "Unknown"),
            "room_no": student.get("ROOM NO", "Unknown"),
            "department": student.get("DEPARTMENT", "Unknown"),
            "year": student.get("YEAR", "Unknown")
        }
    return None

@app.post("/extract")
def extract_data(input_text: InputText):
    name, reg_no = extract_name_and_reg_no(input_text.text)
    
    if not name and not reg_no:
        raise HTTPException(status_code=400, detail="No valid name or register number found.")
    
    student_details = get_student_details(name, reg_no)
    
    if not student_details:
        raise HTTPException(status_code=404, detail="No student found.")
    
    return student_details

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Ensure PORT is dynamically fetched
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
