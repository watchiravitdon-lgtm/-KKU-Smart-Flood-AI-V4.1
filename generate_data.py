# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd

def generate_synthetic_data_v4():
    print("กำลังสร้างข้อมูลจำลองระบบ V4 (Synthetic Dataset)...")
    np.random.seed(2026)
    n_samples = 1500
    
    rainfall = np.random.uniform(0, 480, n_samples)
    water_level = np.random.uniform(0.2, 9.8, n_samples)
    humidity = np.random.uniform(35, 100, n_samples)
    temperature = np.random.uniform(18, 40, n_samples)
    
    data = pd.DataFrame({
        'Rainfall_mm': rainfall,
        'Water_Level_m': water_level,
        'Humidity_percent': humidity,
        'Temperature_C': temperature
    })
    
    risk_labels = []
    for idx, row in data.iterrows():
        base_score = (row['Rainfall_mm'] * 0.45) + (row['Water_Level_m'] * 35) + (row['Humidity_percent'] * 0.15)
        
        if base_score > 240 or row['Rainfall_mm'] > 220 or row['Water_Level_m'] > 7.2:
            risk = "HIGH"
        elif base_score > 120 or row['Rainfall_mm'] > 85 or row['Water_Level_m'] > 4.0:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        risk_labels.append(risk)
        
    data['Risk'] = risk_labels
    
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/flood_data.csv', index=False, encoding='utf-8')
    print(f"สร้างข้อมูลสำเร็จ! บันทึกที่ data/flood_data.csv (จำนวน {n_samples} แถว)")

if __name__ == "__main__":
    generate_synthetic_data_v4()
