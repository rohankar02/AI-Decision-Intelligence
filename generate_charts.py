import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def create_charts():
    print("Loading data...")
    df = pd.read_csv('Data/cleaned_data.csv')
    
    os.makedirs('visualizations', exist_ok=True)

    # Clean up hours and days to integers for better chart labels
    df = df.dropna(subset=['hour', 'day'])
    df['hour'] = df['hour'].astype(int)
    df['day'] = df['day'].astype(int)

    # 1. Orders by Day
    print("Generating Orders by Day chart...")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='day', data=df, hue='day', palette='viridis', legend=False)
    plt.title('Orders by Day of Week (0 = Monday, 6 = Sunday)')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Orders')
    plt.savefig('visualizations/orders_by_day.png', bbox_inches='tight', dpi=300)
    plt.close()

    # 2. Delivery Time Analysis (by Hour)
    print("Generating Delivery Time Analysis chart...")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='Time_taken(min)', data=df, hue='hour', palette='coolwarm', legend=False)
    plt.title('Delivery Time Analysis by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Time Taken (minutes)')
    plt.savefig('visualizations/delivery_time_analysis.png', bbox_inches='tight', dpi=300)
    plt.close()

    # 3. Correlation Heatmap
    print("Generating Heatmap...")
    plt.figure(figsize=(10, 8))
    numeric_cols = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Time_taken(min)', 'hour', 'day', 'month', 'weekend']
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='YlGnBu', fmt='.2f', square=True)
    plt.title('Feature Correlation Heatmap')
    plt.savefig('visualizations/heatmap.png', bbox_inches='tight', dpi=300)
    plt.close()

    # 4. Orders by Hour
    print("Generating Orders by Hour chart...")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='hour', data=df, hue='hour', palette='mako', legend=False)
    plt.title('Total Orders by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Orders')
    plt.savefig('visualizations/orders_by_hour.png', bbox_inches='tight', dpi=300)
    plt.close()

    print("Successfully saved all charts to the 'visualizations' folder.")

if __name__ == "__main__":
    create_charts()
