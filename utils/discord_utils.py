import requests
import os


def send_message_via_webhook(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Discord Webhook message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")


def send_discord_message(message):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url is None:
        print("Webhook URL not found. Please set the 'DISCORD_WEBHOOK_URL' environment variable.")
    else:
        send_message_via_webhook(webhook_url, message)
