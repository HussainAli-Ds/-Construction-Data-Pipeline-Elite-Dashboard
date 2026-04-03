# 🚀 Construction Data Pipeline & Elite Dashboard

## 📊 Overview

This project is a complete **end-to-end data engineering pipeline** with a powerful **interactive dashboard**.

It automatically:

* 📥 Detects new Excel/CSV files
* 🧹 Cleans & removes duplicates
* 📦 Loads data into PostgreSQL
* 📊 Visualizes insights in a modern dashboard

---

## 🏗 Architecture

```
Excel/CSV Files
      ↓
 File Watcher (Python)
      ↓
 Data Cleaning & Deduplication
      ↓
 PostgreSQL Database
      ↓
 Streamlit Dashboard
```

---

## ⚙️ Tech Stack

* **Python** (ETL pipeline)
* **PostgreSQL** (Database)
* **Streamlit** (Dashboard)
* **Pandas** (Data processing)
* **Docker** (Deployment)

---

## 📂 Project Structure

```
Construction_pipeline/
│
├── code/                  # ETL pipeline
├── dashboard/             # Streamlit dashboard
├── input_files/           # Incoming files
├── processed_files/       # Processed files
├── failed_files/          # Failed files
├── logs/                  # Logs
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env (not included)
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
DB_HOST=db
DB_PORT=5432
DB_NAME=construction_project
DB_USER=your_user
DB_PASS=your_password
```

---

## 🐳 Run with Docker (Recommended)

### 1. Build & Start

```
docker-compose up --build
```

### 2. Open Dashboard

👉 http://localhost:8501

---

## 💻 Run Without Docker

### Install dependencies

```
pip install -r requirements.txt
```

### Start Pipeline

```
python code/main.py
```

### Start Dashboard

```
streamlit run dashboard/dashboard.py
```

---

## 📊 Features

### 🔄 Data Pipeline

* Automatic file detection
* Handles large files efficiently
* Duplicate removal
* Error handling & logging

### 📈 Dashboard

* Overview metrics (labour, machines, cost)
* Drill-down filters (site & date)
* Top performers & rankings
* Charts (bar, line, distribution)
* Advanced insights & analytics

---

## 🧠 Insights Included

* Top materials by usage
* Best & worst labour performance
* Machine utilization analysis
* Maintenance cost breakdown
* Project progress tracking

---

## 👨‍💻 Author

**Hussain Ali**

📧 Email: [ha780383@gmail.com](mailto:ha780383@gmail.com)
📞 Phone: 03357897412

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share!
