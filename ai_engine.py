import google.generativeai as genai
import json
import os

# 👇 YOUR KEY
API_KEY = "PASTE_YOUR_KEY_HERE" 

genai.configure(api_key=API_KEY)

# ✅ USING THE EXACT NAME FROM YOUR LIST
model = genai.GenerativeModel('gemini-flash-latest')

def analyze_syllabus_and_prioritize(syllabus_text):
    if not syllabus_text: return []
    
    prompt = f"""
    Analyze this syllabus. Break it into topics.
    Output STRICT JSON:
    [ {{"topic": "Name", "priority": "High", "reasoning": "..."}} ]
    
    SYLLABUS: {syllabus_text}
    """
    
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        print(f"❌ AI ERROR: {e}")
        return []

def generate_study_plan(topics_data, days_left, daily_hours):
    if not topics_data: return []
    
    prompt = f"""
    Create a {days_left}-day study plan ({daily_hours} hours/day).
    Topics: {json.dumps(topics_data)}
    Output STRICT JSON:
    [ {{"day": 1, "focus": "Topic", "hours": 2, "activity": "Study"}} ]
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        return []