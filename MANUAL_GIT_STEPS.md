# Manual Git Steps - Run These in Shell Tab

## The git locks are preventing automatic execution. You need to run these manually:

### Step 1: Clear Git Locks (Run in Shell)
```bash
rm -f .git/index.lock .git/HEAD.lock .git/config.lock
```

### Step 2: Connect to GitHub (Run in Shell) 
```bash
git remote add origin https://github.com/jphatbeats/titan-trading-2.git
```

### Step 3: Add Discord Changes (Run in Shell)
```bash
git add automated_trading_alerts.py requirements.txt replit.md
```

### Step 4: Commit Changes (Run in Shell)
```bash
git commit -m "Discord bot integration: TITAN BOT#6444 working with AI alerts"
```

### Step 5: Push to GitHub (Run in Shell)
```bash
git push -u origin main
```

## Alternative: Use Replit's Git UI
1. Click the Git icon in left sidebar
2. Stage the files: automated_trading_alerts.py, requirements.txt, replit.md
3. Add commit message: "Discord bot integration: TITAN BOT working with AI alerts"  
4. Commit and Push

## What This Accomplishes:
- Connects this Replit to your actual GitHub repository
- Pushes Discord bot integration changes to GitHub
- Triggers Railway to auto-deploy the new code
- Updates your GitHub (no more "2 hours ago")
- Enables Railway deployment with DISCORD_TOKEN