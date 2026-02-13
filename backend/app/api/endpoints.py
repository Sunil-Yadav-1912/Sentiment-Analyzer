from fastapi import APIRouter, HTTPException
from app.schemas import (
    TextInput,
    BatchTextInput,
    SentimentResult,
    BatchSentimentResult,
    HealthResponse,
    ModelInfo
)
from app.core.model_manager import model_manager
from app.utils.helpers import get_system_info, format_confidence, preprocess_text
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint with API information and examples"""
    return {
        "message": "DistilBERT Sentiment Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/": "GET - API information",
            "/health": "GET - Health check with system status",
            "/analyze": "POST - Analyze sentiment of single text",
            "/analyze/batch": "POST - Analyze sentiment of multiple texts",
            "/models/info": "GET - Get model information"
        },
        "examples": {
            "single_analysis": {
                "endpoint": "/analyze",
                "method": "POST",
                "input": {"text": "I love this movie! It's absolutely fantastic."},
                "output": {
                    "text": "I love this movie! It's absolutely fantastic.",
                    "sentiment": "POSITIVE",
                    "confidence": 0.999
                }
            },
            "batch_analysis": {
                "endpoint": "/analyze/batch",
                "method": "POST",
                "input": {
                    "texts": [
                        "I love this!",
                        "This is terrible.",
                        "It's okay, I guess."
                    ]
                }
            }
        },
        "documentation": "/docs"
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint with system information
    
    Returns service status, device information, and system metrics
    """
    if not model_manager.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service is starting up."
        )
    
    model_info = model_manager.get_model_info()
    system_info = get_system_info()
    
    return HealthResponse(
        status="healthy",
        device=model_info.get("device", "unknown"),
        model_loaded=True,
        system_info=system_info
    )


@router.post("/analyze", response_model=SentimentResult)
async def analyze_sentiment(input_data: TextInput):
    """
    Analyze sentiment of a single text
    
    - **text**: The text to analyze (1-5000 characters)
    
    Returns sentiment label (POSITIVE/NEGATIVE) and confidence score
    """
    if not model_manager.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please try again in a moment."
        )
    
    try:
        # Preprocess text
        processed_text = preprocess_text(input_data.text)
        
        # Get prediction
        sentiment, confidence = model_manager.predict_sentiment(processed_text)
        
        return SentimentResult(
            text=input_data.text,
            sentiment=sentiment,
            confidence=format_confidence(confidence)
        )
    
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        )


@router.post("/analyze/batch", response_model=BatchSentimentResult)
async def analyze_batch_sentiment(input_data: BatchTextInput):
    """
    Analyze sentiment of multiple texts in batch
    
    - **texts**: List of texts to analyze (1-50 texts, each 1-5000 characters)
    
    Returns list of sentiment results with labels and confidence scores
    """
    if not model_manager.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please try again in a moment."
        )
    
    try:
        results = []
        
        for text in input_data.texts:
            # Preprocess text
            processed_text = preprocess_text(text)
            
            # Get prediction
            sentiment, confidence = model_manager.predict_sentiment(processed_text)
            
            results.append(
                SentimentResult(
                    text=text,
                    sentiment=sentiment,
                    confidence=format_confidence(confidence)
                )
            )
        
        return BatchSentimentResult(
            results=results,
            total=len(results)
        )
    
    except Exception as e:
        logger.error(f"Error during batch sentiment analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing batch sentiment: {str(e)}"
        )


@router.get("/models/info", response_model=ModelInfo)
async def get_model_info():
    """
    Get information about the loaded model
    
    Returns model name, device, parameters count, and other details
    """
    info = model_manager.get_model_info()
    return ModelInfo(**info)
