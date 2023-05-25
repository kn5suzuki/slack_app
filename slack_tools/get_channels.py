import os
from dotenv import load_dotenv

from slack_sdk.web import WebClient


def get_public_channels(client):
    return client.conversations_list(
        limit=1000, types='public_channel')['channels']


def get_private_channels(client):
    return client.conversations_list(
        limit=1000, types='private_channel')['channels']


def get_all_channels(client):
    return get_private_channels(client)+get_public_channels(client)


def create_channel_list(CHANNELS_LIST: list):
    channel_list = []
    for channel in CHANNELS_LIST:
        channel_dict = {
            'name': channel['name'],
            'id': channel['id']
        }
        channel_list.append(channel_dict)
    return channel_list


def create_channel_dict(CHANNELS_LIST: list):
    channel_dict = {}
    for channel in CHANNELS_LIST:
        channel_dict[channel['name']] = channel['id']
    return channel_dict


if __name__ == "__main__":
    load_dotenv()
    SLACK_API_TOKEN = os.getenv('UserOAuthToken')
    client = WebClient(token=SLACK_API_TOKEN)

    PRIVATE_LIST = get_all_channels(client)
    print(create_channel_list(PRIVATE_LIST))
