from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import sqlite3
from datetime import datetime
import os
import urllib.parse

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# ==========================================
# 1. CRASH-PROOF MONGODB SETUP
# ==========================================
RAW_MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")

try:
    if "mongodb+srv://" in RAW_MONGO_URI:
        # Safely extract and escape the password to handle complex special characters
        prefix, rest = RAW_MONGO_URI.split("://", 1)
        user_pass, host_rest = rest.split("@", 1)
        username, password = user_pass.split(":", 1)
        clean_password = urllib.parse.quote_plus(password)
        MONGO_URI = f"{prefix}://{username}:{clean_password}@{host_rest}"
    else:
        MONGO_URI = RAW_MONGO_URI

    # Added a 2-second timeout so it won't hang forever if the cloud is slow
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = mongo_client["churnshield_db"]
    logs_collection = db["activity_logs"]
    
    # Ping the database to force authentication verification
    mongo_client.admin.command('ping')
    print("✅ MongoDB Cloud Connected Successfully!")
except Exception as e:
    print(f"⚠️ MongoDB Connection Blocked: {e}")
    print("🔄 Activating Local Safety Mode (Prevents Render from Crashing).")
    
    # Safe dummy object to trap database inputs so the UI still functions perfectly
    class MockCollection:
        def insert_one(self, doc):
            print(f"[Mock Log Saved Local]: {doc}")
    logs_collection = MockCollection()

# ==========================================
# 2. SQLITE OPERATOR STATE SETUP
# ==========================================
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

# Initialize the SQLite table
init_sqlite()

# ==========================================
# 3. ROUTING & CONTROLLERS
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/current-user')
def get_current_user():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, role, assigned_region FROM managers LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return jsonify({"name": row[0], "role": row[1], "region": row[2]})
        return jsonify({"name": "Guest Operator", "role": "Viewer", "region": "Global"})
    except Exception:
        return jsonify({"name": "Shreya B S", "role": "Senior Account Director", "region": "APAC Region"})

@app.route('/api/churn-prediction')
def get_prediction():
    # Grab user interaction parameters directly from frontend sliders
    tickets = int(request.args.get('tickets', 5))
    clicks = int(request.args.get('clicks', 250))

    # Algorithmic calculation balancing complaints vs software interactions
    base_risk = (tickets * 8) - (clicks / 20) + 30
    churn_percentage = max(2, min(98, round(base_risk, 1)))

    status = "High Risk" if churn_percentage > 50 else "Low Risk"
    message = "Action Required: High risk of cancellation detected by AI!" if churn_percentage > 50 else "Account Stable. Predictive signals clean."

    # Fire telemetry tracking snapshots straight to MongoDB 
    try:
        logs_collection.insert_one({
            "timestamp": datetime.utcnow(),
            "client_name": "Global Logistics Corp",
            "metrics": {"tickets": tickets, "clicks": clicks},
            "risk_score": f"{churn_percentage}%",
            "status": status
        })
    except Exception as log_error:
        print(f"Log interception failure: {log_error}")

    return jsonify({
        "customer_name": "Global Logistics Corp",
        "churn_risk": churn_percentage,
        "status": status,
        "message": message,
        "timestamp": datetime.utcnow().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)