from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "taskflow-backend"
    })


@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, completed
        FROM tasks
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": row[3]
        })

    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():

    data = request.get_json()

    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING id, title, description, completed
    """, (title, description))

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "completed": row[3]
    }), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    data = request.get_json()

    completed = data.get("completed")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = %s
        WHERE id = %s
        RETURNING id, title, description, completed
    """, (completed, task_id))

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "completed": row[3]
    })


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id
    """, (task_id,))

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task deleted successfully"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )