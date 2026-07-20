# ==========================================
# Stage 1: Build dependencies
# ==========================================
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build-essential for any compilation requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Final minimal runner image
# ==========================================
FROM python:3.9-slim AS runner

WORKDIR /app

# Install runtime dependencies (curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV FASTAPI_PORT=8000
ENV LOG_LEVEL=INFO

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Universal Sentiment Analyzer in Production Mode"\n\
\n\
# Check if model exists, if not run setup\n\
if [ ! -f "sentiment_pipeline.pkl" ]; then\n\
    echo "📊 Model not found, running initial training..."\n\
    python eda.py\n\
    python model_trainer.py\n\
fi\n\
\n\
echo "🔄 Starting services..."\n\
# Start FastAPI backend\n\
python api.py &\n\
API_PID=$!\n\
\n\
# Start Streamlit UI\n\
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &\n\
STREAMLIT_PID=$!\n\
\n\
echo "✅ Services started:"\n\
echo "   - FastAPI API: http://localhost:8000"\n\
echo "   - Streamlit UI: http://localhost:8501"\n\
echo "   - API Docs: http://localhost:8000/docs"\n\
\n\
# Wait for any process to exit\n\
wait -n\n\
\n\
# Exit with status of process that exited first\n\
exit $?\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set up non-root system user and change directory ownership
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -d /app -s /bin/bash appuser && \
    mkdir -p logs && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8501 8000

# Health check using non-root user capabilities
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command runs both services
CMD ["/app/start.sh"]
