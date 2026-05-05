import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "app.log"):
    """Centralized logging configuration with rotation."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # File Handler (with rotation to save space)
        file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

class DecisionIntelligenceError(Exception):
    """Base class for all system errors."""
    pass

class DataProcessingError(DecisionIntelligenceError):
    """Raised when data loading or cleaning fails."""
    pass

class AIAnalysisError(DecisionIntelligenceError):
    """Raised when LLM interactions fail."""
    pass

class SimulationError(DecisionIntelligenceError):
    """Raised when mathematical models fail."""
    pass
