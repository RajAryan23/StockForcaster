import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller

# Reading the dataset using read_csv
df = pd.read_csv("stock_data.csv", 
                 parse_dates=True, 
                 index_col="Date")

# Deleting unwanted column
df.drop(columns='Unnamed: 0', inplace=True)

# Displaying the first five rows of dataset
print(df.head())

# Plotting Line plot for Time Series data
sns.set(style="whitegrid")  # Setting the style to whitegrid for a clean background

plt.figure(figsize=(12, 6))  # Setting the figure size
sns.lineplot(data=df, x=df.index, y='High', label='High Price', color='blue')

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('High')
plt.title('Share Highest Price Over Time')

plt.show()

# Resampling
df_resampled = df.resample('M').mean()  # Resampling to monthly frequency, using mean as an aggregation function

sns.set(style="whitegrid")  # Setting the style to whitegrid for a clean background

# Plotting the 'High' column with seaborn, setting x as the resampled 'Date'
plt.figure(figsize=(12, 6))  # Setting the figure size
sns.lineplot(data=df_resampled, x=df_resampled.index, y='High', label='Month Wise Average High Price', color='blue')

# Adding labels and title
plt.xlabel('Date (Monthly)')
plt.ylabel('High')
plt.title('Monthly Resampling Highest Price Over Time')

plt.show()

# Detecting Seasonality Using Auto Correlation
plt.figure(figsize=(12, 6))
plot_acf(df['Volume'], lags=40)  # You can adjust the number of lags as needed
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Function (ACF) Plot')
plt.show()

# Detecting Stationarity
result = adfuller(df['High'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:', result[4])

# Smoothening the data using Differencing and Moving Average

# Differencing
df['high_diff'] = df['High'].diff()

# Plotting Original vs Differenced High
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['High'], label='Original High', color='blue')
plt.plot(df.index, df['high_diff'], label='Differenced High', linestyle='--', color='green')
plt.legend()
plt.title('Original vs Differenced High')
plt.show()

# Moving Average
window_size = 120
df['high_smoothed'] = df['High'].rolling(window=window_size).mean()

# Plotting Original vs Moving Average
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['High'], label='Original High', color='blue')
plt.plot(df.index, df['high_smoothed'], label=f'Moving Average (Window={window_size})', linestyle='--', color='orange')

plt.xlabel('Date')
plt.ylabel('High')
plt.title('Original vs Moving Average')
plt.legend()
plt.show()

# Original Data Vs Differenced Data
# Create a DataFrame with 'High' and 'high_diff' columns side by side
df_combined = pd.concat([df['High'], df['high_diff']], axis=1)

# Display the combined DataFrame
print(df_combined.head())

# Remove rows with missing values in 'high_diff'
df.dropna(subset=['high_diff'], inplace=True)
print(df['high_diff'].head())

# Conduct the ADF test on differenced data
result = adfuller(df['high_diff'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:', result[4])
