from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import generate_classroom_activity, get_db_connection

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
#Prevents web pages from making requests to a different domain  - (Cross-Origin Resource Sharing)

@app.route('/generate-activity', methods=['POST'])
def generate_activity():
    try:
        data = request.json
        topic = data.get("topic", "")
        grade = data.get("grade", "")
        board = data.get("board", "")

        if not topic or not grade or not board:
            return jsonify({"error": "Topic, grade, and board are required"}), 400

        print(f"Received request for topic: {topic}, Grade: {grade}, Board: {board}")

        # Use helper function to get activity
        activity = generate_classroom_activity(topic, grade, board)

        return jsonify({"activity": activity})

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)