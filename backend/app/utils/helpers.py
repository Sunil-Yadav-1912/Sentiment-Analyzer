import psutil
import platform
from typing import Dict


def get_system_info() -> Dict[str, any]:
    """Get system information including CPU, memory, and platform details"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_percent": cpu_percent,
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_percent": memory.percent
        }
    except Exception as e:
        return {"error": str(e)}


def format_confidence(confidence: float, decimals: int = 3) -> float:
    """Format confidence score to specified decimal places"""
    return round(confidence, decimals)


def preprocess_text(text: str) -> str:
    """Preprocess text before analysis"""
    # Strip whitespace
    text = text.strip()
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text
