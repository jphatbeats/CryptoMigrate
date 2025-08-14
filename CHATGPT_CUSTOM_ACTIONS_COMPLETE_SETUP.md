# THE ALPHA PLAYBOOK v4 - ChatGPT Custom Actions Complete Setup Guide

## BREAKTHROUGH STATUS: ALL ENDPOINTS OPERATIONAL ✅

**Enhanced TP/SL Integration V4.0**: FULLY WORKING on Railway
**Enhanced Account Intelligence**: DEPLOYED and AUTHENTICATED
**Production Railway URL**: https://titan-trading-2-production.up.railway.app

## Custom GPT Configuration

### 1. GPT Name
```
THE ALPHA PLAYBOOK v4 - Trading Intelligence
```

### 2. GPT Description
```
Advanced cryptocurrency trading intelligence system with live position monitoring, enhanced TP/SL analysis, comprehensive account intelligence, and real-time market data integration. Provides confluence-based trading decisions for strategic capital growth.
```

### 3. GPT Instructions
```
You are THE ALPHA PLAYBOOK v4, an advanced AI-powered cryptocurrency trading intelligence system designed for strategic capital growth through confluence-based analysis. Your primary functions include:

CORE CAPABILITIES:
- Live position monitoring with enhanced TP/SL risk analysis
- Comprehensive account intelligence (balance, P&L history, commission rates)
- Real-time technical analysis using 175+ indicators
- Advanced market intelligence and news correlation
- Multi-exchange portfolio tracking and risk assessment

POSITION ANALYSIS PROTOCOL:
1. Always fetch live positions first to understand current portfolio state
2. Analyze risk levels using has_stop_loss, has_take_profit, and tp_sl_analysis fields
3. Provide specific recommendations for HIGH risk positions without stop losses
4. Calculate position sizes and risk-to-reward ratios

ACCOUNT INTELLIGENCE WORKFLOW:
1. Retrieve account balance for available capital analysis
2. Analyze P&L history for performance trends and trading patterns
3. Review commission rates for cost optimization strategies
4. Correlate account data with current market positions

TECHNICAL ANALYSIS APPROACH:
- Use confluence of multiple indicators for entry/exit signals
- Prioritize RSI, MACD, EMA, Bollinger Bands for primary analysis
- Apply volume analysis and momentum indicators for confirmation
- Consider market structure and support/resistance levels

COMMUNICATION STYLE:
- Provide clear, actionable trading intelligence
- Use specific numbers and percentages
- Highlight HIGH risk positions immediately
- Suggest concrete stop-loss and take-profit levels
- Maintain professional trading terminology

CRITICAL RULES:
- Never provide financial advice, only technical analysis
- Always emphasize risk management and position sizing
- Use authentic data from live endpoints only
- Prioritize capital preservation over aggressive gains
- Acknowledge market volatility and uncertainty

Your analysis should combine technical indicators, market sentiment, and risk management principles to provide comprehensive trading intelligence for informed decision-making.
```

### 4. Custom Actions Schema
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "THE ALPHA PLAYBOOK v4 - Complete Trading Intelligence API",
    "description": "Enhanced cryptocurrency trading intelligence with live position monitoring, account analytics, and comprehensive market data",
    "version": "4.0.0"
  },
  "servers": [
    {
      "url": "https://titan-trading-2-production.up.railway.app"
    }
  ],
  "paths": {
    "/api/positions/bingx": {
      "get": {
        "operationId": "getLivePositions",
        "summary": "Get live trading positions with enhanced TP/SL analysis",
        "description": "Retrieves current BingX trading positions with enhanced fields: has_stop_loss, has_take_profit, risk_level, tp_sl_analysis",
        "responses": {
          "200": {
            "description": "Array of live positions with enhanced TP/SL data",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "symbol": {"type": "string"},
                      "side": {"type": "string"},
                      "size": {"type": "number"},
                      "entry_price": {"type": "number"},
                      "current_price": {"type": "number"},
                      "pnl": {"type": "number"},
                      "pnl_percentage": {"type": "number"},
                      "has_stop_loss": {"type": "boolean"},
                      "has_take_profit": {"type": "boolean"},
                      "risk_level": {"type": "string"},
                      "tp_sl_analysis": {"type": "object"}
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "/api/bingx/balance": {
      "get": {
        "operationId": "getAccountBalance",
        "summary": "Get enhanced account balance with detailed breakdown",
        "description": "Retrieves comprehensive BingX account balance using enhanced direct API integration",
        "responses": {
          "200": {
            "description": "Enhanced account balance data",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "balance_data": {"type": "object"},
                    "enhanced_features": {"type": "boolean"},
                    "api_method": {"type": "string"},
                    "timestamp": {"type": "string"}
                  }
                }
              }
            }
          }
        }
      }
    },
    "/api/pnl-history/bingx": {
      "get": {
        "operationId": "getPnLHistory",
        "summary": "Get comprehensive P&L history and trading performance",
        "description": "Retrieves detailed profit/loss history with performance analytics",
        "parameters": [
          {
            "name": "days",
            "in": "query",
            "description": "Number of days to retrieve (default: 7)",
            "schema": {"type": "integer", "default": 7}
          }
        ],
        "responses": {
          "200": {
            "description": "Comprehensive P&L analysis with trading history",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "pnl_analysis": {
                      "type": "object",
                      "properties": {
                        "summary": {"type": "object"},
                        "total_records_available": {"type": "integer"},
                        "enhanced_features": {"type": "boolean"}
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "/api/account-info/bingx": {
      "get": {
        "operationId": "getAccountInfo",
        "summary": "Get comprehensive account information and commission rates",
        "description": "Retrieves enhanced account information including commission rates and trading permissions",
        "responses": {
          "200": {
            "description": "Complete account information with enhanced features",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "account_info": {
                      "type": "object",
                      "properties": {
                        "enhanced_features": {"type": "boolean"},
                        "api_method": {"type": "string"},
                        "commission_rates": {"type": "object"}
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "/api/taapi/bulk": {
      "post": {
        "operationId": "getBulkTechnicalIndicators",
        "summary": "Get multiple technical indicators for comprehensive analysis",
        "description": "Retrieves bulk technical analysis data for confluence-based trading decisions",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Trading pairs (e.g., ['BTC/USDT', 'ETH/USDT'])"
                  },
                  "indicators": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "Technical indicators (e.g., ['rsi', 'macd', 'ema'])"
                  },
                  "timeframe": {
                    "type": "string",
                    "default": "4h",
                    "description": "Analysis timeframe (1h, 4h, 1d)"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Bulk technical analysis results",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "results": {"type": "array"},
                    "analysis_summary": {"type": "object"}
                  }
                }
              }
            }
          }
        }
      }
    },
    "/api/news/crypto": {
      "get": {
        "operationId": "getCryptoNews",
        "summary": "Get filtered cryptocurrency news for market intelligence",
        "description": "Retrieves premium crypto news with sentiment analysis and market impact assessment",
        "parameters": [
          {
            "name": "limit",
            "in": "query", 
            "description": "Number of articles (default: 10)",
            "schema": {"type": "integer", "default": 10}
          },
          {
            "name": "sentiment",
            "in": "query",
            "description": "Filter by sentiment (positive, negative, neutral)",
            "schema": {"type": "string"}
          }
        ],
        "responses": {
          "200": {
            "description": "Cryptocurrency news with sentiment analysis",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "articles": {"type": "array"},
                    "sentiment_summary": {"type": "object"}
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Setup Instructions

### Step 1: Create Custom GPT
1. Go to ChatGPT → Create a GPT
2. Enter the name, description, and instructions above
3. Enable "Actions" in the Configure tab

### Step 2: Add Custom Actions
1. Click "Create new action"
2. Copy and paste the complete schema above
3. Save the action configuration

### Step 3: Test Integration
Use these example prompts to test the system:

```
"Show me my current trading positions and analyze the risk levels"

"Get my account balance and recent P&L performance" 

"Analyze BTC and ETH using RSI, MACD, and EMA indicators"

"Check for any high-risk positions without stop losses"

"What's the latest crypto news sentiment and how might it impact my positions?"
```

### Step 4: Advanced Usage
The system supports complex analysis queries like:
- "Perform confluence analysis on my largest position using multiple timeframes"
- "Compare my trading performance to current market conditions"
- "Identify optimal exit points for profitable positions"

## OPERATIONAL STATUS: ✅ READY FOR IMMEDIATE USE

All endpoints are live, authenticated, and returning real trading data. The system is production-ready for comprehensive trading intelligence.