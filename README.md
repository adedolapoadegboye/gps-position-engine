# GPS Positioning System

## 📌 Overview
This program processes real-time GPS data using RTCM messages to estimate the **user's position** and **clock bias**. It utilizes **ephemeris data**, **pseudorange measurements**, and **least-squares estimation** to compute an accurate position in the **WGS-84 coordinate system**.

## 🚀 Features
- Parses **RTCM messages** from a GPS receiver
- Extracts **ephemeris** and **pseudorange data**
- Computes **satellite positions**
- Uses **least-squares estimation** to determine **user position & clock bias**
- Converts **ECEF coordinates to latitude, longitude, and height**
- Computes **HDOP, VDOP** values for positioning accuracy
- Supports **ENU (East-North-Up) transformation** for local reference frame

---

## 📥 Installation
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/gps-position-engine.git
cd gps-position-engine
```

### **2️⃣ Install Dependencies**
Ensure you have Python **3.7+** installed. Then, install the required libraries:
```bash
pip install numpy pyserial
```

---

## 📜 Usage
### **Run the Main Program**
```bash
python main.py
```

The program will:
1. **Read RTCM messages** from a GPS receiver.
2. **Parse and extract** ephemeris & pseudorange data.
3. **Estimate user position** using least squares.
4. **Display computed latitude, longitude, and height**.

---

## 🛠️ Main Components

### **1️⃣ RTCM Parsing & Data Processing**
- `parse_rtcm_messages.py`: Reads and parses RTCM messages.
- `process_parsed_message.py`: Extracts relevant satellite and receiver data.
- `format_ephemeris.py`: Converts raw ephemeris data into a structured format.
- `format_pseudorange.py`: Processes MSM pseudorange data.

### **2️⃣ Position Estimation**
- `estimate_satellite_clock_bias.py`: Computes satellite clock bias correction.
- `get_satellite_position.py`: Converts ephemeris data into ECEF satellite positions.
- `estimate_position.py`: Implements least-squares estimation to compute user position and clock bias.

### **3️⃣ Coordinate Conversion & Accuracy Computation**
- `WGStoEllipsoid.py`: Converts ECEF coordinates to **Latitude, Longitude, and Height**.
- `rot.py`: Computes rotation matrices for **ENU transformation**.
- `compute_HDOP_VDOP.py`: Computes **HDOP & VDOP** values to measure position accuracy.

---

## 📊 Output Example
```
EPH: {28: {...}, 24: {...}, 25: {...}}
PR: {6: 21285360.3, 11: 20685764.2, 12: 20086191.0, ...}
Receiver TOW: 598027.0
Satellite 6 ECEF Position: [[ 20398851.41 -16747187.81  -2013475.28]]
Satellite 6 theta: 5.16e-06
Estimated Position: [  4153.2  -5284.1  6320.9]
Estimated Clock Bias: -243217.4
HDOP: 1.4321
VDOP: 2.7893
```

---

## 📌 Notes
- The program is designed for **real-time processing**, but can be adapted for post-processing.
- Requires an **RTCM-capable GPS receiver** for live data.
- Uses **WGS-84 reference frame** for positioning.

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 🤝 Contributing
1. **Fork the repository**
2. **Create a new branch** (`feature-name`)
3. **Commit your changes**
4. **Push and create a PR!**

---

## 📞 Contact
For questions or issues, reach out via **GitHub Issues** or email at `your-email@example.com` 🚀

