from pydantic import BaseModel, Field, validator
from typing import List, Optional


class TextInput(BaseModel):
    """Single text input for sentiment analysis"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze")
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()


class BatchTextInput(BaseModel):
    """Multiple texts input for batch sentiment analysis"""
    texts: List[str] = Field(..., min_items=1, max_items=50, description="List of texts to analyze")
    
    @validator('texts')
    def texts_not_empty(cls, v):
        if not v:
            raise ValueError('Texts list cannot be empty')
        # Strip whitespace and validate each text
        cleaned = [text.strip() for text in v if text.strip()]
        if not cleaned:
            raise ValueError('All texts are empty')
        return cleaned


class SentimentResult(BaseModel):
    """Single sentiment analysis result"""
    text: str = Field(..., description="Analyzed text")
    sentiment: str = Field(..., description="Predicted sentiment (POSITIVE or NEGATIVE)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class BatchSentimentResult(BaseModel):
    """Batch sentiment analysis results"""
    results: List[SentimentResult] = Field(..., description="List of sentiment analysis results")
    total: int = Field(..., description="Total number of texts analyzed")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    device: str = Field(..., description="Device being used (CPU/CUDA)")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    system_info: Optional[dict] = Field(None, description="System information")


class ModelInfo(BaseModel):
    """Model information response"""
    status: str = Field(..., description="Model status")
    model_name: Optional[str] = Field(None, description="Model name")
    tokenizer_name: Optional[str] = Field(None, description="Tokenizer name")
    device: Optional[str] = Field(None, description="Device")
    max_sequence_length: Optional[int] = Field(None, description="Maximum sequence length")
    parameters: Optional[int] = Field(None, description="Number of model parameters")


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error")
