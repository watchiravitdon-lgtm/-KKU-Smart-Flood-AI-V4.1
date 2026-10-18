# -*- coding: utf-8 -*-
import requests
import pandas as pd

PROVINCE_COORDINATES = {
    "ขอนแก่น": {"lat": 16.4322, "lon": 102.8236},
    "กรุงเทพมหานคร": {"lat": 13.7563, "lon": 100.5018},
    "เชียงใหม่": {"lat": 18.7883, "lon": 98.9853},
    "นครราชสีมา": {"lat": 14.9799, "lon": 102.0978},
    "อุบลราชธานี": {"lat": 15.2287, "lon": 104.8564},
    "ชลบุรี": {"lat": 13.3611, "lon": 100.9847},
    "ภูเก็ต": {"lat": 7.8804, "lon": 98.3922},
}

ALL_PROVINCES = [
    "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", 
    "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", 
    "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", 
    "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", 
    "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "ภูเก็ต", 
    "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", 
    "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", "สมุทรสงคราม", 
    "สมุทรสาคร", "สระแก้ว", "สระบุรี", "สิงห์บุรี", "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", 
    "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อุดรธานี", "อุทัยธานี", "อุตรดิตถ์", "อุบลราชธานี", "อำนาจเจริญ"
]

def get_province_coords(province_name):
    if province_name in PROVINCE_COORDINATES:
        return PROVINCE_COORDINATES[province_name]
    return {"lat": 15.0, "lon": 101.0}

def get_wmo_weather_desc(code):
    mapping = {
        0: "ท้องฟ้าแจ่มใส", 1: "ท้องฟ้าโปร่ง", 2: "ครึ้มบางส่วน", 3: "ท้องฟ้าครึ้ม",
        45: "มีหมอก", 48: "มีหมอกน้ำค้างแข็ง", 51: "ฝนละอองเบาบาง", 53: "ฝนละอองปานกลาง",
        55: "ฝนละอองหนาแน่น", 61: "ฝนตกเล็กน้อย", 63: "ฝนตกปานกลาง", 65: "ฝนตกหนัก",
        80: "ฝนซู่เล็กน้อย", 81: "ฝนซู่ปานกลาง", 82: "ฝนซู่รุนแรง",
        95: "พายุฝนฟ้าคะนอง"
    }
    return mapping.get(code, "แปรปรวนเล็กน้อย")

def fetch_thaiwater_data_v4(province_name):
    try:
        base_coords = get_province_coords(province_name)
        mock_station_data = [
            {"station_name": f"สถานีหลัก{province_name} A", "lat": base_coords['lat']+0.01, "lon": base_coords['lon']+0.01, "rain_1h": 4.0, "rain_24h": 55.0, "water_level": 3.8, "status": "warning"},
            {"station_name": f"สถานีตรวจสอบ B", "lat": base_coords['lat']-0.01, "lon": base_coords['lon']-0.02, "rain_1h": 0.0, "rain_24h": 14.5, "water_level": 2.1, "status": "normal"},
            {"station_name": f"สถานีจุดเสี่ยง C", "lat": base_coords['lat']+0.02, "lon": base_coords['lon']-0.01, "rain_1h": 18.5, "rain_24h": 110.0, "water_level": 8.2, "status": "overbank"}
        ]
        
        df = pd.DataFrame(mock_station_data)
        return {
            "rain_1h": float(df["rain_1h"].mean()),
            "rain_24h": float(df["rain_24h"].max()),
            "rain_3d": None, 
            "rain_7d": None,
            "max_water_level": float(df["water_level"].max()),
            "water_trend": "คงที่และเริ่มทรงตัว" if df["water_level"].max() < 5 else "มีระดับเพิ่มสูงขึ้นอย่างมีนัยสำคัญ",
            "overbank_count": int((df["status"] == "overbank").sum()),
            "warning_critical_count": int((df["status"].isin(["warning", "critical"])).sum()),
            "stations_list": mock_station_data
        }
    except Exception:
        return {"rain_1h": 0.0, "rain_24h": 0.0, "rain_3d": None, "rain_7d": None, "max_water_level": 0.0, "water_trend": "ไม่มีข้อมูล", "overbank_count": 0, "warning_critical_count": 0, "stations_list": []}

def fetch_openmeteo_current(province_name):
    coords = get_province_coords(province_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&timezone=Asia%2FBangkok"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            current = res.json().get("current", {})
            return {
                "temperature": current.get("temperature_2m", 28.0),
                "humidity": current.get("relative_humidity_2m", 75.0),
                "precipitation": current.get("precipitation", 0.0),
                "wind_speed": current.get("wind_speed_10m", 2.0)
            }
    except Exception:
        pass
    return {"temperature": 29.0, "humidity": 70.0, "precipitation": 0.0, "wind_speed": 3.0}

def fetch_openmeteo_forecast(province_name):
    coords = get_province_coords(province_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max&timezone=Asia%2FBangkok"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            daily = res.json().get("daily", {})
            forecast_list = []
            for i in range(len(daily.get("time", []))):
                forecast_list.append({
                    "date": daily["time"][i],
                    "weather_desc": get_wmo_weather_desc(daily["weather_code"][i]),
                    "temp_max": daily["temperature_2m_max"][i],
                    "temp_min": daily["temperature_2m_min"][i],
                    "precip_sum": daily["precipitation_sum"][i],
                    "precip_prob": daily["precipitation_probability_max"][i],
                    "wind_speed_max": daily["wind_speed_10m_max"][i]
                })
            return forecast_list
    except Exception:
        pass
    return []
