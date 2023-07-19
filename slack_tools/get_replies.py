import os
from dotenv import load_dotenv

from slack_sdk.web import WebClient

def get_replies_list(client, CHANNEL_ID: str, ts: str):
    replies = []
    # メッセージに対する全ての返信を取得
    has_more = True
    cursor = ""
    while has_more:
        response = client.conversations_replies(channel="YOUR_CHANNEL_ID", ts=ts, cursor=cursor, limit=10)
        messages = response["messages"]
        replies.extend(messages)
        if response["has_more"]:
            cursor = response["response_metadata"]["next_cursor"]
        else:
            has_more = False
    return replies