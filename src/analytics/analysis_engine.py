import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AnalysisEngine:
    """
    Performs deep exploratory analysis to identify patterns, anomalies, 
    and segments. Results are structured for LLM consumption.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def run_exploratory_analysis(
        self, 
        revenue_col: str = 'revenue', 
        date_col: str = 'date', 
        segment_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a full suite of analysis and returns a structured report.
        """
        analysis_report = {
            "top_segments": self._analyze_segments(revenue_col, segment_col),
            "anomalies": self._detect_anomalies(revenue_col, date_col),
            "seasonality": self._analyze_seasonality(revenue_col, date_col),
            "trend_health": self._analyze_trends(revenue_col, date_col)
        }
        
        logger.info("Exploratory analysis completed.")
        return analysis_report

    def _analyze_segments(self, revenue_col: str, segment_col: Optional[str]) -> List[Dict]:
        """Identifies top performing categories/segments."""
        if not segment_col or segment_col not in self.df.columns:
            # Try to auto-detect a categorical column if not provided
            cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
            if len(cat_cols) > 0:
                segment_col = cat_cols[0]
                logger.info(f"Auto-selected '{segment_col}' for segment analysis.")
            else:
                return []

        segment_data = (
            self.df.groupby(segment_col)[revenue_col]
            .agg(['sum', 'count', 'mean'])
            .sort_values(by='sum', ascending=False)
            .head(5)
            .reset_index()
        )
        return segment_data.to_dict(orient='records')

    def _detect_anomalies(self, revenue_col: str, date_col: str) -> List[Dict]:
        """Detects revenue spikes/drops using Z-score (Standard Deviations)."""
        # Aggregate to daily revenue for anomaly detection
        daily_rev = self.df.groupby(self.df[date_col].dt.date)[revenue_col].sum().reset_index()
        
        if len(daily_rev) < 5: # Not enough data for stats
            return []

        mean = daily_rev[revenue_col].mean()
        std = daily_rev[revenue_col].std()
        
        # Z-score > 2 (Significant) or 3 (Extreme)
        daily_rev['z_score'] = (daily_rev[revenue_col] - mean) / std
        anomalies = daily_rev[abs(daily_rev['z_score']) > 2].copy()
        
        anomalies['type'] = anomalies['z_score'].apply(lambda x: 'Spike' if x > 0 else 'Drop')
        anomalies[date_col] = anomalies[date_col].astype(str)
        
        return anomalies[[date_col, revenue_col, 'type', 'z_score']].to_dict(orient='records')

    def _analyze_seasonality(self, revenue_col: str, date_col: str) -> Dict[str, Any]:
        """Identifies patterns by Day of Week and Month."""
        # Day of Week Performance
        dow_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        self.df['day_of_week'] = self.df[date_col].dt.dayofweek
        dow_analysis = self.df.groupby('day_of_week')[revenue_col].mean().to_dict()
        dow_analysis = {dow_map[k]: round(v, 2) for k, v in dow_analysis.items()}

        # Month of Year Performance
        self.df['month'] = self.df[date_col].dt.month
        month_analysis = self.df.groupby('month')[revenue_col].mean().to_dict()
        
        return {
            "best_days": sorted(dow_analysis.items(), key=lambda x: x[1], reverse=True),
            "monthly_averages": month_analysis
        }

    def _analyze_trends(self, revenue_col: str, date_col: str) -> Dict[str, Any]:
        """Identifies if the general trend is declining or growing."""
        monthly_rev = self.df.set_index(date_col).resample('ME')[revenue_col].sum()
        
        if len(monthly_rev) < 2:
            return {"status": "Insufficient data for trend analysis"}

        recent_growth = monthly_rev.pct_change().iloc[-1]
        
        status = "Growing" if recent_growth > 0.05 else "Declining" if recent_growth < -0.05 else "Stable"
        
        return {
            "recent_growth_rate": round(recent_growth * 100, 2),
            "overall_status": status,
            "is_declining": recent_growth < 0
        }

if __name__ == "__main__":
    print("Analysis Engine module ready.")
