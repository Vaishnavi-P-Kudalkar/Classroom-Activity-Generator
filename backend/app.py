from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import generate_classroom_activity, get_db_connection
from flask import send_file
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/generate-activity', methods=['POST'])
def generate_activity():
    try:
        data = request.json
        topic = data.get("topic", "")
        grade = data.get("grade", "")
        board = data.get("board", "")
        location = data.get("location", "")

        if not topic or not grade or not board:
            return jsonify({"error": "Topic, grade, and board are required"}), 400

        print(f"Received request for topic: {topic}, Grade: {grade}, Board: {board}, Location: {location}")

        activity = generate_classroom_activity(topic, grade, board, location)

        return jsonify({"activity": activity})

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500



@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()
    activity_text = data.get('activity', 'No activity content provided.')

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 12)

    # Break long lines for readability
    y = 800
    for line in activity_text.split('\n'):
        lines = [line[i:i+100] for i in range(0, len(line), 100)]
        for l in lines:
            pdf.drawString(40, y, l)
            y -= 15
            if y <= 40:
                pdf.showPage()
                y = 800

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='classroom_activity.pdf', mimetype='application/pdf')



@app.route('/list-activities', methods=['GET'])
def list_activities():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, topic, grade, board, activity, timestamp FROM activities ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        activities = [
            {
                "id": row["id"],
                "topic": row["topic"],
                "grade": row["grade"],
                "board": row["board"],
                "activity": row["activity"],
                "timestamp": row["timestamp"]
            }
            for row in rows
        ]

        conn.close()
        return jsonify({"activities": activities}), 200

    except Exception as e:
        print(f"Error listing activities: {e}")
        return jsonify({"error": "Unable to fetch activities", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
