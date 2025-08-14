# Discord Webhook Setup for ChatGPT Alpha Bot

## Your Callouts Channel
Channel ID: `1403926917694099496`

## Steps to Get Webhook URL:

1. **Go to your Discord server**
2. **Right-click on your callouts channel**
3. **Select "Edit Channel"**
4. **Go to "Integrations" tab**
5. **Click "Create Webhook"**
6. **Name it "ChatGPT Alpha Bot"**
7. **Copy the webhook URL**

## Add to Environment:
```bash
export DISCORD_WEBHOOK_CALLOUTS="your_webhook_url_here"
```

Or add to your environment variables in Replit:
- Key: `DISCORD_WEBHOOK_CALLOUTS`
- Value: `https://discord.com/api/webhooks/...`

## Test the Bot:
Once you add the webhook, the bot will immediately send alerts for the 6 signals it already found:
- SUI, FLOKI, GRT, SAND, FLOW, COMP (all 61.5% score)

The bot is running and finding signals - it just needs the webhook to send them to you!