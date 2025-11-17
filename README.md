<h1 align="center">🌊 Ocean Hazard – AI-Powered Coastal Threat Detection System</h1>

<p align="center">
  <b>A real-time intelligent system for detecting, classifying, and mapping coastal hazards across India.</b><br>
  Built using Machine Learning, Flask, GeoLocation, and MongoDB.
</p>

---

## 📌 Table of Contents  
- [Overview](#overview)  
- [Why I Built This Project](#why-i-built-this-project)  
- [How This Project Is Different](#how-this-project-is-different)  
- [Key Features](#key-features)  
- [Technology Stack](#technology-stack)  
- [System Architecture](#system-architecture)  
- [Project Structure](#project-structure)  
- [Setup Instructions](#setup-instructions)  
- [Deployment (Render)](#deployment-render)  
- [Future Enhancements](#future-enhancements)  
- [Author](#author)

---

# 🚀 Overview

**Ocean Hazard** is a full-stack AI-powered platform built to detect, classify, and visualize coastal hazards across India.  
It allows users to upload real images and descriptions of hazardous events along the seashore—pollution, floods, dead animals, high tides, storms—and intelligently identifies whether it is a real hazard using an ML model.

It provides an interactive heatmap that shows **real-time hazard hotspots**, helping in:

- 🛟 **Beach safety**
- 🌍 **Environmental monitoring**
- 🌧️ **Climate risk assessment**
- 📡 **Disaster management**

---

# 🎯 Why I Built This Project

I built Ocean Hazard to solve **real-world coastal safety challenges**.

> ❗ There is no centralized system to track and map coastal hazards in real-time in India.

I wanted to create a system that:
- Saves lives by identifying risks early  
- Assists lifeguards and authorities  
- Helps track climate-change-induced coastal events  
- Prevents pollution from spreading  
- Gives users a platform to report environmental issues  

This project blends **AI + Environment + Social Impact** — all in one.

---

# 💡 How This Project Is Different  

Most web apps are just CRUD systems.  
Ocean Hazard is **intelligent**, **geospatial**, and **AI-driven**.

### 🧠 1. AI-Based Hazard Classification  
Understands the text using NLP & ML, classifies if it's hazardous.  
Rejects non-hazard submissions.

### 🌍 2. Automatic Geolocation  
Converts location text → Lat/Lon and validates if the place is inside India.

### 🗺️ 3. Real-Time Interactive Heatmap  
Displays hazard hotspots on the Indian coastline with intensity levels.

### 🧹 4. Smart Text Cleaning + Summary  
Cleans user description and auto-generates a short summary.

### 📸 5. Image + Metadata Storage  
Stores every hazard with image + location + summary + prediction.

### ⚙️ 6. Full End-to-End Stack  
ML → NLP → Flask → MongoDB → Maps → Deployment  
A full real-world system.

---

# 🔥 Key Features

### ✔ Upload Hazard Reports  
Images + Description + Date + Time + Location

### ✔ Hazard Classification Pipeline  
Custom ML pipeline to identify hazards

### ✔ Geolocation Validation  
Only incidents inside India are allowed

### ✔ Interactive Heatmap  
Watch hotspot intensities grow dynamically

### ✔ View All Hazard Reports  
Beautiful gallery with images and metadata

### ✔ Deployed on Render  
Secure, scalable backend hitting MongoDB Atlas

---

# 🛠️ Technology Stack

### **Frontend**
- HTML, CSS, Bootstrap
- Jinja Templates  
- Leaflet.js (Heatmap + Map)

### **Backend**
- Flask  
- Python  
- Gunicorn  
- Custom NLP Pipeline  
- Custom ML Model (TF-IDF + Logistic Regression)

### **Database**
- MongoDB Atlas

### **Deployment**
- Render Web Service  
- Environment Variables via Render Secrets  
- Gunicorn Production Server  

---

# 🧠 System Architecture

```
User Uploads Post
        ↓
Image saved → /static/uploads/
        ↓
Text processed using NLP + ML model
        ↓
Hazard classification
        ↓
Location → Lat/Lon (geolocation)
        ↓
MongoDB stores hazard details
        ↓
Heatmap updates with new hotspot
        ↓
Users view hazard gallery & map
```

---

# 🌳 Project Structure

```
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── main.py
│   ├── procfile
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── databases
│       │   ├── __init__.py
│       │   └── mongo_db.py
│       ├── exception
│       │   ├── __init__.py
│       │   └── exception.py
│       ├── logging
│       │   ├── __init__.py
│       │   └── logging.py
│       ├── ml_models
│       │   ├── __init__.py
│       │   └── classifier.py
│       ├── model
│       │   └── ocean_hazard_model1.pkl
│       ├── pipeline
│       │   ├── __init__.py
│       │   └── hazard_pipeline.py
│       ├── routes
│       │   ├── __init__.py
│       │   ├── home_routes.py
│       │   ├── map_routes.py
│       │   └── post_routes.py
│       └── utils
│           ├── __init__.py
│           ├── geolocation.py
│           ├── summarizer.py
│           ├── text_processor.py
│           ├── translator.py
│           └── validator.py
└── frontend
    ├── static
    │   └── uploads
    │       
    │       
    └── templates
        ├── index.html
        ├── map.html
        └── posts.html

```

---

# ⚙️ Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone https://github.com/reddyrohith49471/ocean-hazard
cd ocean-hazard/backend
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add `.env` file
```
MONGO_URI=your_mongodb_connection_string
```

### 4️⃣ Run App
```bash
python app.py
```

### 5️⃣ Open in browser
```
http://localhost:5001
```

---

# 🌐 Deployment (Render)

### 🔹 Add secret:
Environment → Add Environment Variable  
```
MONGO_URI = your-uri-here
```

### 🔹 Start command:
```
gunicorn app:app -b 0.0.0.0:$PORT
```

### 🔹 Build command:
```
pip install -r requirements.txt
```

---

# 🔮 Future Enhancements

- 🌪️ Deep Learning for hazard severity estimation  
- 🤖 LLM-based description summarization  
- 📱 Mobile App version  
- 🛰️ Integration with real-time ocean sensors  
- ⚠️ Auto-alert system for authorities  
- 📊 Admin dashboard with statistics  

---

# 👤 Author

**Reddy Rohith Kosinepalli**  
AI/ML Engineer | Python Developer | Backend Developer  
- GitHub: https://github.com/reddyrohith49471  
- LinkedIn: https://www.linkedin.com/in/reddy-rohith-kosinepalli  

---

If you like this project, please ⭐ star the repository — it motivates me to build more impactful AI solutions!
