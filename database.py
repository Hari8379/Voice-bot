from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://MongoVoiceAssistant1:MongoVoiceAssistant1@clusterdbvoicebot.vfdos.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDbVoicebot")
db = client["College_department"]
collection = db["AIDS"]

def get_students_by_name(student_name):
    """
    Search for students using case-insensitive substring matching across multiple years.
    Return only Name, Block, Floor, and Room No.
    """
    student_name = student_name.strip().lower()
    year_fields = ["SECONDYEAR", "THIRDYEAR", "FOURTHYEAR"]
    
    matched_students = []
    
    for year_field in year_fields:
        sample_doc = collection.find_one({year_field: {"$exists": True}})  
        if sample_doc and year_field in sample_doc:
            student_records = sample_doc[year_field]
            
            for student in student_records:
                if "NAME" in student and student_name in student["NAME"].strip().lower():
                    matched_students.append({
                        "NAME": student["NAME"],
                        "BLOCK": student["BLOCK"],
                        "FLOOR": student["FLOOR"],
                        "ROOM NO": student["ROOM NO"]
                    })
    
    return matched_students
