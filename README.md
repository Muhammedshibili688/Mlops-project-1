
---

# 🚗 Vehicle Insurance Response Prediction — End-to-End MLOps System

> **A full-stack, production-oriented MLOps project** demonstrating how real-world machine learning systems are designed, built, deployed, and continuously delivered using modern MLOps practices and cloud infrastructure.

This project goes **far beyond model training**. It showcases **data engineering, ML pipelines, model governance, CI/CD, cloud deployment, and system design decisions** that recruiters expect from a serious Data Scientist / MLOps Engineer.

---

## 🔍 Problem Statement

Predict whether a customer is likely to respond positively to a vehicle insurance offer, using structured customer and vehicle data.

The focus of this project is **not just accuracy**, but **building a scalable, maintainable, and production-ready ML system**.

---

## 🧠 What Makes This Project Different?

✅ End-to-end MLOps lifecycle
✅ Modular, production-grade codebase
✅ Cloud-native architecture (AWS + Docker + GitHub Actions)
✅ Automated CI/CD pipeline
✅ Model versioning and registry
✅ Real-time inference via FastAPI
✅ Designed with **interview-level engineering rigor**

---

## 🏗️ High-Level Architecture

```
GitHub Push
   ↓
CI Pipeline (GitHub Actions)
   - Build Docker Image
   - Push to Amazon ECR
   ↓
CD Pipeline (Self-Hosted Runner on EC2)
   - Pull Image from ECR
   - Run Container
   ↓
FastAPI Application (EC2)
   - Inference API
   - Training Trigger
   ↓
MongoDB Atlas (Data Source)
AWS S3 (Model Registry)
```

---

## 🧩 Project Structure (Modular & Scalable)

```
├── src/
│   ├── components/           # Data ingestion, validation, transformation, training
│   ├── configuration/        # MongoDB & AWS connections
│   ├── data_access/          # Database access layer
│   ├── entity/               # Config & artifact entities
│   ├── pipeline/             # Training & prediction pipelines
│   ├── aws_storage/          # S3 model registry logic
│   ├── utils/                # Common utilities
│   ├── logger/               # Centralized logging
│   ├── exception/            # Custom exception handling
│
├── notebook/                 # EDA & feature engineering
├── static/                   # Frontend static assets
├── templates/                # HTML templates
├── app.py                    # FastAPI application
├── Dockerfile                # Containerization
├── requirements.txt
├── setup.py / pyproject.toml # Local package management
└── .github/workflows/aws.yaml # CI/CD pipeline
```

---

## ⚙️ Tech Stack & Tools

### 🧪 Machine Learning

* Scikit-learn
* Pandas, NumPy
* Feature Engineering & Validation
* Modular Estimator Design

### 🗄️ Data Layer

* **MongoDB Atlas** (Cloud NoSQL DB)
* Secure connection via environment variables

### ☁️ Cloud & DevOps

* **AWS EC2** – model serving
* **AWS S3** – model registry
* **AWS ECR** – Docker image registry
* **IAM Roles & Policies**

### 🐳 Containerization

* Docker
* Multi-stage, production-ready images

### 🔁 CI/CD

* GitHub Actions
* Self-Hosted Runner on EC2
* Automated build → push → deploy

### 🌐 API & Serving

* FastAPI
* Uvicorn
* HTML UI + REST endpoints

---

## 🔄 End-to-End ML Pipeline

### 1️⃣ Data Ingestion

* Pulls raw data from MongoDB Atlas
* Converts key-value records into DataFrames
* Stores artifacts for reproducibility

### 2️⃣ Data Validation

* Schema validation via `schema.yaml`
* Data drift & structure checks
* Prevents bad data from entering training

### 3️⃣ Data Transformation

* Feature engineering
* Encoding & scaling
* Pipeline-based preprocessing

### 4️⃣ Model Training

* Modular estimator design
* Metrics-driven evaluation
* Trained artifacts saved locally & to S3

### 5️⃣ Model Evaluation

* Compares new model vs previous model
* Threshold-based promotion logic
* Prevents regression in production

### 6️⃣ Model Registry (AWS S3)

* Versioned models
* Centralized storage
* Pull/push via S3 APIs

---

## 🚀 FastAPI Application

### Available Routes

| Route      | Description                    |
| ---------- | ------------------------------ |
| `/`        | Web UI for prediction          |
| `/train`   | Trigger full training pipeline |
| `/predict` | Prediction endpoint            |

The app is containerized and exposed via EC2 public IP.

---

## 🔁 CI/CD Workflow (Production-Style)

### CI (GitHub-Hosted Runner)

* Build Docker image
* Tag & push to **Amazon ECR**

### CD (Self-Hosted Runner on EC2)

* Pull latest image from ECR
* Stop old container
* Run new container
* Zero manual intervention

> **Key Design Choice:**
> EC2 never builds images — it only pulls and runs.
> This follows real-world production standards.

---

## 🔐 Security & Configuration

* Secrets managed via **GitHub Secrets**
* Environment variables for MongoDB & AWS
* IAM-based access to AWS services
* `.gitignore` for artifacts & credentials

---

## 🧪 Local Development

```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🌍 Deployment

```text
http://<EC2_PUBLIC_IP>:8000
```

Port enabled via EC2 Security Groups.

---

## 📈 What Recruiters Should Notice

✔ Clean separation of concerns
✔ Real CI/CD, not scripts
✔ Cloud-native ML system
✔ Production-oriented thinking
✔ Debugging & failure-handling awareness
✔ Scalable project structure

---

## 🧠 Key Learnings Demonstrated

* How ML moves from notebook → production
* Why CI builds & servers only run
* How to version models safely
* How to deploy ML systems responsibly
* How to design for maintainability

---

## 📌 Final Note

This project reflects **real industry practices**, not academic demos.
Every design choice was made with **scalability, reliability, and clarity** in mind.

---
