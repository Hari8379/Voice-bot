import re

def extract_name(text):
    """
    Extracts a potential name from a given text using a more flexible approach.
    Ensures case-insensitivity and avoids capturing question words.
    """
    # Define a regex to find words that are likely to be names
    name_pattern = r"\b(?!where|is|who|what|when|why|how)[A-Za-z]+\b"
    matches = re.findall(name_pattern, text, re.IGNORECASE)  # Case-insensitive

    # Return the first meaningful word found, capitalized
    return matches[-1].capitalize() if matches else None

def extract_department_year(text):
    department_keywords = {
        "artificial intelligence and data science": "AI&DS",
        "aids": "AI&DS",
        "computer science": "CSE",
        "cs": "CSE",
        "electronics and communication": "ECE",
        "ece": "ECE"
    }
    
    year_keywords = {
        "first year": "I",
        "second year": "II",
        "third year": "III",
        "fourth year": "IV",
        "1st year": "I",
        "2nd year": "II",
        "3rd year": "III",
        "4th year": "IV"
    }
    
    extracted_department = None
    extracted_year = None

    for key, value in department_keywords.items():
        if key in text.lower():
            extracted_department = value
            break

    for key, value in year_keywords.items():
        if key in text.lower():
            extracted_year = value
            break

    return extracted_department, extracted_year
