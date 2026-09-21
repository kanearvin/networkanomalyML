# networkanomalyML
# Network Anomaly Detection (using the dataset of UNSW-NB15)

## 📌 Project Overview
This repository contains an end-to-end Machine Learning pipeline designed to detect network intrusions (Exploits, DoS, Fuzzers) using behavioral analysis. It utilizes LightGBM to evaluate Zeek/Bro flow metrics and is served via a FastAPI REST endpoint.

## 🚀 Deployment Guide  

### Local Deployment
1. Clone the repository: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API: `uvicorn src.app:app --reload`
4. Access the interactive UI at: `http://127.0.0.1:8000/docs`

### Docker Deployment (Reproducible Environment)
To run this application in an isolated Docker container:
```bash
docker build -t intrusiondetect-api .
docker run -p 8000:8000 intrusiondetect-api
