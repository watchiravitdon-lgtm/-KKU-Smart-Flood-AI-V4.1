# KKU Smart Flood AI V4.0

### ระบบการคำนวณวิเคราะห์ภัยน้ำท่วมระดับจังหวัดผ่านสถาปัตยกรรมแมชชีนเลิร์นนิงต้นแบบ

---

## 🔬 รายละเอียดเชิงทฤษฎีและกรอบการประเมิน (V4.0 Framework)
* **Dataset Size:** 1,500 Rows คำนวณสร้างด้วยฟังก์ชันความเชื่อมโยงสถิติแบบจำลอง
* **Core Model Algorithm:** Random Forest Classifier (150 Estimators, Max Depth 8)
* **API Modules:** โครงข่ายดึงข้อมูลสภาพอากาศ Open-Meteo ปัจจุบันและการพยากรณ์ล่วงหน้า 7 วันอิงแบบกริดจุดพิกัด

## 🚀 ลำดับขั้นตอนการสั่งงานระบบปฏิบัติการคัดกรอง
1. ติดตั้งแพ็กเกจไลบรารี: `pip install -r requirements.txt`
2. สร้างชุดสถิติจำลองระบบ: `python generate_data.py`
3. ฝึกสอนประเมินผลตัวแบบ: `python train_model.py`
4. รันระบบแสดงอินเตอร์เฟซแอปพลิเคชัน: `streamlit run app.py`
