from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import sqlite3
from datetime import datetime
import pickle
import os
import numpy as np

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# 1. MongoDB Setup (Activity Logs)
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["churnshield_db"]
logs_collection = db["activity_logs"]

# 2. SQLite Setup (Structured Account Directories)
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_sqlite():
    """Create a local SQL table and insert a dummy account manager profile if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            assigned_region TEXT NOT NULL
        )
    ''')
    # Check if we already have data, if not insert a test profile
    cursor.execute("SELECT COUNT(*) FROM managers")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO managers (name, role, assigned_region) VALUES (?, ?, ?)", 
                       ("Shreya B S", "Senior Account Director", "APAC Region"))
        conn.commit()
    conn.close()

init_sqlite() # Initialize the database tables on startup

# 3. Load ML Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'churn_model.pkl')
with open(MODEL_PATH, 'rb') as file:
    ml_model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

# NEW API: Fetch who is currently logged into the system from SQLite
@app.route('/api/current-user')
def get_current_user():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Query the first manager profile in our relational table
    cursor.execute("SELECT name, role, assigned_region FROM managers LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "name": row[0],
            "role": row[1],
            "region": row[2]
        })
    return jsonify({"error": "No active user session profile found"}), 404

@app.route('/api/log-activity', methods=['POST'])
def log_activity():
    data = request.get_json()
    log_document = {
        "client_name": data.get("client_name", "Unknown"),
        "action": data.get("action", "Page View"),
        "timestamp": datetime.utcnow()
    }
    logs_collection.insert_one(log_document)
    return jsonify({"status": "success"})

@app.route('/api/churn-prediction')
def get_prediction():
    client_features = np.array([[12, 6, 45, 2]]) 
    prediction = ml_model.predict(client_features)[0]
    probabilities = ml_model.predict_proba(client_features)[0]
    churn_percentage = round(probabilities[1] * 100, 1)

    status = "High Risk" if prediction == 1 else "Low Risk"
    message = "Action Required: High risk of cancellation detected by AI!" if prediction == 1 else "Account Stable."

    return jsonify({
        "customer_name": "Global Logistics Corp",
        "churn_risk": churn_percentage,
        "status": status,
        "message": message
    })

if __name__ == '__main__':
    app.run(debug=True)