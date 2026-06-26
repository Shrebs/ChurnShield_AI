from flask import Flask, render_template, jsonify
import os

# We tell Flask that our HTML/CSS files are located in the frontend folder
app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

@app.route('/')
def home():
    # This renders your index.html page when you go to http://127.0.0.1:5000
    return render_template('index.html')

@app.route('/api/churn-prediction')
def get_prediction():
    # This is a temporary fake API endpoint until we wire up the real ML model
    # It sends data straight to your JavaScript file
    sample_data = {
        "customer_name": "Acme Corp",
        "churn_risk": 82.5,
        "status": "High Risk",
        "message": "Action Required: High risk of cancellation!"
    }
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(debug=True)