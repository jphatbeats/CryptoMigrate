// TAAPI.io NPM Client Test
// Testing modern ES6 class-based API
const Taapi = require("taapi").default;

console.log("🚀 Starting TAAPI.io Client Test...");
console.log("📊 Testing modern class-based client");

try {
    // Initialize client with proper ES6 syntax
    const client = new Taapi("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjg5NDFjMGE4MDZmZjE2NTFlMmM1ZTM0IiwiaWF0IjoxNzU0NTM3NDUxLCJleHAiOjMzMjU5MDAxNDUxfQ.QRqOzRFsTcYKSYUuezVQMFdJcL2A6lHIwWC5L0JOLTU");
    
    console.log("✅ Client initialized successfully");
    console.log("🔧 Client methods:", Object.getOwnPropertyNames(Object.getPrototypeOf(client)));
    
    // Test if we can access indicators
    console.log("🔄 Testing simple RSI call...");
    
    // Try different method signatures
    if (typeof client.getIndicator === 'function') {
        client.getIndicator("rsi", "binance", "BTC/USDT", "1h")
            .then(result => {
                console.log("✅ RSI Success:", result);
            })
            .catch(error => {
                console.log("⚠️ getIndicator failed:", error.message);
            });
    } else {
        console.log("⚠️ getIndicator method not found");
        console.log("🔧 Available methods:", Object.getOwnPropertyNames(client));
    }
    
} catch (error) {
    console.log("❌ Client initialization failed:", error.message);
    console.log("📋 Switching to basic HTTP server approach...");
    
    // Fallback: Create basic HTTP server for TAAPI calls
    const http = require('http');
    const url = require('url');
    
    const server = http.createServer((req, res) => {
        const queryObject = url.parse(req.url, true).query;
        
        res.writeHead(200, {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        
        res.end(JSON.stringify({
            message: "TAAPI NPM client not compatible - use direct REST API",
            endpoint: "https://api.taapi.io/" + (queryObject.indicator || "rsi"),
            suggestion: "Use individual indicators schema for ChatGPT"
        }));
    });
    
    server.listen(4101, () => {
        console.log("🔧 Fallback server running on port 4101");
        console.log("💡 Recommendation: Use individual indicators schema");
    });
}