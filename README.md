# Universal Sentiment Analyzer

[![CI/CD Jenkins](https://img.shields.io/badge/ci%2Fcd-jenkins-blue.svg)](Jenkinsfile)
[![Docker Build](https://img.shields.io/badge/docker-multi--stage-blue.svg)](Dockerfile)

A streamlined, production-ready machine learning base project for real-time sentiment analysis (Positive, Negative, or Intermediate). Built with Scikit-learn, FastAPI, Streamlit, Docker, and Jenkins CI/CD.

## 🚀 Features

### Core Analysis
- **Universal Text Sentiment Analysis**: Predicts sentiment for product reviews, customer feedback, tweets, and general text.
- **3-Tier Classification**: Predicts **Positive**, **Negative**, or **Intermediate** (neutral/mixed) with confidence scores.
- **Input Validation**: Filters invalid or whitespace-only inputs.
- **Fast Prediction Caching**: MD5 hashing and TTL cache for fast lookups.

### User Interfaces & APIs
- **Streamlit Web UI**: Elegant single-page user interface with instant sentiment feedback and sample test cases.
- **FastAPI Backend**: REST API server for programmatic sentiment analysis.

### DevOps & Infrastructure
- **Jenkins CI/CD Pipeline**: Automated environment setup, static analysis, security scanning, unit testing (`pytest`), and Docker build.
- **Multi-Stage Dockerfile**: Compact, production-grade container build with non-root security standards.
- **Jenkins Trigger Automation**: Utility script `trigger_jenkins.py` for automated pipeline execution.

---

## 🏗️ Architecture

```
┌─────────────────┐        ┌──────────────────┐
│   Streamlit UI  │        │   FastAPI REST   │
│    (app.py)     │        │    (api.py)      │
└────────┬────────┘        └────────┬─────────┘
         │                          │
         └────────────┬─────────────┘
                      │
           ┌──────────▼──────────┐
           │   Inference Service │
           │ (Validation & Cache)│
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │   ML Pipeline       │
           │ (TF-IDF + LogReg)   │
           └─────────────────────┘
```

---

## 💻 Quick Start

### 1. Run Streamlit UI
```bash
streamlit run app.py
```

### 2. Run FastAPI Server
```bash
python api.py
```

### 3. Run Unit Tests
```bash
pytest test_sentiment_analyzer.py -v
```

---

## 🐳 Docker Deployment

Build and run using Docker:

```bash
docker build -t sailesh2508/sentiment-analyzer:latest .
docker run -p 8501:8501 -p 8000:8000 sailesh2508/sentiment-analyzer:latest
```

---

## ⚙️ DevOps Pipeline (Jenkins)

The included `Jenkinsfile` runs:
1. Virtual environment and dependency installation
2. Static code linting (`black`, `flake8`)
3. Security vulnerability scanning (`bandit`, `safety`)
4. Unit testing (`pytest` with JUnit XML results)
5. Production Docker image compilation
