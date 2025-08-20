import requests
import json
import time
import aiohttp
import asyncio


def get_tokens_from_file(filepath: str):
    tokens = []
    with open(filepath) as token_file:
        tokens = [token.strip() for token in token_file]
        tokens = list(
            set(tokens)
        )  # anti duplicate er - or just use everything as a set? maybe
    return tokens


async def get_thread_message_count(session, token):
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

    # response = requests.post(url, headers=headers, data=json.dumps(payload))
    async with session.post(url, headers=headers, json=payload) as response:
        return await response.json()


async def send_message(
    session,
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

    # response = requests.post(url, headers=headers, data=json.dumps(payload))
    async with session.post(url, headers=headers, json=payload) as response:
        return await response.json()


async def send_threadgrower_message(session, token):
    return await send_message(
        session, token, channel="C06QV2T1P4G", text="a", thread_ts="1710818631.730789"
    )


tokens = get_tokens_from_file("tokens.txt")
token = tokens[0]


async def main():

    async with aiohttp.ClientSession() as session:
        count = await get_thread_message_count(session, token)
        print(count["messages"][0]["reply_count"])

        while True:

            loop_start = time.time()
            send_json = await send_threadgrower_message(session, token=token)
            send_ok = send_json["ok"]
            print(send_ok)
            # if send_ok == False:
            #     print(send_json)
            #     while True:
            #         None
            print(time.time() - loop_start)


asyncio.run(main())
