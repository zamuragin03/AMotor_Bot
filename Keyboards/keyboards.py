from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Service.StorageService import StorageService
from Service.ResponsibleService import ResponsibleService
class Keyboards:
    def remove():
        return ReplyKeyboardRemove()
    def GetAdminKb():
        admin_filter = ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True)
        options = ['Посмотреть все склады', 'Посмотреть всех ответственных']
        admin_filter.row(KeyboardButton('Добавить ответственного'))
        admin_filter.row(KeyboardButton('Добавить склад'))
        admin_filter.row(
            *[KeyboardButton(el)for el in options]
        )
        return admin_filter

    def GetStoragesKb():
        storages_kb = ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True)
        storages_kb.row(KeyboardButton('⬅Начало⬅'))
        
        for option in StorageService.getStorageNames():
            btn = KeyboardButton(text=option)
            storages_kb.row(btn)
        return storages_kb

    def GetResponsiblesKb():
        resp_kb = ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True)
        resp_kb.row(KeyboardButton('⬅Начало⬅'))
        
        for option in ResponsibleService.getResponsibleNames():
            btn = KeyboardButton(text=option)
            resp_kb.row(btn)
        return resp_kb

    def ActionsWithStorageKb():
        actions_kb = ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True)
        options = [
            '⬅Начало⬅',
            'Удалить склад',
            'Изменить название',
            'Изменить адрес',
            'Изменить телефон',
            'Изменить ссылку',
            'Установить ответственного-1',
            'Установить ответственного-2',
            'Установить ответственного-3',
                   ]
        for option in options:
            btn = KeyboardButton(text=option)
            actions_kb.row(btn)
        return actions_kb
    
    def ActionsWithRespobsibleKb():
        actions_kb = ReplyKeyboardMarkup(
            one_time_keyboard=False, resize_keyboard=True)
        actions_kb.row(KeyboardButton('⬅Начало⬅'))
        
        options = [
            'Удалить ответственного',
                   ]
        for option in options:
            btn = KeyboardButton(text=option)
            actions_kb.row(btn)
        return actions_kb
        