import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Professional styling
plt.style.use('ggplot')
sns.set_palette("magma")

def generate_logistics_visuals():
    # Load the cleaned data (or raw if cleaned doesn't exist)
    if os.path.exists('Data/cleaned_data.csv'):
        df = pd.read_csv('Data/cleaned_data.csv')
    else:
        # Fallback to engineering features if necessary
        df = pd.read_csv('Data/orders.csv')
        df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\d+)').astype(float)
        df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'], errors='coerce')
        df['hour'] = df['Time_Orderd'].dt.hour
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], dayfirst=True, errors='coerce')
        df['day'] = df['Order_Date'].dt.dayofweek

    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')

    # --- VIZ 1: Hourly Demand Peaks ---
    plt.figure(figsize=(10, 6))
    sns.histplot(df['hour'], bins=24, kde=True, color='purple', alpha=0.6)
    plt.title('Logistics Planning: Peak Order Volumes by Hour', fontsize=14)
    plt.xlabel('Hour of Day (24h)', fontsize=12)
    plt.ylabel('Total Orders', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.savefig('visualizations/hourly_demand.png')
    print("✓ Saved hourly_demand.png")

    # --- VIZ 2: Delivery Performance by Day ---
    plt.figure(figsize=(10, 6))
    day_map = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
    df['day_name'] = df['day'].map(day_map)
    sns.boxplot(x='day_name', y='Time_taken(min)', data=df, palette='viridis', order=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.title('Operational Efficiency: Delivery Duration by Day', fontsize=14)
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Time Taken (Minutes)', fontsize=12)
    plt.savefig('visualizations/daily_efficiency.png')
    print("✓ Saved daily_efficiency.png")

    # --- VIZ 3: Heatmap of Demand (Hour vs Day) ---
    plt.figure(figsize=(12, 7))
    pivot = df.pivot_table(index='day_name', columns='hour', values='Time_taken(min)', aggfunc='count').fillna(0)
    pivot = pivot.reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    sns.heatmap(pivot, cmap='YlGnBu', annot=False, cbar_kws={'label': 'Order Intensity'})
    plt.title('Strategic Heatmap: Order Density Across the Week', fontsize=14)
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Day of Week', fontsize=12)
    plt.savefig('visualizations/demand_heatmap.png')
    print("✓ Saved demand_heatmap.png")

if __name__ == "__main__":
    print("Generating logistics insights for Food Delivery project...")
    generate_logistics_visuals()
