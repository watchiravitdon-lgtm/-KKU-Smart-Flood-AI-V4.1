# -*- coding: utf-8 -*-
import os
import joblib
import numpy as np

def predict_risk_v4(rainfall, water_level, humidity, temperature):
    model_path = 'models/flood_model.pkl'
    if not os.path.exists(model_path):
        return "LOW", np.array([[0.9, 0.05, 0.05]])
        
    model = joblib.load(model_path)
    features = np.array([[rainfall, water_level, humidity, temperature]])
    
    pred = model.predict(features)
    probs = model.predict_proba(features)
    return pred, probs

def apply_realtime_safety_layer_v4(model_pred, api_data):
    final_pred = model_pred
    reason = "ประมวลดัชนีชี้วัดผลลัพธ์ผ่านเกณฑ์การเรียนรู้ปกติของโมเดลปัญญาประดิษฐ์"
    
    overbank = api_data.get("overbank_count", 0)
    warning_crit = api_data.get("warning_critical_count", 0)
    
    if overbank > 0 or api_data.get("max_water_level", 0) > 7.5:
        if final_pred != "HIGH":
            final_pred = "HIGH"
            reason = "🛡️ Real-time Safety Layer ปรับระดับเป็น HIGH เนื่องจากตรวจพบภาวะระดับตลิ่งล้นพิกัดหรือระดับน้ำวิกฤตหน้าด่านตรวจ"
    elif warning_crit > 0:
        if final_pred == "LOW":
            final_pred = "MEDIUM"
            reason = "🛡️ Real-time Safety Layer ปรับระดับขึ้นสู่ MEDIUM เพื่อความปลอดภัยสูงสุดจากการเตือนภัยย่อยในโครงข่ายข้อมูล"
            
    return final_pred, reason
