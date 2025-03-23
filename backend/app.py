from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import generate_classroom_activity

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Classroom Backend is running!"})

@app.route("/generate-activity", methods=["POST"])
def generate_activity():
    data = request.json
    topic = data.get("topic", "Default Topic")

    # Get AI-generated classroom activity
    activity = generate_classroom_activity(topic)

    return jsonify({"topic": topic, "activity": activity})

if __name__ == "__main__":
    app.run(debug=True)
