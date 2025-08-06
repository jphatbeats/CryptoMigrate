#!/bin/bash

# Push the fixed ChatGPT schema to Railway
# This will make ChatGPT use working endpoints only

echo "=== Pushing Fixed ChatGPT Schema to Railway ==="

# Stage the fixed schema file
git add no_auth_schema.json

# Commit the fix
git commit -m "Fix ChatGPT endpoints - remove broken individual exchange endpoints

- Removed getBingXPositions (returns HTML error)
- Removed getKrakenBalance (returns HTML error) 
- Removed getBlofinPositions (returns HTML error)
- ChatGPT will now use working getAllExchangeData endpoint
- Railway deployment confirmed working with complete position data"

# Push to Railway (triggers auto-deploy)
git push origin main

echo "=== Schema fix pushed to Railway ==="
echo "Wait 2-3 minutes for Railway to deploy"
echo "Then test ChatGPT integration"