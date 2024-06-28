import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv(verbose=True)
# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.getenv("SLACK_API_TOKEN"))
logger = logging.getLogger(__name__)

# ID of the channel you want to send the message to
channel_id = os.getenv("SLACK_CHANNEL_ID", "")

try:
    # Call the chat.postMessage method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id, 
        text="Hello world"
    )
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")
