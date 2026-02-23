from fastapi import HTTPException


def extract_chat_id(link: str):
    marker = "t.me/"
    if marker not in link:
        raise HTTPException(400, "Invalid Telegram link")
    return {"chatId": link.split(marker)[1].split("/")[0]}
