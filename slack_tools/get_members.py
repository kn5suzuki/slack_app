import os
from dotenv import load_dotenv

from slack_sdk.web import WebClient


def get_all_members(client):
    return client.users_list()['members']


def get_channel_members(client, channel_id):
    return client.conversations_members(channel=channel_id)["members"]


def create_members_dict(member_list):
    members_dict = {}
    for member in member_list:
        members_dict[member["id"]] = member["profile"]['display_name']
    return members_dict


if __name__ == "__main__":
    load_dotenv()
    SLACK_API_TOKEN = os.getenv('UserOAuthToken')
    client = WebClient(token=SLACK_API_TOKEN)

    MEMBER_LIST = get_all_members(client)
    # print(create_members_dict(MEMBER_LIST))
