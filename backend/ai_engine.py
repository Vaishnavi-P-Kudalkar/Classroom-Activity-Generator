import sqlite3
import requests
import os
import json
import time
from googletrans import Translator  # Make sure this is installed: pip install googletrans==4.0.0-rc1

def get_db_connection():
    db_path = os.path.abspath("database.db")
    print(f"Using database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        grade TEXT NOT NULL,
        board TEXT NOT NULL,
        activity TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    
    return conn

def generate_complexity_instructions(grade, board):
    complexity_map = {
        '1-3': {
            'CBSE': "Use simple language, focus on basic concepts, include lots of visual aids and hands-on activities.",
            'ICSE': "Emphasize foundational understanding with interactive and playful learning approaches.",
            'State': "Use local context and simple, concrete examples that students can easily relate to."
        },
        '4-6': {
            'CBSE': "Introduce more structured learning, include basic analytical thinking, use step-by-step explanations.",
            'ICSE': "Encourage critical thinking, provide slightly more complex explanations with real-world connections.",
            'State': "Balance between local context and broader understanding, use engaging visual representations."
        },
        '7-10': {
            'CBSE': "Focus on in-depth understanding, include advanced concepts, encourage scientific reasoning and research.",
            'ICSE': "Promote advanced analytical skills, include complex problem-solving and interdisciplinary connections.",
            'State': "Provide comprehensive understanding with advanced local and global perspectives."
        }
    }
    
    grade_range = '1-3' if int(grade) <= 3 else '4-6' if int(grade) <= 6 else '7-10'
    return complexity_map.get(grade_range, {}).get(board, "Create an engaging and age-appropriate educational activity.")

def detect_target_language(location_str):
    location_str = location_str.lower()
    if "karnataka" in location_str:
        return "kn"
    elif "tamil nadu" in location_str:
        return "ta"
    elif "maharashtra" in location_str:
        return "mr"
    elif "telangana" in location_str:
        return "te"
    elif "kerala" in location_str:
        return "ml"
    else:
        return "en"

def generate_classroom_activity(topic, grade, board, location=""):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check cache
    cursor.execute("SELECT activity FROM activities WHERE topic = ? AND grade = ? AND board = ?", 
                   (topic.lower(), grade, board))
    cached = cursor.fetchone()
    if cached:
        print(f"Found cached activity for '{topic}' in grade {grade}, {board} board")
        conn.close()
        return cached[0]

    print(f"Generating new activity for '{topic}' in grade {grade}, {board} board")

    complexity_instructions = generate_complexity_instructions(grade, board)

    prompt = f"""
    Create an engaging, educational classroom activity about "{topic}" for {grade}th grade students following {board} board curriculum.

    Complexity Guidelines: {complexity_instructions}

    Activity Requirements:
    - Align with {grade}th grade learning capabilities
    - Match {board} board educational standards
    - Interactive and hands-on
    - 20-30 minutes in length
    - Include clear steps for the teacher to follow

    Respond *only* in the following format using section headers (###):

    ### Title
    [Your title here]

    ### Learning Objectives
    - Objective 1
    - Objective 2

    ### Materials Needed
    - Item 1
    - Item 2

    ### Instructions
    1. Step 1
    2. Step 2

    ### Assessment
    [Describe assessment or reflection method]
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a creative educator generating classroom activities."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        activity = result["choices"][0]["message"]["content"].strip()

        # Clean extra sections
        def clean_activity_response(activity_text):
            expected_sections = ["### Title", "### Learning Objectives", "### Materials Needed", "### Instructions", "### Assessment"]
            sections = activity_text.split("###")
            cleaned_sections = []
            for section in sections:
                section = section.strip()
                if any(section.startswith(title.replace("### ", "")) for title in expected_sections):
                    cleaned_sections.append("### " + section)
            return "\n\n".join(cleaned_sections)

        activity = clean_activity_response(activity)

    except Exception as e:
        print(f"Exception during OpenRouter API call: {str(e)}")
        activity = f"""
        ### Title
        Creative {topic.title()} Challenge

        ### Learning Objectives
        - Understand key concepts related to {topic}
        - Collaborate with peers to create visual representations

        ### Materials Needed
        - Chart paper
        - Markers
        - Reference books

        ### Instructions
        1. Divide class into small groups.
        2. Each group researches a different aspect of {topic}.
        3. They create a poster or model.
        4. Present to the class.

        ### Assessment
        Evaluate based on understanding, teamwork, and creativity.
        """

    # Translate if needed
    target_lang = detect_target_language(location)
    if target_lang != "en":
        try:
            translator = Translator()
            translated = translator.translate(activity, src='en', dest=target_lang)
            activity = translated.text
            print(f"Translated to {target_lang}")
        except Exception as e:
            print(f"Translation error: {e} — using English version.")

    # Save to DB
    cursor.execute(
        "INSERT INTO activities (topic, grade, board, activity) VALUES (?, ?, ?, ?)", 
        (topic.lower(), grade, board, activity)
    )
    conn.commit()
    conn.close()
    return activity
