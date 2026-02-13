import torch
import logging
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from typing import Optional, Tuple
from .config import settings


logger = logging.getLogger(__name__)


class ModelManager:
    """Singleton class to manage ML model loading and inference"""
    
    _instance: Optional['ModelManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.tokenizer: Optional[DistilBertTokenizer] = None
            self.model: Optional[DistilBertForSequenceClassification] = None
            self.device: Optional[torch.device] = None
            self._initialized = True
    
    def load_model(self) -> None:
        """Load the sentiment analysis model and tokenizer"""
        if self.model is not None and self.tokenizer is not None:
            logger.info("Model already loaded")
            return
        
        try:
            # Determine device
            if settings.DEVICE == "auto":
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            else:
                self.device = torch.device(settings.DEVICE)
            
            logger.info(f"Using device: {self.device}")
            
            # Load tokenizer
            logger.info(f"Loading tokenizer: {settings.TOKENIZER_NAME}")
            self.tokenizer = DistilBertTokenizer.from_pretrained(settings.TOKENIZER_NAME)
            
            # Load model
            logger.info(f"Loading model: {settings.MODEL_NAME}")
            self.model = DistilBertForSequenceClassification.from_pretrained(
                settings.MODEL_NAME
            )
            
            # Move model to device and set to evaluation mode
            self.model = self.model.to(self.device)
            self.model.eval()
            
            logger.info("Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def predict_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Predict sentiment for a given text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=settings.MAX_SEQUENCE_LENGTH
        )
        
        # Move inputs to device
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get results
        labels = ['NEGATIVE', 'POSITIVE']
        predicted_class = torch.argmax(predictions, dim=-1).item()
        predicted_label = labels[predicted_class]
        confidence = torch.max(predictions).item()
        
        return predicted_label, confidence
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        if self.model is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": settings.MODEL_NAME,
            "tokenizer_name": settings.TOKENIZER_NAME,
            "device": str(self.device),
            "max_sequence_length": settings.MAX_SEQUENCE_LENGTH,
            "parameters": sum(p.numel() for p in self.model.parameters()),
        }
    
    def is_ready(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None


# Global model manager instance
model_manager = ModelManager()
