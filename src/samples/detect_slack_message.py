import logging
import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(verbose=True)

# Initialize Slack client
client = WebClient(token=os.getenv("SLACK_API_TOKEN"))
logger = logging.getLogger(__name__)

# ID of the channel you want to monitor
channel_id = os.getenv("SLACK_CHANNEL_ID")

if channel_id is None:
    logger.error("SLACK_CHANNEL_ID environment variable not set.")
    exit(1)

def get_latest_message(channel_id):
    try:
        response = client.conversations_history(channel=channel_id, limit=1)
        messages = response['messages']
        if messages:
            return messages[0]
        return None
    except SlackApiError as e:
        logger.error(f"Error fetching conversation history: {e}")
        return None

def monitor_channel(channel_id, interval=5):
    last_timestamp = None
    while True:
        latest_message = get_latest_message(channel_id)
        if latest_message:
            timestamp = latest_message['ts']
            if timestamp != last_timestamp:
                user = latest_message.get('user', 'Unknown')
                text = latest_message.get('text', '')
                logger.info(f"New message from {user}: {text}")
                last_timestamp = timestamp
        time.sleep(interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monitor_channel(channel_id)
