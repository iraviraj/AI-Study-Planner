import google.generativeai as genai
import json
import os

# 👇 YOUR KEY
API_KEY = "YOUR_API_KEY_HERE_FOR_TESTING" 

genai.configure(api_key=API_KEY)

def get_working_model():
    """
    Tries to find a model that actually works for this key.
    This solves the 404 error by trying different valid names.
    """
    # Priority list of models to try
    model_names = [
        'gemini-1.5-flash',       # Best (High limits)
        'gemini-flash-latest',    # Alias for Flash
        'gemini-1.5-flash-001',   # Specific version
        'gemini-pro',             # Standard fallback
        'gemini-1.0-pro'          # Oldest reliable version
    ]
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # Quick test to see if it works
            model.generate_content("test")
            print(f"✅ CONNECTED TO: {name}") # Look for this in your terminal!
            return model
        except Exception:
            continue # Try the next one
            
    print("❌ ALL MODELS FAILED. Check API Key.")
    return None

# Initialize the working model once
model = get_working_model()

def analyze_syllabus_and_prioritize(syllabus_text):
    if not model: return [] # If connection failed, return empty
    if not syllabus_text: return []
    
    print(f"🧠 AI Analyzing: {syllabus_text[:30]}...")
    
    prompt = f"""
    Analyze this syllabus. Break it into topics.
    Output STRICT JSON format:
    [ {{"topic": "Name", "priority": "High/Medium/Low", "reasoning": "Short reason"}} ]
    
    SYLLABUS: {syllabus_text}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        print(f"❌ GENERATION ERROR: {e}")
        return []

def generate_study_plan(topics_data, days_left, daily_hours):
    if not model: return []
    if not topics_data: return []
    
    print(f"📅 Generating Plan for {days_left} days...")
    
    prompt = f"""
    Create a {days_left}-day study plan ({daily_hours} hours/day).
    Topics: {json.dumps(topics_data)}
    Output STRICT JSON format:
    [ {{"day": 1, "focus": "Topic Name", "hours": 2, "activity": "Specific task"}} ]
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        print(f"❌ PLAN ERROR: {e}")
        return []