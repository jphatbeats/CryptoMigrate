#!/bin/bash

# Push Railway Python Configuration Fix
echo "🚀 Pushing Railway Python environment fix to GitHub..."

git add .
git commit -m "Fix Railway Python environment configuration

- Added nixpacks.toml to specify Python 3.10 environment
- Added runtime.txt for explicit Python version
- Added railway.json with proper deployment configuration
- Updated Procfile to use 'python' instead of 'python3'
- Previous OpenAI integration fix included
- Railway deployment should now work properly"

git push origin main

echo "✅ Railway Python fix pushed to GitHub!"
echo "🚂 Railway will automatically redeploy with proper Python environment"
echo "⏱️  Wait 3-5 minutes for Railway deployment to complete"
echo "🧠 ChatGPT endpoints will then work with OpenAI integration"