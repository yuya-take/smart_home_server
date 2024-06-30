import logging
import os

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv(verbose=True)


class SlackManager:
    def __init__(self):
        self.slack_api_token = os.getenv("SLACK_API_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID", "")
        self.client = WebClient(token=self.slack_api_token)

        self.timestamp = None

    def send_message(self, message):
        try:
            # Call the chat.postMessage method using the WebClient
            result = self.client.chat_postMessage(channel=self.channel_id, text=message)
            logging.debug(result)

        except SlackApiError as e:
            logging.error(f"Error posting message: {e}")

    def get_latest_message(self):
        try:
            response = self.client.conversations_history(channel=self.channel_id, limit=1)
            messages = response["messages"]
            if messages:
                latest_message = messages[0]
                if "bot_id" not in latest_message:
                    if latest_message["ts"] != self.timestamp:
                        self.timestamp = latest_message["ts"]
                        return messages[0]
                else:
                    return None
            return None
        except SlackApiError as e:
            logging.error(f"Error fetching conversation history: {e}")
            return None
