# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

def train_flood_model_v4():
    data_path = 'data/flood_data.csv'
    if not os.path.exists(data_path):
        from generate_data import generate_synthetic_data_v4
        generate_synthetic_data_v4()
        
    df = pd.read_csv(data_path)
    
    X = df[['Rainfall_mm', 'Water_Level_m', 'Humidity_percent', 'Temperature_C']]
    y = df['Risk']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=2026, stratify=y
    )
    
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"=== Model V4 Performance ===")
    print(f"Accuracy: {acc:.4f}")
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/flood_model.pkl')
    
    metrics_summary = {
        "accuracy": float(acc),
        "n_estimators": 150,
        "total_rows": int(len(df))
    }
    with open('models/model_metrics.json', 'w') as f:
        json.dump(metrics_summary, f)
        
    importances = model.feature_importances_
    features = ['Rainfall', 'Water Level', 'Humidity', 'Temperature']
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(8, 5))
    plt.bar([features[i] for i in indices], importances[indices], color='#2c3e50', edgecolor='black')
    plt.title('Feature Importance (V4.0 Prototype)')
    plt.ylabel('Score')
    plt.tight_layout()
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/feature_importance.png')
    plt.close()
    print("เซฟไฟล์โมเดลและรูปภาพวิเคราะห์ความต้องการตัวแปรเสร็จสิ้น")

if __name__ == "__main__":
    train_flood_model_v4()
