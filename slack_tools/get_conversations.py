import os
from dotenv import load_dotenv

from slack_sdk.web import WebClient


def get_conversations_list(client, CHANNEL_ID: str):
    return client.conversations_history(
        channel=CHANNEL_ID, limit=100)['messages']


if __name__ == "__main__":
    load_dotenv()
    SLACK_API_TOKEN = os.getenv('UserOAuthToken')
    CHANNEL_ID = os.getenv('ChannelID')
    client = WebClient(token=SLACK_API_TOKEN)

    print(get_conversations_list(client, CHANNEL_ID)[0])
