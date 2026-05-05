import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MetricsEngine:
    """
    Computes business-critical KPIs and trends from a cleaned dataset.
    Designed for scalability and reuse across different business models.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_all_kpis(
        self, 
        revenue_col: str = 'revenue', 
        customer_col: str = 'customer_id', 
        date_col: str = 'date'
    ) -> Dict[str, Any]:
        """
        Main entry point to compute the KPI suite.
        Returns a structured dictionary of metrics.
        """
        try:
            # Check if required columns exist
            missing = [col for col in [revenue_col, customer_col, date_col] if col not in self.df.columns]
            if missing:
                logger.error(f"Missing columns for KPI calculation: {missing}")
                # Try to fall back to 'sales' if 'revenue' is missing
                if 'revenue' in missing and 'sales' in self.df.columns:
                    revenue_col = 'sales'
                    logger.info("Falling back to 'sales' column for revenue.")
                else:
                    return {"error": f"Missing columns: {missing}"}

            results = {
                "summary": self._compute_summary(revenue_col, customer_col),
                "trends": self._compute_trends(revenue_col, date_col),
                "retention": self._compute_retention(customer_col)
            }
            
            logger.info("Successfully calculated all KPIs.")
            return results

        except Exception as e:
            logger.error(f"Error in metrics calculation: {e}")
            return {"error": str(e)}

    def _compute_summary(self, revenue_col: str, customer_col: str) -> Dict[str, float]:
        """Calculates snapshot metrics: Total Revenue, AOV, etc."""
        total_revenue = float(self.df[revenue_col].sum())
        total_orders = len(self.df)
        unique_customers = int(self.df[customer_col].nunique())
        
        aov = total_revenue / total_orders if total_orders > 0 else 0
        revenue_per_customer = total_revenue / unique_customers if unique_customers > 0 else 0

        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "unique_customers": unique_customers,
            "average_order_value": round(aov, 2),
            "revenue_per_customer": round(revenue_per_customer, 2)
        }

    def _compute_trends(self, revenue_col: str, date_col: str) -> Dict[str, Any]:
        """Calculates revenue trends over time (Daily/Monthly)."""
        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            return {"error": f"Column {date_col} is not datetime type."}

        # Monthly Trend
        monthly_trend = (
            self.df.groupby(pd.Grouper(key=date_col, freq='ME'))[revenue_col]
            .sum()
            .reset_index()
        )
        
        # Convert date to string for JSON serialization
        monthly_trend[date_col] = monthly_trend[date_col].dt.strftime('%Y-%m')
        
        # Calculate Growth Rate
        monthly_trend['growth_rate'] = monthly_trend[revenue_col].pct_change() * 100

        return monthly_trend.to_dict(orient='records')

    def _compute_retention(self, customer_col: str) -> Dict[str, Any]:
        """Calculates customer loyalty metrics."""
        order_counts = self.df[customer_col].value_counts()
        total_customers = len(order_counts)
        
        if total_customers == 0:
            return {"repeat_customer_rate": 0}

        repeat_customers = int((order_counts > 1).sum())
        repeat_rate = (repeat_customers / total_customers) * 100

        return {
            "repeat_customers": repeat_customers,
            "one_time_customers": total_customers - repeat_customers,
            "repeat_customer_rate_percent": round(repeat_rate, 2)
        }

if __name__ == "__main__":
    print("Metrics Engine module ready.")
