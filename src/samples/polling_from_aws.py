import boto3
import requests
import time
import json

sqs_client = boto3.client('sqs', region_name='ap-northeast-1')
queue_url = "https://sqs.ap-northeast-1.amazonaws.com/211125774107/test"
slack_token = "xoxb-7063594105058-7070683272882-WULTAGbxOmStkYjfF7Hrzqz7"  # Slack OAuthトークンを設定
channel_id = "C0722HPKZHA"  # メッセージを送信するSlackチャネルID

def clear_queue(client, queue_url):
    while True:
        resp = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )

        if 'Messages' not in resp:
            break

        for message in resp['Messages']:
            receipt_handle = message['ReceiptHandle']
            delete_message(client, queue_url, receipt_handle)

    print("Queue cleared.")

def delete_message(client, queue_url, receipt_handle):
    try:
        client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted.")
    except Exception as e:
        print(f"Error deleting message: {e}")

def send_message_to_slack(token, channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": message
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200 or not response.json().get("ok"):
        print(f"Failed to send message to Slack: {response.text}")
    else:
        print(f"Message sent to Slack: {message}")

clear_queue(sqs_client, queue_url)

while True:
    resp = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20
    )

    if 'Messages' in resp:
        for message in resp['Messages']:
            body = message['Body']
            print(f"Received message: {body}")
            send_message_to_slack(slack_token, channel_id, body)
            receipt_handle = message['ReceiptHandle']
            delete_message(sqs_client, queue_url, receipt_handle)
    else:
        print("No messages to display.")

    time.sleep(5)
