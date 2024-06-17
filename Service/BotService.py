import requests
import io
from aiogram import types
import re
class BotService:
    def CreateMediaGroup(photos, text):
        media_group=[]
        for id, photo in enumerate(photos):
            photo_file = requests.get(photo).content
            if id == len(photos)-1:
                media_group.append(types.InputMediaPhoto(media=io.BytesIO(photo_file),caption=text))
            else:
                media_group.append(types.InputMediaPhoto(media=io.BytesIO(photo_file)))
        return media_group
    def SearchFromAnotherBotMessage(message:str):
        pattern = r'OEM:\s*(.*?)\s*Запрос:'
        match = re.search(pattern, message, re.DOTALL)
        if match:
            result = match.group(1)
            return result
     