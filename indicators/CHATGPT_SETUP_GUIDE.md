# ChatGPT Custom Actions Setup Guide

## 🚀 Complete Setup Instructions

### Step 1: Railway Deployment Configuration

**Your Railway Project**: https://indicators-production.up.railway.app  
**GitHub Repository**: https://github.com/jphatbeats/indicators

#### Required Environment Variables on Railway:
1. **TAAPI_API_KEY** ← **CRITICAL: Add this to Railway Variables**
   - Go to Railway Dashboard → Your Project → Variables
   - Add: `TAAPI_API_KEY = your_actual_taapi_key`
   - Without this, you'll only get test data

2. **PORT** (Railway sets automatically)
3. **Optional**: `INDICATORS_PORT = 5001` (if using separate indicators server)

### Step 2: ChatGPT Custom Actions Import

Copy this complete OpenAPI schema for ChatGPT Custom Actions:

```yaml
openapi: 3.1.0
info:
  title: Railway TAAPI Universal Indicators API
  description: |
    Complete access to all 252+ TAAPI.io technical indicators via Railway server.
    ChatGPT dynamically chooses indicators based on analysis requirements.
    
    KEY FEATURES:
    - 252 authentic technical indicators from TAAPI.io
    - Dynamic indicator selection for optimal analysis
    - Zero data hallucination - all calculations from real exchange data
    - Multi-timeframe and multi-exchange support
    
    INDICATOR CATEGORIES:
    • Momentum: RSI, MACD, Stochastic, ADX, CCI, MFI, Williams %R
    • Volume: OBV, A/D Line, Chaikin, VWAP, Volume Profile
    • Trend: EMA, SMA, SuperTrend, Ichimoku, ALMA, HMA
    • Volatility: Bollinger Bands, ATR, Keltner Channels
    • Pattern Recognition: 39 candlestick patterns
    • Cycle Analysis: Hilbert Transform, MESA indicators
    • Statistics: Linear Regression, Correlation, Beta
    • Oscillators: Awesome Oscillator, Elder Ray
    • Bands/Channels: Price channels, regression bands
    • Support/Resistance: Pivot points, key levels
    
    WORKFLOW:
    1. ChatGPT selects appropriate indicators for analysis type
    2. Calls Railway endpoints for real-time calculations
    3. Combines results for confluence analysis
    4. Generates trading insights based on indicator agreement
    
  version: 1.0.0
  contact:
    name: THE ALPHA PLAYBOOK v4 - Railway TAAPI Integration
    url: https://indicators-production.up.railway.app

servers:
  - url: https://indicators-production.up.railway.app
    description: Railway TAAPI Indicators Production Server

security:
  - {}

paths:
  /api/taapi/available:
    get:
      operationId: getAvailableIndicators
      summary: Get All 252 Available TAAPI Indicators
      description: |
        Returns complete categorized list of all available indicators.
        Use this first to see what indicators are available for analysis.
      responses:
        '200':
          description: Complete list of 252 indicators by category
          content:
            application/json:
              schema:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  total_indicators:
                    type: integer
                    description: Total number of indicators (252+)
                  categories:
                    type: object
                    description: All indicator categories with lists
                  usage:
                    type: string
                    description: How to use individual indicators

  /api/taapi/{indicator}:
    get:
      operationId: getSpecificIndicator
      summary: Get Any TAAPI Indicator
      description: |
        Universal endpoint for any of the 252+ TAAPI indicators. ChatGPT dynamically chooses indicators based on analysis needs.
        Popular: rsi, macd, bbands, ema, sma, stoch, adx, obv, atr, cci, vwap, supertrend.
        Patterns: cdldoji, cdlhammer, cdlengulfing. Advanced: ichimoku, fibonacci.
      x-openai-isConsequential: false
        
      parameters:
        - name: indicator
          in: path
          required: true
          description: Any indicator name from the 252 available
          schema:
            type: string
            example: rsi
        - name: symbol
          in: query
          required: false
          description: Trading pair (default BTC/USDT)
          schema:
            type: string
            default: BTC/USDT
            example: ETH/USDT
        - name: interval
          in: query
          required: false
          description: Timeframe (1m, 5m, 15m, 1h, 4h, 1d, etc.)
          schema:
            type: string
            default: 1h
            example: 4h
        - name: period
          in: query
          required: false
          description: Indicator period (default varies by indicator)
          schema:
            type: integer
            example: 14
        - name: fast
          in: query
          required: false
          description: Fast period for indicators like MACD
          schema:
            type: integer
            example: 12
        - name: slow
          in: query
          required: false
          description: Slow period for indicators like MACD
          schema:
            type: integer
            example: 26
        - name: signal
          in: query
          required: false
          description: Signal period for indicators like MACD
          schema:
            type: integer
            example: 9
        - name: stddev
          in: query
          required: false
          description: Standard deviation for Bollinger Bands
          schema:
            type: number
            example: 2.0
      responses:
        '200':
          description: Indicator calculation result
          content:
            application/json:
              schema:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  symbol:
                    type: string
                  indicator:
                    type: string
                  interval:
                    type: string
                  data:
                    type: object
                    description: Indicator calculation results
                  source:
                    type: string
                    description: Always "taapi.io" for authentic data

  /api/taapi/confluence:
    get:
      operationId: getConfluenceAnalysis
      summary: Comprehensive Multi-Indicator Analysis
      description: |
        Gets multiple key indicators for confluence analysis:
        RSI, MACD, Bollinger Bands, EMA, SMA, ATR, ADX, Stochastic, 
        OBV, CCI, Williams %R, MFI, Aroon
        
        Perfect for comprehensive trading analysis.
      x-openai-isConsequential: false
      parameters:
        - name: symbol
          in: query
          required: false
          schema:
            type: string
            default: BTC/USDT
        - name: interval
          in: query
          required: false
          schema:
            type: string
            default: 1h
      responses:
        '200':
          description: Multiple indicators for confluence analysis
          content:
            application/json:
              schema:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  symbol:
                    type: string
                  interval:
                    type: string
                  indicators:
                    type: array
                    description: Array of indicator results
                  confluence_score:
                    type: number
                    description: Agreement score between indicators

  /api/taapi/multiple:
    post:
      operationId: getMultipleIndicators
      summary: Get Custom Set of Indicators
      description: |
        Request specific combination of indicators chosen by ChatGPT.
        Useful when you need a custom set for specific analysis.
      x-openai-isConsequential: false
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                symbol:
                  type: string
                  default: BTC/USDT
                interval:
                  type: string
                  default: 1h
                indicators:
                  type: array
                  items:
                    type: string
                  description: List of indicator names to calculate
                  example: ["rsi", "macd", "bbands", "ema"]
      responses:
        '200':
          description: Results for requested indicators
          content:
            application/json:
              schema:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  symbol:
                    type: string
                  interval:
                    type: string
                  results:
                    type: array
                    description: Array of indicator calculation results
```

### Step 3: ChatGPT Integration Steps

1. **Open ChatGPT (Plus/Pro account required)**
2. **Go to Custom GPTs → Create**
3. **In the Actions tab, paste the complete schema above**
4. **Set the server URL to**: `https://indicators-production.up.railway.app`
5. **Authentication**: None (public endpoints)
6. **Test the integration** with a simple call

### Step 4: Testing Your Setup

Once configured, test with these ChatGPT prompts:

```
"What indicators are available for technical analysis?"
"Get RSI for BTC/USDT on 1 hour timeframe"
"Perform confluence analysis on ETH/USDT"
"Show me Bollinger Bands for SOL/USDT on 4 hour chart"
```

## 🔑 CRITICAL: TAAPI API Key Setup

**YOU MUST ADD YOUR TAAPI API KEY TO RAILWAY:**

1. **Railway Dashboard** → **Your Project** → **Variables**
2. **Add Variable**: 
   - **Name**: `TAAPI_API_KEY`
   - **Value**: `your_actual_taapi_key_here`
3. **Deploy** the changes

**Without the API key, you'll only get test data. With it, you get authentic real-time calculations.**

## 🎯 Success Checklist

- ✅ Railway deployment active at indicators-production.up.railway.app
- ✅ TAAPI_API_KEY added to Railway environment variables
- ✅ ChatGPT Custom Actions configured with the schema above
- ✅ Test calls returning real indicator data
- ✅ All 252 indicators accessible via dynamic selection

Once complete, ChatGPT will have access to the most comprehensive technical analysis system available, with zero data hallucination and maximum analytical flexibility.