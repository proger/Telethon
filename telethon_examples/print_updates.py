#!/usr/bin/env python3
# A simple script to print all updates received.
# Import modules to access environment, sleep, write to stderr
import asyncio
import os
import sys
import time

# Import the client
from telethon import TelegramClient

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)

# This is a helper method to access environment variables or
# prompt the user to type them in the terminal if missing.
def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


# Define some variables so the code reads easier
session = os.environ.get('TG_SESSION', 'printer')
api_id = get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = get_env('TG_API_HASH', 'Enter your API hash: ')


from telethon.events.raw import Raw

async def main():
    client = TelegramClient(session, api_id, api_hash)

    async def handler(update: Raw):
        print(update)

    client.add_event_handler(handler)

    await client.start()
    await client.send_message('me', 'Hello to myself!')

    async for message in client.iter_messages('torontotv', reverse=False):
        print(message.reactions)


if __name__ == '__main__':
    asyncio.run(main())