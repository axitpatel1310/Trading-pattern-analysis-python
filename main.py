# Install required packages if you don't have them:
# pip install pandas plotly TA-Lib

import pandas as pd
import plotly.graph_objects as go
import talib

# -----------------------------
# Step 1: Load CSV Data
# -----------------------------
file_path = 'data.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Ensure proper datetime format
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# -----------------------------
# Step 2: Detect Candlestick Patterns
# -----------------------------
patterns = {
    'Morning Star': talib.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close']),
    'Evening Star': talib.CDLEVENINGSTAR(df['Open'], df['High'], df['Low'], df['Close']),
    'Doji': talib.CDLDOJI(df['Open'], df['High'], df['Low'], df['Close']),
    'Bullish Engulfing': talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close']),
    'Bearish Engulfing': talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close']) * -1,
    'Hammer': talib.CDLHAMMER(df['Open'], df['High'], df['Low'], df['Close']),
    'Hanging Man': talib.CDLHANGINGMAN(df['Open'], df['High'], df['Low'], df['Close'])
}

fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    increasing_line_color='green',
    decreasing_line_color='red',
    name='Candlesticks'
)])

# -----------------------------
# Step 4: Overlay Patterns
# -----------------------------
marker_colors = {
    'Morning Star': 'blue',
    'Evening Star': 'orange',
    'Doji': 'purple',
    'Bullish Engulfing': 'green',
    'Bearish Engulfing': 'red',
    'Hammer': 'pink',
    'Hanging Man': 'brown'
}

marker_symbols = {
    'Morning Star': 'triangle-up',
    'Evening Star': 'triangle-down',
    'Doji': 'star',
    'Bullish Engulfing': 'circle',
    'Bearish Engulfing': 'circle',
    'Hammer': 'diamond',
    'Hanging Man': 'diamond'
}

for pattern_name, pattern_values in patterns.items():
    pattern_dates = df['Date'][pattern_values != 0]
    if not pattern_dates.empty:
        # Choose Y positions slightly above/below for visibility
        if pattern_name in ['Morning Star', 'Bullish Engulfing', 'Hammer']:
            y_vals = df.loc[pattern_values != 0, 'Low'] * 0.995
        else:
            y_vals = df.loc[pattern_values != 0, 'High'] * 1.005
        
        fig.add_trace(go.Scatter(
            x=pattern_dates,
            y=y_vals,
            mode='markers',
            marker=dict(
                color=marker_colors[pattern_name],
                size=12,
                symbol=marker_symbols[pattern_name]
            ),
            name=pattern_name
        ))

# -----------------------------
# Step 5: Layout
# -----------------------------
fig.update_layout(
    title='Apex Trading (Akkyaaa)',
    xaxis_title='Date',
    yaxis_title='Price (₹)',
    template='plotly_dark',
    xaxis_rangeslider_visible=False
)

fig.show()
