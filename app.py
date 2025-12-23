from flask import Flask, render_template, request, jsonify
from ai_engine import analyze_syllabus_and_prioritize, generate_study_plan

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    
    # Get inputs
    syllabus_text = data.get('syllabus_text')
    days = data.get('days')
    hours = data.get('hours')
    
    # Run AI Logic
    ranked_topics = analyze_syllabus_and_prioritize(syllabus_text)
    study_plan = generate_study_plan(ranked_topics, days, hours)
    
    return jsonify({
        "topics": ranked_topics,
        "schedule": study_plan
    })

if __name__ == '__main__':
    # We use port 5001 to match your Mac settings
    app.run(debug=True, port=5003)