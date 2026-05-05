import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(filename="sample_business_data.csv"):
    """Generates a realistic business dataset for testing the AI Decision System."""
    
    np.random.seed(42)
    rows = 500
    
    # 1. Dates
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i//5) for i in range(rows)]
    
    # 2. Categories & Products
    categories = ['Electronics', 'Home Office', 'Software', 'Consulting']
    category_list = np.random.choice(categories, rows, p=[0.3, 0.4, 0.2, 0.1])
    
    # 3. Revenue (Adding some seasonality/trends)
    base_revenue = np.random.uniform(50, 200, rows)
    # Add a growth trend
    trend = np.linspace(1, 1.5, rows)
    revenue = base_revenue * trend
    
    # 4. Customers
    customer_ids = np.random.randint(1001, 1150, rows) # 150 unique customers (allows for repeat rate)
    
    df = pd.DataFrame({
        'Date': dates,
        'Category': category_list,
        'Revenue': revenue.round(2),
        'Customer_ID': customer_ids,
        'Order_Status': 'Completed'
    })
    
    df.to_csv(filename, index=False)
    print(f"✅ Success! Sample data generated: {filename}")

if __name__ == "__main__":
    generate_sample_data()
