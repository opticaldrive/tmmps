import requests
import json
import time


def get_tokens_from_file(filepath: str):
    tokens = []
    with open(filepath) as token_file:
        tokens = [token.strip() for token in token_file]
        tokens = list(
            set(tokens)
        )  # anti duplicate er - or just use everything as a set? maybe
    return tokens


def get_thread_message_count(token):
    """GET https://slack.com/api/conversations.history
    Authorization: Bearer xoxb-your-token
    {
    "channel": "YOUR_CONVERSATION_ID",
    "latest": "YOUR_TS_VALUE",
    "limit": 1,
    "inclusive": true
    }
    """

    url = "https://slack.com/api/conversations.history"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Create the payload for the request
    payload = {
        "channel": "C06QV2T1P4G",
        "latest": "1710818631.730789",
        "limit": 1,
        "inclusive": "true",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response


def send_message(
    token: str,
    channel: str,
    text: str,
    thread_ts=None,
):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Create the payload for the request
    payload = {
        "channel": channel,
        "text": text,
    }

    if thread_ts is not None:
        payload["thread_ts"] = thread_ts

    response = requests.post(url, headers=headers, data=json.dumps(payload))


def send_threadgrower_message(token):
    send_message(token, channel="C06QV2T1P4G", text="a", thread_ts="1710818631.730789")


tokens = get_tokens_from_file("tokens.txt")
token = tokens[0]

# count_response = get_thread_message_count(token)
# count = count_response.json()
# print(count)
# print(count["messages"][0]["reply_count"])

# while True:
#     loop_start = time.time()
#     send_threadgrower_message(token=token)
#     print(time.time() - loop_start)
