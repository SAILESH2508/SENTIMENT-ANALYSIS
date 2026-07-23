# 🧠 Universal Sentiment Analyzer

[![CI/CD Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?logo=jenkins&logoColor=white)](Jenkinsfile)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](app.py)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](api.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

A production-ready, end-to-end machine learning application for real-time sentiment analysis. Classifies any English text as **Positive**, **Negative**, or **Intermediate (Neutral/Mixed)** with confidence scores. Built with Scikit-learn, FastAPI, Streamlit, Docker, and a full Jenkins CI/CD pipeline.

---

## 📸 Demo

> **Streamlit UI** — Glassmorphism-styled single-page app with instant feedback, quick examples, and a session history sidebar.

> **FastAPI** — Interactive Swagger docs at `/docs` for direct API exploration.

---

## ✨ Features

### 🎯 Core ML
| Feature | Detail |
|---|---|
| Model | Logistic Regression + TF-IDF (1–2 gram) |
| Dataset | 50,000 IMDB Movie Reviews (balanced) |
| Classification | Positive / Negative / Intermediate |
| Confidence Score | Per-prediction probability output |
| Preprocessing | HTML stripping, lowercasing, punctuation removal |
| Caching | MD5-keyed TTL prediction cache (configurable TTL) |
| Batch Inference | Configurable batch size with progress logging |

### 🖥️ Interfaces
- **Streamlit Web UI** — Glassmorphism design, animated result cards, quick-example buttons, and session history sidebar.
- **FastAPI REST API** — Single prediction, batch prediction, CSV file upload, model info, health check, and cache management endpoints.
- **Swagger / OpenAPI Docs** — Auto-generated interactive API documentation at `http://localhost:8000/docs`.

### 🔧 Engineering & DevOps
- **Jenkins CI/CD Pipeline** — 5-stage automated pipeline: dependency install → linting → SAST security scan → unit tests → Docker build.
- **Multi-Stage Dockerfile** — Minimal production image with a non-root user, virtual environment isolation, and a built-in health check.
- **Automated Setup Script** — `setup.py` handles dependencies, data download, model training, and validation in one command.
- **Structured Logging** — All predictions and errors are logged to `sentiment_analyzer.log` with timestamps.
- **YAML Configuration** — Centralized `config.yaml` for model thresholds, cache TTL, security limits, and UI settings.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Interfaces                       │
│                                                      │
│   ┌──────────────────┐    ┌───────────────────────┐ │
│   │   Streamlit UI   │    │   FastAPI REST API    │ │
│   │    (app.py)      │    │      (api.py)         │ │
│   │  Port: 8501      │    │     Port: 8000        │ │
│   └────────┬─────────┘    └──────────┬────────────┘ │
└────────────┼──────────────────────────┼──────────────┘
             │                          │
             └────────────┬─────────────┘
                          │
           ┌──────────────▼──────────────┐
           │      Inference Service       │
           │    (inference_service.py)    │
           │  - Input Validation          │
           │  - TTL Prediction Cache      │
           │  - Batch Processing          │
           │  - Prediction Logging        │
           └──────────────┬──────────────┘
                          │
           ┌──────────────▼──────────────┐
           │       ML Pipeline            │
           │    (sentiment_pipeline.pkl)  │
           │  TF-IDF Vectorizer (1-2gram) │
           │  + Logistic Regression       │
           └──────────────┬──────────────┘
                          │
           ┌──────────────▼──────────────┐
           │     Shared Utilities         │
           │        (utils.py)            │
           │  - preprocess_text()         │
           │  - validate_text_input()     │
           │  - ModelConfig class         │
           └──────────────────────────────┘
```

---

## 📁 Project Structure

```
sentiment analysis/
├── app.py                    # Streamlit web UI (main entry point)
├── api.py                    # FastAPI REST API server
├── inference_service.py      # SentimentAnalyzer class with caching
├── model_trainer.py          # Model training script (TF-IDF + LogReg)
├── utils.py                  # Shared preprocessing and validation utilities
├── ui.py                     # Streamlit UI components (sidebar, result cards)
├── styles.py                 # Custom CSS/glassmorphism styles for Streamlit
├── download_data.py          # IMDB dataset downloader
├── setup.py                  # One-command automated setup script
├── test_sentiment_analyzer.py# Pytest test suite (unit + integration)
├── config.yaml               # Centralized configuration file
├── requirements.txt          # Python dependencies
├── Dockerfile                # Multi-stage production Docker build
├── Jenkinsfile               # 5-stage Jenkins CI/CD pipeline
├── trigger_jenkins.py        # Jenkins pipeline trigger utility
├── .streamlit/
│   └── config.toml           # Streamlit server configuration
├── data/
│   ├── IMDB Dataset.csv      # Raw IMDB dataset (50k reviews)
│   ├── train.csv             # Training split
│   └── test.csv              # Test split
├── sentiment_pipeline.pkl    # Trained model artifact
└── model_metrics.pkl         # Saved evaluation metrics
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Option 1 — Automated Setup (Recommended)

This handles everything: dependencies, data, model training, and tests.

```bash
python setup.py
```

### Option 2 — Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download dataset (if not already present)
python download_data.py

# 3. Train the model
python model_trainer.py

# 4. Launch the Streamlit UI
streamlit run app.py
```

### Option 3 — Run the API Server

```bash
python api.py
# API available at: http://localhost:8000
# Swagger docs at:  http://localhost:8000/docs
```

---

## 🐳 Docker Deployment

Build and run both services (Streamlit UI + FastAPI) in a single container:

```bash
# Build the image
docker build -t sailesh2508/sentiment-analyzer:latest .

# Run the container
docker run -p 8501:8501 -p 8000:8000 sailesh2508/sentiment-analyzer:latest
```

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| FastAPI | http://localhost:8000 |
| API Swagger Docs | http://localhost:8000/docs |

> If the model is not found inside the container, it automatically triggers training on startup.

---

## 🔌 API Reference

### `POST /predict` — Single Text Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "This movie was absolutely fantastic!", "use_cache": true}'
```

**Response:**
```json
{
  "label": "Positive",
  "confidence_score": 0.92,
  "probabilities": {
    "positive": 0.92,
    "negative": 0.08
  },
  "processed_text_length": 38
}
```

### `POST /predict/batch` — Batch Prediction

```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Great product!", "Awful experience.", "It was okay."]}'
```

### `POST /predict/file` — CSV File Upload

Upload a CSV with a `text` column to get bulk predictions.

```bash
curl -X POST "http://localhost:8000/predict/file" \
     -F "file=@your_data.csv"
```

### `GET /health` — Health Check

```bash
curl http://localhost:8000/health
```

### `GET /model/info` — Model Information

Returns model type, vectorizer, feature count, and accuracy metrics.

### `POST /cache/clear` — Clear Prediction Cache

---

## ⚙️ Configuration (`config.yaml`)

Key settings you can tune without touching the code:

```yaml
model:
  thresholds:
    intermediate_lower: 0.40   # Below this → Negative
    intermediate_upper: 0.60   # Above this → Positive
                               # Between → Intermediate
  training:
    ngram_range: [1, 2]        # Unigrams + bigrams
    max_iter: 1000
    c_value: 1.0

performance:
  cache_predictions: true
  cache_ttl_seconds: 3600      # Cache expires after 1 hour

security:
  rate_limit_per_minute: 60
  max_file_size_mb: 10
  allowed_file_types: [".csv", ".txt"]
```

---

## 🧪 Testing

```bash
# Run the full test suite
pytest test_sentiment_analyzer.py -v

# With JUnit XML output (as used in Jenkins)
pytest test_sentiment_analyzer.py -v --junitxml=test-results.xml
```

**Test coverage includes:**
- `TestUtils` — Text preprocessing, input validation, `ModelConfig` label logic
- `TestSentimentAnalyzer` — Prediction accuracy, caching, batch inference, model info, cache clearing
- `TestIntegration` — End-to-end prediction workflow with mocked pipeline

---

## 🔄 CI/CD Pipeline (Jenkins)

The `Jenkinsfile` defines a 5-stage automated pipeline:

```
Stage 1: Virtual Env & Dependencies
        ↓  pip install -r requirements.txt
Stage 2: Code Quality & Linting
        ↓  black (formatting) + flake8 (style)
Stage 3: Security SAST Scan
        ↓  bandit (code security) + safety (dependency CVEs)
Stage 4: Automated Unit Testing
        ↓  pytest with JUnit XML report
Stage 5: Docker Image Build
        ↓  docker build → sailesh2508/sentiment-analyzer:latest
```

To trigger the pipeline programmatically:

```bash
python trigger_jenkins.py
```

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Algorithm | Logistic Regression |
| Vectorizer | TF-IDF (1–2 gram) |
| Training Data | 50,000 IMDB reviews (25k positive, 25k negative) |
| Train/Test Split | 80% / 20% |
| Random State | 42 |
| Max Iterations | 1000 |
| Regularization (C) | 1.0 |
| Intermediate Zone | 0.40 – 0.60 probability |

The model achieves strong accuracy on the IMDB test set. Full metrics (accuracy, per-class precision/recall/F1, confusion matrix, feature count) are saved to `model_metrics.pkl` and exposed via the `/model/info` API endpoint.

---

## 🛡️ Security

- Container runs as a **non-root user** (`appuser`, UID 10001)
- Rate limiting configurable via `config.yaml`
- File upload restricted to `.csv` and `.txt` with size limits
- SAST scanning with `bandit` and `safety` in CI/CD
- CORS middleware included (configure `allow_origins` for production)

---

## 📦 Dependencies

```
pandas          — Data loading and manipulation
scikit-learn    — TF-IDF vectorizer and Logistic Regression
streamlit       — Web UI framework
fastapi         — REST API framework
uvicorn         — ASGI server for FastAPI
pydantic        — Request/response data validation
joblib          — Model serialization
requests        — HTTP client for dataset download
pytest          — Test framework
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👤 Author

**Sailesh** — [GitHub: sailesh2508](https://github.com/sailesh2508)

---

*Built as a portfolio project demonstrating end-to-end ML engineering: from data preprocessing and model training to REST APIs, containerization, and automated CI/CD.*
