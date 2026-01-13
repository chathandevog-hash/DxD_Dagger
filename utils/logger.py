from config import LOG_CHANNEL

async def log(client, text: str):
    try:
        if LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, text)
    except:
        pass
