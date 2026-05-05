import pandas as pd
import numpy as np
import logging
import re
from typing import Tuple, List, Dict, Optional

# Configure logging for production-level traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    A production-ready class to load, clean, and analyze CSV data for 
    Decision Intelligence systems.
    """
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.column_metadata: Dict[str, List[str]] = {
            "numeric": [],
            "categorical": [],
            "date": []
        }

    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts columns to lower_snake_case.
        Example: 'Total Sales ($)' -> 'total_sales'
        """
        def clean_name(name):
            # Convert to string, lowercase, and strip
            name = str(name).lower().strip()
            # Remove special characters
            name = re.sub(r'[^\w\s]', '', name)
            # Replace spaces/hyphens with underscores
            name = re.sub(r'[\s\-]+', '_', name)
            return name

        df.columns = [clean_name(col) for col in df.columns]
        logger.info(f"Standardized columns: {df.columns.tolist()}")
        return df

    def detect_and_convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Attempts to convert object columns to datetime objects.
        Uses heuristics like column names and data patterns.
        """
        for col in df.columns:
            # Heuristic 1: Column name contains date-related keywords
            date_keywords = ['date', 'time', 'at', 'timestamp', 'period', 'month', 'year']
            is_date_named = any(key in col.lower() for key in date_keywords)
            
            if is_date_named or df[col].dtype == 'object':
                # Try converting to datetime
                try:
                    # We check a sample to avoid expensive conversion on long text columns
                    sample = df[col].dropna().head(5)
                    if sample.empty:
                        continue
                        
                    converted = pd.to_datetime(df[col], errors='coerce')
                    
                    # If conversion successful for most non-null values, keep it
                    if converted.notnull().sum() > (df[col].notnull().sum() * 0.8):
                        df[col] = converted
                        logger.info(f"Converted '{col}' to datetime.")
                except (ValueError, TypeError):
                    continue
        return df

    def clean_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handles null values based on data types:
        - Numeric: Fills with median (preserves distribution better than mean)
        - Categorical: Fills with 'Unknown'
        - Dates: Left as NaT
        """
        # Numeric
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())
        
        # Categorical/Object
        cat_cols = df.select_dtypes(include=['object', 'string', 'category']).columns
        for col in cat_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna("Unknown")
        
        return df

    def update_metadata(self, df: pd.DataFrame):
        """Updates the internal registry of column types."""
        self.column_metadata["numeric"] = df.select_dtypes(include=[np.number]).columns.tolist()
        self.column_metadata["categorical"] = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.column_metadata["date"] = df.select_dtypes(include=['datetime64']).columns.tolist()

    def process(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Main execution pipeline: Load -> Standardize -> Dates -> Clean -> Metadata
        """
        try:
            logger.info(f"Attempting to load: {file_path}")
            # Low_memory=False prevents DtypeWarnings in large files
            df = pd.read_csv(file_path, low_memory=False)
            
            # 1. Standardize Names
            df = self.standardize_column_names(df)
            
            # 2. Convert Dates
            df = self.detect_and_convert_dates(df)
            
            # 3. Clean Missing Values
            df = self.clean_missing_values(df)
            
            # 4. Final metadata detection
            self.update_metadata(df)
            
            self.df = df
            logger.info(f"Processing complete. Shape: {df.shape}")
            return df, self.column_metadata
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

if __name__ == "__main__":
    # Quick test logic
    print("Data Processor module ready.")
