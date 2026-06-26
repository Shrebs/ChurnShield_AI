import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_enterprise_model():
    print("🤖 Phase 3: Initializing Machine Learning Model Training pipeline...")
    
    # 1. GENERATE MOCK ENTERPRISE DATA
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'months_active': np.random.randint(1, 36, n_samples),
        'support_tickets_opened': np.random.randint(0, 10, n_samples),
        'monthly_clicks_logged': np.random.randint(10, 500, n_samples),
        'subscription_tier': np.random.choice([1, 2, 3], n_samples) # 1: Free, 2: Premium, 3: Enterprise
    }
    
    df = pd.DataFrame(data)
    
    # Simple rule for Churn: High support tickets + low app clicks = high probability to cancel
    df['churn'] = np.where((df['support_tickets_opened'] > 5) & (df['monthly_clicks_logged'] < 100), 1, 0)
    
    # Add minor noise to make it realistic
    random_noise = np.random.choice([0, 1], size=n_samples, p=[0.92, 0.08])
    df['churn'] = np.bitwise_xor(df['churn'], random_noise)

    # 2. SPLIT DATA INTO FEATURES (X) AND TARGET (Y)
    X = df[['months_active', 'support_tickets_opened', 'monthly_clicks_logged', 'subscription_tier']]
    y = df['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. TRAIN A RANDOM FOREST CLASSIFIER
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"✅ Model Training Complete. Evaluation Accuracy Score: {accuracy * 100:.2f}%")

    # 4. EXPORT AND SERIALIZE THE MODEL
    # This explicit path configuration ensures it creates the folder and file correctly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'churn_model.pkl')
    
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
        
    print(f"💾 Model artifact serialized and saved successfully to: {model_path}")

if __name__ == '__main__':
    train_enterprise_model()