#!/bin/bash

# URGENT Railway Deployment Fix Commands
# Run these commands manually to fix the Railway timeout issue

echo "=== STEP 1: Clean requirements.txt (remove duplicates) ==="
cat > requirements.txt << 'EOF'
Flask==2.3.3
Flask-CORS==4.0.0
ccxt==4.4.98
requests==2.31.0
aiohttp==3.12.15
pandas==2.0.3
numpy==1.24.3
schedule==1.2.0
pytz==2023.3
discord.py==2.3.2
python-dotenv==1.0.0
openai==1.3.8
trafilatura==1.6.3
EOF

echo "=== STEP 2: Update Railway config for better startup ==="
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "python main_server.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 120,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
EOF

echo "=== STEP 3: Add staging and commit changes ==="
git add requirements.txt railway.json no_auth_schema.json CHATGPT_ENDPOINTS_FIX.md RAILWAY_FIX_URGENT.md

echo "=== STEP 4: Commit with descriptive message ==="
git commit -m "URGENT: Fix Railway deployment timeout

- Clean requirements.txt (remove duplicates causing build failures)
- Update railway.json health check configuration
- Remove broken endpoints from ChatGPT schema
- Fix API timeout issues preventing ChatGPT integration

Fixes:
- Railway deployment hanging/timing out
- ChatGPT endpoints returning empty responses
- Duplicate dependencies causing build conflicts"

echo "=== STEP 5: Push to Railway (triggers auto-deploy) ==="
git push origin main

echo "=== STEP 6: Monitor Railway deployment ==="
echo "Watch Railway logs at: https://railway.app/project/titan-trading-2"
echo "Test endpoint after deploy: curl https://titan-trading-2-production.up.railway.app/health"

echo "=== DEPLOYMENT FIX COMMANDS READY ==="
echo "Run these commands in sequence to fix Railway deployment"