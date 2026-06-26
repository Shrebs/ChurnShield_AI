from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# 1. MongoDB Cloud Ingest Setup
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import sqlite3
from datetime import datetime
import os
import urllib.parse # <-- Add this import at the top!

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# 1. MongoDB Cloud Ingest Setup (With Automatic Character Escaping)
RAW_MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")

# If it's a cloud Atlas link, automatically fix any password character errors safely
if "mongodb+srv://" in RAW_MONGO_URI:
    try:
        # Split the link to safely encode the password section
        prefix, rest = RAW_MONGO_URI.split("://", 1)
        user_pass, host_rest = rest.split("@", 1)
        username, password = user_pass.split(":", 1)
        
        clean_password = urllib.parse.quote_plus(password)
        MONGO_URI = f"{prefix}://{username}:{clean_password}@{host_rest}"
    except Exception:
        MONGO_URI = RAW_MONGO_URI # Fallback if string layout is different
else:
    MONGO_URI = RAW_MONGO_URI

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["churnshield_db"]
logs_collection = db["activity_logs"]
# 2. SQLite Profile Infrastructure Setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_sqlite():
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
    cursor.execute("SELECT COUNT(*) FROM managers")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO managers (name, role, assigned_region) VALUES (?, ?, ?)", 
                       ("Shreya B S", "Senior Account Director", "APAC Region"))
        conn.commit()
    conn.close()

init_sqlite()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/current-user')
def get_current_user():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, role, assigned_region FROM managers LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"name": row[0], "role": row[1], "region": row[2]})
    return jsonify({"error": "No active profile found"}), 404

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

# 3. Optimized Production Analytical Endpoint
@app.route('/api/churn-prediction')
def get_prediction():
    # 1. Get numbers from the sliders in the browser
    tickets = int(request.args.get('tickets', 5))
    clicks = int(request.args.get('clicks', 250))

    # 2. Logic: High tickets and Low clicks = High Churn Risk
    # This is a simulation of the ML model's behavior
    base_risk = (tickets * 8) - (clicks / 20) + 30
    churn_percentage = max(2, min(98, round(base_risk, 1))) # Keep it between 2% and 98%

    status = "High Risk" if churn_percentage > 50 else "Low Risk"
    message = "Action Required: AI predicts imminent cancellation!" if churn_percentage > 50 else "Account Stable. No action needed."

    # 3. Log the "Interaction" to MongoDB
    logs_collection.insert_one({
        "timestamp": datetime.utcnow(),
        "action": f"Simulation Run: Tickets={tickets}, Clicks={clicks}, Result={churn_percentage}%"
    })

    return jsonify({
        "churn_risk": churn_percentage,
        "status": status,
        "message": message
    })