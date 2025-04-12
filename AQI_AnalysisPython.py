import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the dataset
df = pd.read_csv('C:/Users/yashr/Downloads/Air_Quality_Index.csv')

# Display basic info and handle missing values
print(df.info())
print(df.isnull().sum())

for col in ['pollutant_min', 'pollutant_max', 'pollutant_avg']:
    df[col] = df[col].fillna(df[col].median())

print(df.isnull().sum())

# EDA

# Chart 1: KDE Plot of Pollutant Average
plt.figure(figsize=(10, 5))
sns.set_theme(style="whitegrid")
sns.kdeplot(df['pollutant_avg'], fill=True, color='skyblue')
plt.title('Density Plot of Pollutant Averages')
plt.xlabel('Average Pollutant Level')
plt.ylabel('Density')
plt.show()
#Most monitoring stations report low to moderate pollutant averages, with a gradual tapering as values increase.

# Chart 2: Average Pollution by Region Category (if available)
if 'region' in df.columns:
    region_avg = df.groupby('region')['pollutant_avg'].mean().sort_values()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=region_avg.values, y=region_avg.index, palette='magma')
    plt.title('Average Pollution Levels by Region')
    plt.xlabel('Pollution Level')
    plt.ylabel('Region')
    plt.show()
    
#Regions differ noticeably in their pollution levels.

# Chart 3: Boxplot of Pollution Ranges Across Cities
plt.figure(figsize=(12, 6))
top_cities = df['city'].value_counts().nlargest(5).index
subset = df[df['city'].isin(top_cities)]
sns.boxplot(x='city', y='pollutant_max', data=subset, palette='Set2')
plt.title('Pollutant Max Values in Top Cities')
plt.xlabel('City')
plt.ylabel('Max Pollutant Level')
plt.show()
#Some cities exhibit wide variability with extreme outliers in pollutant_max, pointing to temporary pollution spikes (e.g., festivals, construction, traffic).

# Chart 4: Heatmap Between Latitude, Longitude & Pollutant Level (Binned)
df['lat_bin'] = pd.cut(df['latitude'], bins=10)
df['long_bin'] = pd.cut(df['longitude'], bins=10)
grid = df.groupby(['lat_bin', 'long_bin'])['pollutant_avg'].mean().unstack()
plt.figure(figsize=(10, 8))
sns.heatmap(grid, cmap='Spectral', linewidths=0.5)
plt.title('Spatial Heatmap of Average Pollution')
plt.xlabel('Longitude Bin')
plt.ylabel('Latitude Bin')
plt.show()
#Certain bins (grid zones) show concentration of higher pollution, possibly corresponding to industrial zones or high-density urban clusters.

# Chart 5: Pollutant Type Share (Pie Chart)
pollutant_counts = df['pollutant_id'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(pollutant_counts, labels=pollutant_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Distribution of Pollutant Types Monitored')
plt.axis('equal')
plt.show()
#Some pollutants (like PM2.5 or NO₂) are monitored far more frequently than others.

# Chart 6: Pollution Level Variation (Min vs Max)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='pollutant_min', y='pollutant_max', hue='pollutant_avg', palette='coolwarm', alpha=0.7)
plt.title('Pollution Level Variation (Min vs Max)')
plt.xlabel('Minimum Pollutant Level')
plt.ylabel('Maximum Pollutant Level')
plt.legend(title='Average Level')
plt.grid(True)
plt.show()
# Insight: This chart compares minimum and maximum pollutant levels for all data points. A wide spread between min and max suggests significant short-term pollution spikes in some locations. Places with consistently high min and max values likely face constant exposure to pollutants.

# New Chart 7: Linear Regression Plot between Pollutant Min and Max
plt.figure(figsize=(10, 6))
sns.regplot(x='pollutant_min', y='pollutant_max', data=df, 
            scatter_kws={'alpha':0.3, 'color':'blue'}, 
            line_kws={'color':'red', 'linewidth':2})
plt.title('Linear Regression: Pollutant Min vs Max Levels')
plt.xlabel('Minimum Pollutant Level')
plt.ylabel('Maximum Pollutant Level')
plt.grid(True)

# Calculate and display regression statistics
X = df[['pollutant_min']]
y = df['pollutant_max']
model = LinearRegression()
model.fit(X, y)
r_sq = model.score(X, y)
plt.text(0.05, 0.95, f'R² = {r_sq:.2f}\ny = {model.coef_[0]:.2f}x + {model.intercept_:.2f}', 
         transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))

plt.show()
# Insight: The regression plot shows the relationship between minimum and maximum pollutant levels. 
# A strong positive relationship (high R²) suggests that locations with higher baseline pollution 
# (min levels) tend to experience proportionally higher pollution spikes (max levels).