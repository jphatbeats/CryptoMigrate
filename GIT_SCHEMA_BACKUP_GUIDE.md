# Git Schema Backup Guide

## Quick Commands to Save Working Schemas

### 1. Add Schema Files
```bash
# Add all working schemas
git add working_schemas/
git add MODULE_USAGE_GUIDE.md
git add GIT_SCHEMA_BACKUP_GUIDE.md

# Add any specific schema files
git add COINMARKETCAP_CHATGPT_SCHEMA_FIXED.json
git add CRYPTONEWS_CHATGPT_SCHEMA_CORRECTED.json
git add LUNARCRUSH_CHATGPT_SCHEMA_FIXED.json
```

### 2. Commit with Clear Message
```bash
git commit -m "✅ Save working ChatGPT schemas and usage guides

- Added MODULE_USAGE_GUIDE.md with comprehensive module instructions
- Created working_schemas/ directory structure
- Backed up tested and verified schemas
- Includes Railway endpoints and direct API schemas
- All schemas validated and working with ChatGPT Custom Actions"
```

### 3. Push to Repository
```bash
git push origin main
```

## Schema Organization

### Current Working Files:
- `COINMARKETCAP_CHATGPT_SCHEMA_FIXED.json` ✅ Working
- `CRYPTONEWS_CHATGPT_SCHEMA_CORRECTED.json` ✅ Working  
- `LUNARCRUSH_CHATGPT_SCHEMA_FIXED.json` ✅ Working
- `cleaned_chatgpt_schema.json` ✅ Working
- `complete_fixed_cryptonews_schema.json` ✅ Working

### Need to Organize:
- Copy working schemas to `working_schemas/` directory
- Rename with descriptive names
- Add version dates
- Document which are Railway vs Direct API

## Quick Backup Script
```bash
#!/bin/bash
# Save all working schemas to git

echo "🔄 Backing up working schemas..."

# Add module guide and schema files
git add MODULE_USAGE_GUIDE.md
git add working_schemas/
git add *_CHATGPT_SCHEMA*.json
git add *chatgpt_schema*.json

# Commit with timestamp
git commit -m "💾 Schema backup $(date +'%Y-%m-%d %H:%M')"

# Push to remote
git push origin main

echo "✅ Schemas backed up to git!"
```

Make this script executable:
```bash
chmod +x backup_schemas.sh
```

Run whenever you update schemas:
```bash
./backup_schemas.sh
```