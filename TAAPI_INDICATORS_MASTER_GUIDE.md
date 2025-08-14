# TAAPI Indicators — Master Guide with Trading Use Cases

*This comprehensive guide contains 208+ technical indicators organized by trading strategy and use case for THE ALPHA PLAYBOOK v4*

## 🎯 Action Index — Indicators by Trading Use Case

### Breakout Trading
- **donchian** - Donchian Channels
- **keltner** - Keltner Channels
- **bbw** - Bollinger Bands Width
- **sar** - Parabolic SAR
- **acceleration** - Acceleration Bands

### Trend Following
- **adx** - Average Directional Movement Index
- **supertrend** - Supertrend
- **ema** - Exponential Moving Average
- **sma** - Simple Moving Average
- **hma** - Hull Moving Average

### Mean Reversion
- **rsi** - Relative Strength Index
- **stoch** - Stochastic
- **bbands** - Bollinger Bands
- **cci** - Commodity Channel Index

### Momentum Trading
- **macd** - MACD
- **ao** - Awesome Oscillator
- **roc** - Rate of Change
- **mom** - Momentum
- **trix** - TRIX

### Support/Resistance Mapping
- **pivotpoints** - Pivot Points
- **vwap** - Volume Weighted Average Price
- **fibonacciretracement** - Fibonacci Retracement
- **ichimoku** - Ichimoku Cloud

### Volatility Analysis
- **atr** - Average True Range
- **bbands** - Bollinger Bands
- **keltner** - Keltner Channels
- **stddev** - Standard Deviation

### Volume Confirmation
- **obv** - On Balance Volume
- **cmf** - Chaikin Money Flow
- **vosc** - Volume Oscillator
- **ad** - Accumulation/Distribution

### Candlestick Reversals
- **doji** - Doji
- **hammer** - Hammer
- **hangingman** - Hanging Man
- **engulfing** - Engulfing Pattern
- **morningstar** - Morning Star
- **eveningstar** - Evening Star
- **3whitesoldiers** - Three White Soldiers
- **3blackcrows** - Three Black Crows

---

## 📊 Quick Reference Cheat Sheet

### **Most Popular Indicators** (Use These First)
| Indicator | Symbol | Best For | Key Parameters |
|-----------|---------|----------|----------------|
| RSI | `rsi` | Momentum/Overbought-Oversold | period: 14 |
| MACD | `macd` | Trend Changes/Momentum | fast: 12, slow: 26, signal: 9 |
| Bollinger Bands | `bbands` | Volatility/Support-Resistance | period: 20, stddev: 2 |
| EMA | `ema` | Trend Direction | period: 20, 50, 200 |
| Stochastic | `stoch` | Momentum/Overbought-Oversold | fast: 14, slow: 3, signal: 3 |

### **Scalping Setup (1m-5m)**
| Indicator | Parameters | Signal |
|-----------|------------|--------|
| RSI | period: 14 | >70 sell, <30 buy |
| Stochastic | fast: 5, slow: 3 | >80 sell, <20 buy |
| EMA 9 | period: 9 | Price above = bullish |
| EMA 21 | period: 21 | EMA 9 > EMA 21 = uptrend |
| Bollinger Bands | period: 20, stddev: 2 | Price at bands = reversal |

### **Swing Trading Setup (1h-4h)**
| Indicator | Parameters | Signal |
|-----------|------------|--------|
| RSI | period: 14 | Divergences, >70/<30 |
| MACD | fast: 12, slow: 26, signal: 9 | Line crossovers |
| SMA 50 | period: 50 | Dynamic support/resistance |
| SMA 200 | period: 200 | Long-term trend |
| ATR | period: 14 | Volatility-based stops |

---

## 🔥 Complete Indicators Arsenal (208+ Total)

*Note: This is a condensed version. The complete guide contains detailed descriptions, parameters, and trading signals for all 208+ indicators.*

### **MOMENTUM INDICATORS**
- `rsi` - Relative Strength Index
- `stoch` - Stochastic Oscillator  
- `stochf` - Stochastic Fast
- `willr` - Williams %R
- `cci` - Commodity Channel Index
- `mfi` - Money Flow Index
- `roc` - Rate of Change
- `rocp` - Rate of Change Percentage
- `rocr` - Rate of Change Ratio
- `mom` - Momentum
- `cmo` - Chande Momentum Oscillator
- `ao` - Awesome Oscillator
- `ultosc` - Ultimate Oscillator
- `plus_di` - Plus Directional Indicator
- `minus_di` - Minus Directional Indicator
- `dx` - Directional Movement Index
- `adx` - Average Directional Movement Index
- `adxr` - Average Directional Movement Index Rating

### **TREND INDICATORS**
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `wma` - Weighted Moving Average
- `dema` - Double Exponential Moving Average
- `tema` - Triple Exponential Moving Average
- `trima` - Triangular Moving Average
- `kama` - Kaufman Adaptive Moving Average
- `mama` - MESA Adaptive Moving Average
- `hma` - Hull Moving Average
- `t3` - Triple Exponential Moving Average (T3)
- `zlema` - Zero-Lag Exponential Moving Average
- `vwma` - Volume Weighted Moving Average
- `smma` - Smoothed Moving Average
- `wilders` - Wilders Smoothing
- `supertrend` - Supertrend
- `sar` - Parabolic SAR
- `dmi` - Directional Movement Index
- `dm` - Directional Movement

### **VOLATILITY INDICATORS**
- `atr` - Average True Range
- `natr` - Normalized Average True Range
- `trange` - True Range
- `bbands` - Bollinger Bands
- `bbw` - Bollinger Bands Width
- `keltner` - Keltner Channels
- `donchian` - Donchian Channels
- `stddev` - Standard Deviation
- `var` - Variance
- `massi` - Mass Index

### **VOLUME INDICATORS**
- `obv` - On Balance Volume
- `ad` - Chaikin A/D Line
- `adosc` - Chaikin A/D Oscillator
- `cmf` - Chaikin Money Flow
- `vosc` - Volume Oscillator
- `vwap` - Volume Weighted Average Price
- `vwma` - Volume Weighted Moving Average
- `nvi` - Negative Volume Index
- `pvi` - Positive Volume Index

### **OSCILLATORS**
- `macd` - Moving Average Convergence Divergence
- `macdext` - MACD with controllable MA type
- `ppo` - Percentage Price Oscillator
- `apo` - Absolute Price Oscillator
- `trix` - TRIX
- `bop` - Balance of Power
- `dpo` - Detrended Price Oscillator
- `fosc` - Forecast Oscillator
- `kvo` - Klinger Volume Oscillator
- `tsi` - True Strength Index
- `eom` - Ease of Movement
- `vhf` - Vertical Horizontal Filter
- `fisher` - Fisher Transform
- `aroon` - Aroon
- `aroonosc` - Aroon Oscillator
- `mfi` - Money Flow Index
- `accosc` - Accelerator Oscillator
- `coppock` - Coppock Curve
- `stochrsi` - Stochastic RSI

### **PATTERN RECOGNITION**
- `doji` - Doji
- `dojistar` - Doji Star
- `dragonflydoji` - Dragonfly Doji
- `gravestonedoji` - Gravestone Doji
- `longleggeddoji` - Long Legged Doji
- `rickshawman` - Rickshaw Man
- `hammer` - Hammer
- `inverted` - Inverted Hammer
- `hangingman` - Hanging Man
- `shootingstar` - Shooting Star
- `engulfing` - Engulfing Pattern
- `harami` - Harami Pattern
- `haramicross` - Harami Cross Pattern
- `morningstar` - Morning Star
- `morningdojistar` - Morning Doji Star
- `eveningstar` - Evening Star
- `eveningdojistar` - Evening Doji Star
- `piercing` - Piercing Pattern
- `darkcloud` - Dark Cloud Cover
- `3whitesoldiers` - Three Advancing White Soldiers
- `3blackcrows` - Three Black Crows
- `3inside` - Three Inside Up/Down
- `3outside` - Three Outside Up/Down
- `3linestrike` - Three-Line Strike
- `3starsinsouth` - Three Stars In The South
- `abandonedbaby` - Abandoned Baby
- `advanceblock` - Advance Block
- `belthold` - Belt-hold
- `breakaway` - Breakaway
- `closingmarubozu` - Closing Marubozu
- `concealing` - Concealing Baby Swallow
- `counterattack` - Counterattack
- `hikkake` - Hikkake Pattern
- `hikkakemod` - Modified Hikkake Pattern
- `homingpigeon` - Homing Pigeon
- `identical3crows` - Identical Three Crows
- `inneck` - In-Neck Pattern
- `kicking` - Kicking
- `kickingbylength` - Kicking (by length)
- `ladderbottom` - Ladder Bottom
- `longlline` - Long Line Candle
- `marubozu` - Marubozu
- `mathold` - Mat Hold
- `matchinglow` - Matching Low
- `onneck` - On-Neck Pattern
- `separatinglines` - Separating Lines
- `shortline` - Short Line Candle
- `spinningtop` - Spinning Top
- `stalledpattern` - Stalled Pattern
- `sticksandwich` - Stick Sandwich
- `takuri` - Takuri
- `tasukigap` - Tasuki Gap
- `thrusting` - Thrusting Pattern
- `tristar` - Tristar Pattern
- `unique3river` - Unique 3 River
- `upsidegap2crows` - Upside Gap Two Crows
- `xsidegap3methods` - Upside/Downside Gap Three Methods

### **STATISTICAL FUNCTIONS**
- `beta` - Beta
- `correl` - Pearson's Correlation Coefficient
- `linearreg` - Linear Regression
- `linearregangle` - Linear Regression Angle
- `linearregintercept` - Linear Regression Intercept
- `linearregslope` - Linear Regression Slope
- `stddev` - Standard Deviation
- `tsf` - Time Series Forecast
- `var` - Variance

### **MATHEMATICAL OPERATORS**
- `add` - Vector Arithmetic Add
- `div` - Vector Arithmetic Divide
- `mult` - Vector Arithmetic Multiply
- `sub` - Vector Arithmetic Subtract
- `max` - Highest value over period
- `maxindex` - Index of highest value
- `min` - Lowest value over period
- `minindex` - Index of lowest value
- `minmax` - Lowest and highest values
- `minmaxindex` - Indexes of lowest/highest values
- `sum` - Summation

### **PRICE INDICATORS**
- `avgprice` - Average Price
- `medprice` - Median Price
- `typprice` - Typical Price
- `wclprice` - Weighted Close Price

### **HILBERT TRANSFORM INDICATORS**
- `ht_dcperiod` - Dominant Cycle Period
- `ht_dcphase` - Dominant Cycle Phase
- `ht_phasor` - Phasor Components
- `ht_sine` - SineWave
- `ht_trendline` - Instantaneous Trendline
- `ht_trendmode` - Trend vs Cycle Mode

---

## 🚀 ChatGPT Implementation Examples

### **Complete BTC Analysis Request**
```
"Analyze BTC with full technical analysis"

→ Use indicators: rsi, macd, bbands, ema(20), ema(50), sma(200), adx, atr, obv, vwap
→ Multiple timeframes: 1h, 4h, 1d
→ Generate confluence score and trading recommendations
```

### **Meme Token Quick Assessment**
```
"Check PEPE momentum signals"

→ Use indicators: rsi, stoch, willr, cci, bbands(wider), atr
→ Focus on: High volatility patterns, momentum extremes
→ Generate risk-adjusted position sizing
```

### **Breakout Scanner**
```
"Find breakout setups in top 100 coins"

→ Use indicators: bbw, atr, donchian, keltner, volume
→ Look for: Low volatility periods, volume confirmation
→ Generate breakout probability scores
```

---

*This guide enables ChatGPT to use ALL 208+ Taapi.io indicators with intelligent selection based on token type, timeframe, and market conditions. Always use authentic data from Taapi.io API - never fabricate indicator values.*