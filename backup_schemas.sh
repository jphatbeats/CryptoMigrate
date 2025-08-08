#!/bin/bash
# Save all working schemas to git

echo "🔄 Backing up working schemas..."

# Add module guide and schema files
git add MODULE_USAGE_GUIDE.md
git add GIT_SCHEMA_BACKUP_GUIDE.md
git add working_schemas/
git add *_CHATGPT_SCHEMA*.json
git add *chatgpt_schema*.json

# Commit with timestamp
git commit -m "💾 Schema backup $(date +'%Y-%m-%d %H:%M')"

# Push to remote
git push origin main

echo "✅ Schemas backed up to git!"