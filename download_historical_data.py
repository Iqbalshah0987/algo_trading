import yfinance as yf

# Download historical data for a specific stock
# ticker = 'OLAELEC.NS'
ticker = 'AAPL'
start_date = "2015-01-01"
end_date = "2020-01-01"
df = yf.download(ticker, start=start_date, end=end_date)

# Flatten the multi-level columns
# df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Save to CSV
df.to_csv(f'csv/{ticker}_{start_date}_{end_date}.csv')


# data = df.head()
# data = df.tail()
# print(data)
# adj_close_prices = df['Adj Close']
# adj_close_prices_desc = adj_close_prices.describe()
# print(adj_close_prices_desc)

