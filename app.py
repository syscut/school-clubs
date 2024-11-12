from flask import Flask, send_from_directory, jsonify, request
import os
import sqlite3

conn = sqlite3.connect('flight.db')
app = Flask(__name__)

def get_all_scores():

    conn = sqlite3.connect('flight.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM score")
    rows = cursor.fetchall()

    # 將紀錄轉換成 JSON 格式
    score_list = []
    for row in rows:
        score_record = {
            "id": row[0],
            "studentId": row[1],
            "score": row[2],
            "comment": row[3]
        }
        score_list.append(score_record)

    conn.close()

    return score_list

def insert_or_update_score(student_id, score):
    conn = sqlite3.connect('flight.db')
    cursor = conn.cursor()

    # 轉換 student_id 為大寫
    student_id = student_id.upper()

    # 檢查 studentId 是否已存在
    cursor.execute("SELECT id FROM score WHERE studentId = ?", (student_id,))
    record = cursor.fetchone()

    if record:
        # 若 studentId 存在，則進行更新
        cursor.execute("UPDATE score SET score = ? WHERE studentId = ?", (score, student_id))
        message = "Updated existing record."
    else:
        # 若 studentId 不存在，則插入新記錄
        cursor.execute("INSERT INTO score (studentId, score) VALUES (?, ?)", (student_id, score))
        message = "Inserted new record."

    conn.commit()
    conn.close()

    return message


# Replace 'your_directory' with the directory where your ZIP is extracted
your_directory = os.path.join(os.getcwd(), "Project")

@app.route('/')
def index():
    # Serve index.html from the extracted directory
    return send_from_directory(your_directory, 'index.html')

@app.route('/allScore')
def scores():
    scores = get_all_scores()
    return jsonify(scores)

@app.route('/update')
def update_score():
    student_id = request.args.get('studentId')
    score = request.args.get('score', type=int)

    if not student_id or score is None:
        return jsonify({"error": "Missing studentId or score"}), 400

    message = insert_or_update_score(student_id, score)
    return jsonify({"message": message})

@app.route('/<path:filename>')
def serve_file(filename):
    # Serve other files (like JS, CSS) from the extracted directory
    return send_from_directory(your_directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)