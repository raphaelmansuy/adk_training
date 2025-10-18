"""
Slack Bot Development Server (Socket Mode)

This module runs the support bot in Socket Mode, which is ideal for development.
Socket Mode allows your bot to receive events from Slack without needing a
public HTTP webhook.

Usage:
    python -m support_bot.bot_dev

Requirements:
    - .env file in support_bot/ directory with:
      * SLACK_BOT_TOKEN (starts with xoxb-)
      * SLACK_APP_TOKEN (starts with xapp-)
      * GOOGLE_API_KEY (for Gemini API)
"""

import os
import sys
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Validate credentials
if not all([SLACK_BOT_TOKEN, SLACK_APP_TOKEN, GOOGLE_API_KEY]):
    logger.error("❌ Missing required environment variables!")
    logger.error("   Required: SLACK_BOT_TOKEN, SLACK_APP_TOKEN, GOOGLE_API_KEY")
    logger.error("   Check your support_bot/.env file")
    sys.exit(1)

# Initialize Slack app
app = App(token=SLACK_BOT_TOKEN)

# Import the agent
try:
    from support_bot.agent import root_agent
    logger.info("✅ Loaded support_bot agent successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import agent: {e}")
    sys.exit(1)


@app.event("app_mention")
def handle_mention(body, say, logger):
    """
    Handle when the bot is mentioned in a message.

    This function:
    1. Extracts the user's message
    2. Sends it to the ADK agent
    3. Sends the agent's response back to Slack
    """
    try:
        # Get the message text and remove the bot mention
        message_text = body["event"]["text"]
        
        # Remove bot mention (@Support Bot) from the message
        user_message = message_text.split(">", 1)[-1].strip()
        
        logger.info(f"📨 Received message: {user_message}")
        
        # Show typing indicator
        say(f"⏳ Processing your request: `{user_message}`")
        
        # Send to ADK agent (in a real app, you'd use agent.generate() method)
        # For now, we'll show how the agent would be used
        logger.info(f"✓ Agent would process: {user_message}")
        
        # Send response
        response = (
            f"✅ Agent processed your message:\n"
            f"*Message:* {user_message}\n"
            f"*Status:* Ready to integrate with ADK agent\n\n"
            f"_In production, this would call the agent's tools like:_\n"
            f"  • Search knowledge base\n"
            f"  • Create support tickets\n"
            f"  • Get company information"
        )
        
        say(response)
        logger.info("✓ Response sent to Slack")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        say(f"❌ Error: {str(e)}")


@app.event("message")
def handle_message(body, say, logger):
    """Handle direct messages to the bot."""
    try:
        if "text" in body["event"]:
            message_text = body["event"]["text"]
            logger.info(f"💬 Direct message: {message_text}")
            
            # Send response
            response = (
                f"✅ Received your message:\n"
                f"*Message:* {message_text}\n\n"
                f"💡 Try mentioning me with `@Support Bot` in a channel for full features!"
            )
            say(response)
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)


def main():
    """Start the Socket Mode handler."""
    logger.info("🚀 Starting Support Bot in Socket Mode...")
    logger.info("📡 Connecting to Slack using Socket Mode...")
    
    # Create Socket Mode handler
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    
    try:
        logger.info("✅ Bot is running! Listening for mentions...")
        logger.info("📝 Try mentioning the bot in Slack: @Support Bot help")
        logger.info("⏹️  Press Ctrl+C to stop the bot")
        
        handler.start()
    except KeyboardInterrupt:
        logger.info("⏹️  Shutting down bot...")
        handler.close()
        logger.info("✅ Bot stopped")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
