"""
FastAPI backend for the Universal Sentiment Analyzer.
Provides REST API endpoints for sentiment analysis.
"""

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
except ImportError:
    FastAPI = None

from typing import List, Optional, Dict, Any
import pandas as pd
import io
from inference_service import get_analyzer
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if FastAPI is not None:
    # Initialize FastAPI app
    app = FastAPI(
        title="Universal Sentiment Analyzer API",
        description="REST API for sentiment analysis with caching and monitoring",
        version="2.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app = None


# Pydantic models
class TextInput(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=10000, description="Text to analyze"
    )
    use_cache: bool = Field(True, description="Whether to use prediction cache")


class BatchTextInput(BaseModel):
    texts: List[str] = Field(
        ..., min_items=1, max_items=1000, description="List of texts to analyze"
    )
    use_cache: bool = Field(True, description="Whether to use prediction cache")


class SentimentResponse(BaseModel):
    label: str = Field(..., description="Predicted sentiment label")
    confidence_score: float = Field(..., description="Confidence score")
    probabilities: Dict[str, float] = Field(..., description="Class probabilities")
    processed_text_length: int = Field(..., description="Length of processed text")


class BatchSentimentResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="List of prediction results")
    total_processed: int = Field(..., description="Total number of texts processed")
    processing_time_seconds: float = Field(..., description="Total processing time")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    cache_size: int
    timestamp: str


# Initialize analyzer
analyzer = get_analyzer()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Universal Sentiment Analyzer API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if analyzer.pipeline is not None else "unhealthy",
        model_loaded=analyzer.pipeline is not None,
        cache_size=len(analyzer.prediction_cache),
        timestamp=datetime.now().isoformat(),
    )


@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(input_data: TextInput):
    """
    Predict sentiment for a single text input.

    Args:
        input_data: Text input with optional cache setting

    Returns:
        Sentiment prediction with confidence scores
    """
    try:
        result = analyzer.predict_sentiment(input_data.text, input_data.use_cache)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return SentimentResponse(**result)

    except Exception as e:
        logger.error(f"Error in predict_sentiment: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchSentimentResponse)
async def predict_batch(input_data: BatchTextInput):
    """
    Predict sentiment for multiple texts.

    Args:
        input_data: List of texts with optional cache setting

    Returns:
        Batch prediction results with timing information
    """
    try:
        start_time = datetime.now()

        results = analyzer.predict_batch(input_data.texts)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        return BatchSentimentResponse(
            results=results,
            total_processed=len(results),
            processing_time_seconds=processing_time,
        )

    except Exception as e:
        logger.error(f"Error in predict_batch: {e}")
        raise HTTPException(
            status_code=500, detail=f"Batch prediction failed: {str(e)}"
        )


@app.post("/predict/file")
async def predict_file(file: UploadFile = File(...)):
    """
    Predict sentiment for texts in an uploaded CSV file.

    Args:
        file: CSV file with a 'text' column

    Returns:
        Prediction results for all texts in the file
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        # Read CSV file
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))

        if "text" not in df.columns:
            raise HTTPException(
                status_code=400, detail="CSV file must contain a 'text' column"
            )

        # Predict for all texts
        texts = df["text"].dropna().tolist()
        if not texts:
            raise HTTPException(status_code=400, detail="No valid texts found in file")

        start_time = datetime.now()
        results = analyzer.predict_batch(texts)
        end_time = datetime.now()

        # Add results to dataframe
        results_df = pd.DataFrame(results)

        # Return as JSON
        return {
            "filename": file.filename,
            "total_texts": len(texts),
            "processing_time_seconds": (end_time - start_time).total_seconds(),
            "results": results_df.to_dict("records"),
        }

    except Exception as e:
        logger.error(f"Error in predict_file: {e}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")


@app.get("/model/info")
async def get_model_info():
    """Get information about the loaded model."""
    try:
        info = analyzer.get_model_info()
        return info
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get model info: {str(e)}"
        )


@app.post("/cache/clear")
async def clear_cache():
    """Clear the prediction cache."""
    try:
        cache_size_before = len(analyzer.prediction_cache)
        analyzer.clear_cache()

        return {
            "message": "Cache cleared successfully",
            "cache_size_before": cache_size_before,
            "cache_size_after": len(analyzer.prediction_cache),
        }
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
