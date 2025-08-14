# Railway TAAPI.io Endpoints - All 208+ Indicators

## How It Works for ChatGPT

**ChatGPT reads this file** → **Sees all available indicators** → **Chooses which ones to call** → **Makes Railway API requests**

## Base URL
```
https://titan-trading-2-production.up.railway.app/api/taapi
```

## Universal Endpoint Structure
```
GET /api/taapi/{indicator}?symbol={SYMBOL}&exchange={EXCHANGE}&interval={INTERVAL}&{params}
```

## Core Parameters (All Indicators)
- `symbol`: Trading pair (e.g., BTC/USDT, ETH/USDT)
- `exchange`: binance, bybit, kraken, coinbase, kucoin
- `interval`: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

## Available Indicators by Category

### 🚀 Momentum Indicators (Most Popular)
```
/api/taapi/rsi          - RSI (Relative Strength Index)
/api/taapi/macd         - MACD (Moving Average Convergence Divergence)  
/api/taapi/stoch        - Stochastic Oscillator
/api/taapi/stochrsi     - Stochastic RSI
/api/taapi/adx          - Average Directional Index
/api/taapi/cci          - Commodity Channel Index
/api/taapi/mfi          - Money Flow Index
/api/taapi/willr        - Williams %R
/api/taapi/roc          - Rate of Change
/api/taapi/mom          - Momentum
/api/taapi/trix         - TRIX
/api/taapi/ultosc       - Ultimate Oscillator
/api/taapi/aroon        - Aroon Indicator
/api/taapi/aroonosc     - Aroon Oscillator
/api/taapi/cmo          - Chande Momentum Oscillator
```

### 📊 Volume Indicators
```
/api/taapi/obv          - On Balance Volume
/api/taapi/ad           - Accumulation/Distribution
/api/taapi/adosc        - A/D Oscillator
/api/taapi/chaikin      - Chaikin A/D Line
/api/taapi/mfi          - Money Flow Index
/api/taapi/nvi          - Negative Volume Index
/api/taapi/pvi          - Positive Volume Index
/api/taapi/eom          - Ease of Movement
/api/taapi/vwap         - Volume Weighted Average Price
/api/taapi/vwma         - Volume Weighted Moving Average
/api/taapi/fi           - Force Index
/api/taapi/emv          - Ease of Movement Value
/api/taapi/cmf          - Chaikin Money Flow
```

### 📈 Trend Indicators
```
/api/taapi/ema          - Exponential Moving Average
/api/taapi/sma          - Simple Moving Average
/api/taapi/dema         - Double Exponential MA
/api/taapi/tema         - Triple Exponential MA
/api/taapi/trima        - Triangular Moving Average
/api/taapi/kama         - Kaufman Adaptive MA
/api/taapi/mama         - MESA Adaptive MA
/api/taapi/t3           - T3 Moving Average
/api/taapi/wma          - Weighted Moving Average
/api/taapi/ht_trendline - Hilbert Transform Trendline
/api/taapi/linearreg    - Linear Regression
/api/taapi/supertrend   - SuperTrend
```

### 🎯 Volatility Indicators
```
/api/taapi/bbands       - Bollinger Bands
/api/taapi/atr          - Average True Range
/api/taapi/natr         - Normalized ATR
/api/taapi/trange       - True Range
/api/taapi/stddev       - Standard Deviation
/api/taapi/var          - Variance
/api/taapi/beta         - Beta Coefficient
/api/taapi/correl       - Pearson Correlation
```

### 🔄 Cycle Indicators
```
/api/taapi/ht_dcperiod  - Hilbert Transform Dominant Cycle Period
/api/taapi/ht_dcphase   - Hilbert Transform Dominant Cycle Phase
/api/taapi/ht_phasor    - Hilbert Transform Phasor Components
/api/taapi/ht_sine      - Hilbert Transform SineWave
/api/taapi/ht_trendmode - Hilbert Transform Trend Mode
```

### 💰 Price Transform
```
/api/taapi/avgprice     - Average Price
/api/taapi/medprice     - Median Price
/api/taapi/typprice     - Typical Price
/api/taapi/wclprice     - Weighted Close Price
```

### 🎨 Pattern Recognition (50+ Candlestick Patterns)
```
/api/taapi/cdldoji      - Doji
/api/taapi/cdlhammer    - Hammer
/api/taapi/cdlengulfing - Engulfing Pattern
/api/taapi/cdlharami    - Harami Pattern
/api/taapi/cdldragonflydoji - Dragonfly Doji
/api/taapi/cdl3blackcrows - Three Black Crows
/api/taapi/cdl3whitesoldiers - Three White Soldiers
/api/taapi/cdlmorningstar - Morning Star
/api/taapi/cdleveningstar - Evening Star
/api/taapi/cdlshootingstar - Shooting Star
```

### 📐 Statistics & Math
```
/api/taapi/linearreg_angle - Linear Regression Angle
/api/taapi/linearreg_intercept - Linear Regression Intercept
/api/taapi/linearreg_slope - Linear Regression Slope
/api/taapi/tsf          - Time Series Forecast
/api/taapi/beta         - Beta Coefficient
/api/taapi/correl       - Correlation Coefficient
```

### 🔢 Mathematical Transforms
```
/api/taapi/acos         - Arc Cosine
/api/taapi/asin         - Arc Sine
/api/taapi/atan         - Arc Tangent
/api/taapi/cos          - Cosine
/api/taapi/sin          - Sine
/api/taapi/tan          - Tangent
/api/taapi/sqrt         - Square Root
/api/taapi/ln           - Natural Logarithm
/api/taapi/log10        - Base-10 Logarithm
/api/taapi/exp          - Exponential
```

## Example Usage Scenarios

### 🎯 For Quick Analysis (ChatGPT chooses 3-5 indicators)
```
1. Read this file
2. Choose: RSI, MACD, Bollinger Bands
3. Call: 
   - GET /api/taapi/rsi?symbol=BTC/USDT&exchange=binance&interval=1h
   - GET /api/taapi/macd?symbol=BTC/USDT&exchange=binance&interval=1h  
   - GET /api/taapi/bbands?symbol=BTC/USDT&exchange=binance&interval=1h
```

### 🔍 For Deep Analysis (ChatGPT chooses 10-15 indicators)
```
1. Momentum: RSI, MACD, Stochastic, ADX
2. Volume: OBV, MFI, A/D Line
3. Trend: EMA, SMA, SuperTrend  
4. Volatility: Bollinger Bands, ATR
5. Patterns: Doji, Hammer, Engulfing
```

### 📊 For Confluence Analysis (ChatGPT combines categories)
```
1. Choose indicators from different categories
2. Look for agreement across momentum + volume + trend
3. Generate confluence score based on agreement
```

## Special Parameters by Indicator

### RSI
- `period`: Period (default: 14)

### MACD  
- `fast`: Fast period (default: 12)
- `slow`: Slow period (default: 26) 
- `signal`: Signal period (default: 9)

### Bollinger Bands
- `period`: Period (default: 20)
- `stddev`: Standard deviations (default: 2.0)

### Moving Averages
- `period`: Period (default: 20)

### Stochastic
- `fastk_period`: %K period (default: 5)
- `slowk_period`: %K slow period (default: 3)
- `slowd_period`: %D period (default: 3)

## Response Format
```json
{
  "indicator": "rsi",
  "symbol": "BTC/USDT", 
  "exchange": "binance",
  "interval": "1h",
  "result": {
    "value": 52.25
  },
  "timestamp": "2025-08-09T06:30:00Z"
}
```

## ChatGPT Integration Strategy

1. **Read this file** to see all available indicators
2. **Choose appropriate indicators** based on analysis type:
   - Quick scan: 3-5 core indicators
   - Deep analysis: 10-15 indicators across categories
   - Pattern recognition: Include candlestick patterns
3. **Make Railway API calls** to get real-time data
4. **Combine results** for confluence analysis
5. **Generate trading insights** based on indicator agreement

## Advantages of This Approach

✅ **Dynamic Selection**: ChatGPT chooses which indicators to use
✅ **Real-Time Data**: All indicators use live market data
✅ **No Rate Limits**: Railway server handles TAAPI rate limiting
✅ **Complete Coverage**: Access to all 208+ indicators
✅ **Smart Analysis**: ChatGPT can adapt indicator selection to market conditions
✅ **Confluence Scoring**: Combine multiple indicators for stronger signals