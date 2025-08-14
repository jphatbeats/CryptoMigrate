// TAAPI.io Bulk Client - Complete Implementation
// Provides bulk access to all 208+ technical indicators
const Taapi = require("taapi").default;
const http = require('http');
const url = require('url');

console.log("🚀 TAAPI.io Bulk Client Starting...");
console.log("📊 Initializing with full indicator support");

// Initialize client with API key
const client = new Taapi("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjg5NDFjMGE4MDZmZjE2NTFlMmM1ZTM0IiwiaWF0IjoxNzU0NTM3NDUxLCJleHAiOjMzMjU5MDAxNDUxfQ.QRqOzRFsTcYKSYUuezVQMFdJcL2A6lHIwWC5L0JOLTU");

console.log("✅ Client initialized");
console.log("🔧 Available methods:", Object.getOwnPropertyNames(Object.getPrototypeOf(client)));

// Test single indicator with correct parameter format
async function testIndicators() {
    try {
        console.log("🔄 Testing RSI with correct parameters...");
        
        // Correct parameter format for TAAPI client
        const rsiResult = await client.getIndicator("rsi", {
            exchange: "binance",
            symbol: "BTC/USDT",
            interval: "1h",
            period: 14
        });
        
        console.log("✅ RSI Test Success:", rsiResult);
        
        // Test MACD
        const macdResult = await client.getIndicator("macd", {
            exchange: "binance", 
            symbol: "BTC/USDT",
            interval: "1h",
            fast: 12,
            slow: 26,
            signal: 9
        });
        
        console.log("✅ MACD Test Success:", macdResult);
        
        // Test Bulk Queries
        console.log("🔄 Testing bulk queries...");
        
        client.resetBulkConstructs();
        
        // Add multiple calculations
        client.addCalculation("rsi", {
            exchange: "binance",
            symbol: "BTC/USDT", 
            interval: "1h",
            period: 14
        });
        
        client.addCalculation("macd", {
            exchange: "binance",
            symbol: "BTC/USDT",
            interval: "1h",
            fast: 12,
            slow: 26,
            signal: 9
        });
        
        client.addCalculation("ema", {
            exchange: "binance",
            symbol: "BTC/USDT",
            interval: "1h",
            period: 20
        });
        
        const bulkResults = await client.executeBulk();
        console.log("✅ Bulk Results:", JSON.stringify(bulkResults, null, 2));
        
        startHTTPServer();
        
    } catch (error) {
        console.log("❌ Error:", error.message);
        console.log("🔧 Starting fallback HTTP server...");
        startFallbackServer();
    }
}

// HTTP Server for ChatGPT integration
function startHTTPServer() {
    const server = http.createServer(async (req, res) => {
        // Enable CORS
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        
        if (req.method === 'OPTIONS') {
            res.writeHead(200);
            res.end();
            return;
        }
        
        try {
            const parsedUrl = url.parse(req.url, true);
            const query = parsedUrl.query;
            const path = parsedUrl.pathname;
            
            if (path === '/indicator' && query.indicator) {
                // Single indicator endpoint
                const result = await client.getIndicator(query.indicator, {
                    exchange: query.exchange || "binance",
                    symbol: query.symbol || "BTC/USDT", 
                    interval: query.interval || "1h",
                    period: parseInt(query.period) || 14,
                    fast: parseInt(query.fast) || 12,
                    slow: parseInt(query.slow) || 26,
                    signal: parseInt(query.signal) || 9,
                    stddev: parseFloat(query.stddev) || 2,
                    backtrack: parseInt(query.backtrack) || 0
                });
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(result));
                
            } else if (path === '/bulk' && req.method === 'POST') {
                // Bulk endpoint 
                let body = '';
                req.on('data', chunk => body += chunk);
                req.on('end', async () => {
                    try {
                        const bulkRequest = JSON.parse(body);
                        
                        client.resetBulkConstructs();
                        
                        for (const calc of bulkRequest.calculations) {
                            client.addCalculation(calc.indicator, calc.params);
                        }
                        
                        const results = await client.executeBulk();
                        
                        res.writeHead(200, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify(results));
                    } catch (error) {
                        res.writeHead(400, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ error: error.message }));
                    }
                });
                
            } else {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ 
                    error: "Not found",
                    endpoints: [
                        "GET /indicator?indicator=rsi&symbol=BTC/USDT&exchange=binance&interval=1h",
                        "POST /bulk (with JSON body)"
                    ]
                }));
            }
            
        } catch (error) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: error.message }));
        }
    });
    
    server.listen(4101, () => {
        console.log("🌐 TAAPI Bulk Server running on http://localhost:4101");
        console.log("📋 Endpoints:");
        console.log("   GET /indicator - Single indicator queries");
        console.log("   POST /bulk - Bulk indicator queries");
        console.log("✅ Ready for ChatGPT integration!");
    });
}

function startFallbackServer() {
    const server = http.createServer((req, res) => {
        res.writeHead(200, {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        
        res.end(JSON.stringify({
            status: "fallback",
            message: "TAAPI NPM client failed - use direct REST API",
            recommendation: "Use taapi_basic_plan_optimized_schema.yaml for ChatGPT",
            working_endpoints: [
                "https://api.taapi.io/rsi?secret=YOUR_KEY&symbol=BTC/USDT&exchange=binance&interval=1h"
            ]
        }));
    });
    
    server.listen(4101, () => {
        console.log("🔧 Fallback server running on port 4101");
    });
}

// Start the test
testIndicators();