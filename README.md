# ts_llm_prediction
Masters Thesis Paper research project aiming to build algorithmic trading models

# Stocks Data Collection (SP500)
Script takes all stocks seen in `SP500` at least once and requests **daily** `OHLCV` data from YahooFinance (old stocks may not exist in YF database)
<br>

# Collection of aditional Financial & MacroEconomic Indicators 
- `VIX` - Volatility Indicator ([YFinance](https://finance.yahoo.com/quote/%5EVIX/))
- `GOLD` - Gold price ([YFinance](https://finance.yahoo.com/quote/GC=F/))
- `DXY` - US Dollar Index - measure of the value of the U.S. dollar relative to a basket of major foreign currencies - ([YFinance](https://finance.yahoo.com/quote/DX-Y.NYB/))
- `Yield Curve Rates` - interest rates of bonds (usually government bonds) plotted across different maturities - ([source](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2024))
- `FFER` - Federal Funds Effective Rate - the interest rate at which banks lend reserve balances to each other overnight in the US ([source](https://fred.stlouisfed.org/series/FEDFUNDS))

---

# Indicators + Signals used
### Technical Indicators Glossary

- `SMA (Simple Moving Average)`  
  A basic moving average calculated by taking the arithmetic mean of a given set of prices over a specific period of time.

- `EMA (Exponential Moving Average)`  
  A type of moving average that gives more weight to recent prices, making it more responsive to new information.

- `RSI (Relative Strength Index)`  
  A momentum oscillator that measures the speed and change of price movements, typically used to identify overbought or oversold conditions.

- `MACD (Moving Average Convergence Divergence)`  
  A trend-following momentum indicator that shows the relationship between two EMAs and helps identify bullish or bearish momentum.

- `Bollinger Bands`  
  A volatility indicator consisting of a middle SMA and two price bands above and below it, typically two standard deviations away.

- `ATR (Average True Range)`  
  A volatility indicator that measures the degree of price movement or volatility for an asset over a specific time period.

- `OBV (On-Balance Volume)` 
  A volume-based indicator that uses cumulative volume flow to predict changes in stock price. <br>
<br>
---

### Trading Signal Descriptions

- `Signal_SMA`  
  A short-term trend signal: `1` if SMA(20) is above SMA(50), indicating upward momentum; `0` otherwise.

- `Signal_MACD`  
  A momentum signal: `1` if the MACD line is above the signal line (bullish); `0` otherwise.

- `Signal_RSI`  
  A mean-reversion signal based on the RSI value:  
  - `1` if RSI < 30 (oversold, potential Buy)  
  - `-1` if RSI > 70 (overbought, potential Sell)  
  - `0` otherwise

- `Signal_SMA_Cross`  
  A long-term trend signal:  
  - `1` if SMA(50) > SMA(200) (bullish "Golden Cross")  
  - `-1` if SMA(50) < SMA(200) (bearish "Death Cross")  
  - `0` if no clear trend
