import os
from dotenv import load_dotenv
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError


def send_message_to_channel(client, channel_id, message, mention_list=[], channel_mention=False):
    if channel_mention:
        message = '<!channel>\n' + message
    elif mention_list:
        mention_text = ''
        for member in mention_list:
            mention_text += f'<@{member}> '
        message = mention_text+'\n'+message
    try:
        client.chat_postMessage(channel=channel_id, text=message)
        return "メッセージを送信しました"
    except SlackApiError as e:
        return "エラー: {}".format(e)


def send_response(client, channel_id, message_ts, message, mention_list=[]):
    if mention_list:
        mention_text = ''
        for member in mention_list:
            mention_text += f'<@{member}> '
        message = mention_text+'\n'+message
    try:
        result = client.chat_postMessage(
            channel=channel_id, thread_ts=message_ts, text=message)
        return "メッセージを送信しました"
    except SlackApiError as e:
        return "エラー: {}".format(e)


# def send_response()


if __name__ == "__main__":
    load_dotenv()
    SLACK_API_TOKEN = os.getenv('BotUserOAuthToken')
    CHANNEL_ID = os.getenv('ChannelID')
    client = WebClient(token=SLACK_API_TOKEN)

    result = send_message_to_channel(
        client, CHANNEL_ID, "テストです", channel_mention=True)
    print(result)
