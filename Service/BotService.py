import requests
import io
from aiogram import types, Bot
import re
from typing import Dict, List
class BotService:
    def CreateMediaGroup(photos, text):
        media_group=[]
        for id, photo in enumerate(photos):
            photo_file = requests.get(photo).content
            if id == len(photos)-1:
                media_group.append(types.InputMediaPhoto(media=io.BytesIO(photo_file),caption=text[:1024]))
            else:
                media_group.append(types.InputMediaPhoto(media=io.BytesIO(photo_file)))
        return media_group
    def SearchFromAnotherBotMessage(message:str):
        pattern = r'OEM:\s*(.*?)\s*Запрос:'
        match = re.search(pattern, message, re.DOTALL)
        if match:
            result = match.group(1)
            return result
     
    async def SendMessageWithMediaGroup(bot:Bot,message:types.Message,res: Dict[List[str], List[str]]):
        full_caption = res.get('text')+ f'\nЗапрос: {message.from_user.first_name if message.from_user.first_name else "" } {message.from_user.last_name if message.from_user.last_name else ""} @{message.from_user.username if message.from_user.username else ""}'
        photos = BotService.CreateMediaGroup(res.get('photos'), full_caption )
        await bot.send_media_group(
        message.chat.id,
        message_thread_id=message.message_thread_id if message.message_thread_id else None,
        media=photos,)
        if len(full_caption)>=1024:
            await bot.send_message(
                message.chat.id,
                message_thread_id=message.message_thread_id if message.message_thread_id else None,
                text=full_caption[1024:]
            )   