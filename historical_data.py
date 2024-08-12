import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_name = 'NVDA_2015-01-01_2023-09-28'

# Load historical data
data = pd.read_csv(f'csv/{file_name}.csv', parse_dates=['Date'], index_col='Date')

# Calculate moving averages
start_rolling = 45
end_rolling = 90
data['start_rolling'] = data['Adj Close'].rolling(window=start_rolling).mean()
data['end_rolling'] = data['Adj Close'].rolling(window=end_rolling).mean()

# Generate signals
data['signal'] = 0
data['signal'] = np.where(data['start_rolling'] > data['end_rolling'], 1, -1)

# position 1 indicating buy, -1 indicating sell, 0 indicating hold
# The diff() function subtracts the previous row's value from the current row's value.
# Create trading orders
# Calculate the position as the difference in signals (change in signal)
# data['position'] = data['signal']
data['position'] = data['signal'].diff().fillna(0)
# remove null values
data.dropna(inplace=True)


###################################################################
# Plotting the data
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot Adjusted Close Price and Moving Averages on the primary y-axis
ax1.plot(data.index, data['Adj Close'], label='Adjusted Close', color='blue', linewidth=1.5)
ax1.plot(data.index, data['start_rolling'], label='start_rolling-Day Moving Avg', color='green', linestyle='--', linewidth=1)
ax1.plot(data.index, data['end_rolling'], label='end_rolling-Day Moving Avg', color='red', linestyle='--', linewidth=1)

ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.legend(loc='upper left')
ax1.grid(True)

# Plot Positions on the secondary y-axis
ax2 = ax1.twinx()
ax2.plot(data.index, data['position'], label='Position', color='purple', linewidth=1)
ax2.set_ylabel('Position')
ax2.legend(loc='upper right')


# Set plot title
plt.title(f'{file_name} price chart')
# Show the plot
plt.show()
# ##################################################################


# ##################################################################
# bnh as buy and hold returns
# Ensure previous calculations are based on the updated `position`
# Calculate the logarithmic returns for the buy-and-hold strategy
data['bnh_returns'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))

# Strategy returns: multiply buy-and-hold returns by the previous day's position
# This captures the returns when you are in a position (long or short)
data['strategy_returns'] = data['bnh_returns'] * data['signal'].shift(1)


# Handle any NaN values that might be generated due to shifts
data.dropna(inplace=True)



# Plotting the data
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot Adjusted Close Price and Moving Averages on the primary y-axis
ax1.plot(data.index, data['bnh_returns'].cumsum(), label='Buy & Sell returns', color='blue', linewidth=1.5)
ax1.plot(data.index, data['strategy_returns'].cumsum(), label='Strategy Returns', color='red', linewidth=1)

ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.legend(loc='upper left')
ax1.grid(True)

# Set plot title
plt.title(f'{file_name} Returns')
# Show the plot
plt.show()
# ##################################################################


# Filter the DataFrame where 'position' equals 1
# filtered_data = data[data['position'] == 1]
# print(filtered_data)
# print(data[data['position'] == -1])
# print(data[data['position'] == 0])

print("Note: This calculates the natural logarithm of the daily return ratio.\n The logarithmic return is used to compute continuous compounded returns \n and is preferred for financial analysis because it provides time-additive properties")
# Actual returns
actual_returns = data[['bnh_returns', 'strategy_returns']].sum()
print(f'Ratio of Buy & Hold and Strategy Returns:')
print(actual_returns)
print()
# For 100 Rs
rs_100 = np.round(np.exp(actual_returns) * 100, 2)
print(f'If we invest Rs 100, it converts to:')
print(rs_100)
print()
