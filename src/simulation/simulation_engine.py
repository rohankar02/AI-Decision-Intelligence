import pandas as pd
import numpy as np
from typing import Dict, Any, List

class SimulationEngine:
    """
    Models business decisions by comparing current KPIs against 
    predicted outcomes (Before vs. After).
    """

    def __init__(self, current_kpis: Dict[str, Any]):
        self.summary = current_kpis['summary']
        self.retention = current_kpis['retention']

    def simulate_scenario(self, scenario_type: str, change_pct: float) -> Dict[str, Any]:
        """
        Main entry point for simulations. 
        Supported types: 'retention', 'price', 'customer_acquisition'
        """
        before = {
            "revenue": self.summary['total_revenue'],
            "customers": self.summary['unique_customers'],
            "repeat_rate": self.retention['repeat_customer_rate_percent']
        }
        
        after = before.copy()
        change_decimal = change_pct / 100

        if scenario_type == 'retention':
            # Increase in retention directly impacts repeat rate and revenue
            after['repeat_rate'] = min(100.0, before['repeat_rate'] * (1 + change_decimal))
            additional_repeat_revenue = before['revenue'] * (change_decimal * 0.5) # Conservative estimate
            after['revenue'] = before['revenue'] + additional_repeat_revenue
            
        elif scenario_type == 'price':
            # Price increase simulation (includes 1.5x elasticity/churn factor)
            elasticity = 1.5
            revenue_impact = (1 + change_decimal) * (1 - (elasticity * change_decimal))
            after['revenue'] = before['revenue'] * revenue_impact
            
        elif scenario_type == 'customer_acquisition':
            # New customers bring in average revenue per customer
            after['customers'] = int(before['customers'] * (1 + change_decimal))
            rev_per_cust = before['revenue'] / before['customers'] if before['customers'] > 0 else 0
            after['revenue'] = before['revenue'] + (rev_per_cust * (after['customers'] - before['customers']))

        return self._format_results(before, after)

    def compare_scenarios(self, scenarios: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Runs multiple simulations and returns a comparative dataframe.
        Expected format: [{'type': 'retention', 'value': 10, 'label': 'Strategy A'}]
        """
        results = []
        for s in scenarios:
            res = self.simulate_scenario(s['type'], s['value'])
            results.append({
                "Strategy": s['label'],
                "Simulated Revenue": res['comparison_table'][0]['After'],
                "Revenue Gain": res['total_revenue_improvement'],
                "Growth (%)": res['improvement_pct']
            })
        return pd.DataFrame(results)

    def _format_results(self, before: Dict, after: Dict) -> Dict[str, Any]:
        """Calculates deltas and formats the comparison table."""
        comparison = []
        for key in before.keys():
            b_val = before[key]
            a_val = after[key]
            delta = a_val - b_val
            pct_change = (delta / b_val * 100) if b_val != 0 else 0
            
            comparison.append({
                "Metric": key.replace("_", " ").title(),
                "Before": round(b_val, 2),
                "After": round(a_val, 2),
                "Change (%)": round(pct_change, 2)
            })

        return {
            "comparison_table": comparison,
            "total_revenue_improvement": round(after['revenue'] - before['revenue'], 2),
            "improvement_pct": round(((after['revenue'] / before['revenue']) - 1) * 100, 2) if before['revenue'] > 0 else 0
        }

if __name__ == "__main__":
    print("Simulation Engine module ready.")
