
from aiogram.types import *
from aiogram import Bot, types, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import *
from Config import BOT_TOKEN, scheduler
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from Service import StorageService, SearchService, BotService, bazonService, dismaService, ResponsibleService, BotAdmin
from Keyboards import Keyboards
from States import FSMAdmin
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

def schedule():
    scheduler.add_job(main_func, 'interval', hours=1, args=(dp,))
    

async def main_func(dp: Dispatcher):
    bazonService.UpdatedDB()
    dismaService.UpdatedDB()
    
@dp.message_handler(commands=["test"], state="*")
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        await bot.send_message(
        message.chat.id,
        text=str(data),
    )

    
@dp.message_handler(filters.Text(contains='Начало'),state='*')
@dp.message_handler(commands=["admin"], state="*")
async def handle_message(message: types.Message, state:FSMContext):
    if message.from_user.id not in [6504953119,225529144]:
        return 
    if message.message_thread_id in [20108,20106]:
        return 
    await BotAdmin.ReturnToAdminMenu(bot, message)

    


# 20108 -- для переписки с ботом
# 20106 -- для ручных запросов
@dp.message_handler()
async def handle_message(message: types.Message, state:FSMContext):
    if message.message_thread_id ==20108:
        findBy=BotService.SearchFromAnotherBotMessage(message.text)
        res = SearchService.FindDetail(findBy)
        photos = BotService.CreateMediaGroup(res.get('photos'), res.get('text') + f'\nЗапрос: {message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}')
        if len(photos)>0:
            await bot.send_message(
        message.chat.id,
        message_thread_id=20108,
        text='Данная деталь уже есть в базе',
    )
    elif message.message_thread_id==20106:
        res = SearchService.FindDetail(message.text)
        await BotService.SendMessageWithMediaGroup(bot, message,res)
    elif message.chat.type=='private':
        res = SearchService.FindDetail(message.text)
        await BotService.SendMessageWithMediaGroup(bot, message,res)

    


@dp.message_handler(filters.Text(contains='Выйти'), state=FSMAdmin.choosing_action)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Вы вышли из админ меню',
            reply_markup=Keyboards.remove()
        )
    await state.reset_data()
    await state.reset_state()

@dp.message_handler(filters.Text(equals='Добавить ответственного'), state=FSMAdmin.choosing_action)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Добавляем отвтетственного\nУкажите его имя',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_responsible_name.set()
    

@dp.message_handler(filters.Text(equals='Добавить склад'), state=FSMAdmin.choosing_action)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Добавляем склад\nУкажите название склада',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_storage_name.set()
    
@dp.message_handler(state=FSMAdmin.typing_storage_name)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['storage_name']=message.text
    await bot.send_message(
            message.from_user.id,
            f'Отправьте ссылку на выгрузку',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_storage_dump_url.set()
    
@dp.message_handler(state=FSMAdmin.typing_storage_dump_url)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['storage_dump_url']=message.text
    await bot.send_message(
            message.from_user.id,
            f'Укажите адрес склада',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_storage_address.set()

@dp.message_handler(state=FSMAdmin.typing_storage_address)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['storage_address']=message.text
    await bot.send_message(
            message.from_user.id,
            f'Укажите контакты склада',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_storage_contacts.set()

@dp.message_handler(state=FSMAdmin.typing_storage_contacts)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['storage_contacts']=message.text
    StorageService.AddStorage(
        data['storage_name'],
        data['storage_dump_url'],
        data['storage_address'],
        data['storage_contacts'],
        )
    await bot.send_message(
            message.from_user.id,
            f'Склад добавлен. Ответственных можно назначить выбрав склад.',
            reply_markup=Keyboards.remove()
        )
    await BotAdmin.ReturnToAdminMenu(bot, message)
    bazonService.UpdatedDB()
    dismaService.UpdatedDB()


@dp.message_handler(state=FSMAdmin.typing_responsible_name)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['name']=message.text
    await bot.send_message(
            message.from_user.id,
            f'Укажие его ник в телеграмм(без @)',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_responsible_username.set()
    
@dp.message_handler(state=FSMAdmin.typing_responsible_username)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['tg_username']=message.text
    await bot.send_message(
            message.from_user.id,
            f'Ответственный добавлен',
            reply_markup=Keyboards.remove()
        )
    ResponsibleService.AddResponsible(data['name'], data['tg_username'])
    await BotAdmin.ReturnToAdminMenu(bot, message)


@dp.message_handler(filters.Text(equals='Посмотреть всех ответственных'), state=FSMAdmin.choosing_action)
async def handle_message(message: types.Message, state:FSMContext):
    resp  = ResponsibleService.GetAllResponsibles()
    await bot.send_message(
            message.from_user.id,
            f'Ответственные:\n{resp}',
            reply_markup=Keyboards.GetResponsiblesKb()
        )
    await FSMAdmin.choosing_responsible.set()
    
@dp.message_handler(
    lambda x : int(x.text.replace(' ', '').split('–')[0]) in ResponsibleService.getResponsiblesIDs(), 
    state=FSMAdmin.choosing_responsible
    )
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['selected_responsible']=int(message.text.replace(' ', '').split('–')[0])
    resp  = ResponsibleService.GetResponsibleById(data['selected_responsible'])
    await bot.send_message(
        message.from_user.id,
        resp,
        reply_markup=Keyboards.ActionsWithRespobsibleKb()
    )
    await FSMAdmin.choosing_action_with_responsible.set()
    

@dp.message_handler(filters.Text(equals='Удалить ответственного'), state=FSMAdmin.choosing_action_with_responsible)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        ResponsibleService.DeleteResponsibleById(data['selected_responsible'])
    resp  = ResponsibleService.GetAllResponsibles()
    await bot.send_message(
            message.from_user.id,
            f'Ответственный удален:\n{resp}',
            reply_markup=Keyboards.remove()
        )
    await BotAdmin.ReturnToAdminMenu(bot, message)
    
@dp.message_handler(filters.Text(equals='Посмотреть все склады'), state=FSMAdmin.choosing_action)
async def handle_message(message: types.Message, state:FSMContext):
    storages  = StorageService.GetAllStorages()
    await bot.send_message(
            message.from_user.id,
            f'Склады\n{storages}',
            reply_markup=Keyboards.GetStoragesKb()
        )
    await FSMAdmin.choosing_store.set()
    
    
@dp.message_handler(filters.Text(equals=StorageService.getStorageNames()), state=FSMAdmin.choosing_store)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['storage'] = message.text
    stor_info = StorageService.GetStoreInfo(message.text)
    await bot.send_message(
            message.from_user.id,
            f'Выберите действие со складом\n{stor_info}',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    await FSMAdmin.choosing_action_with_store.set()
    
    

@dp.message_handler(filters.Text(equals='Удалить склад'), state=FSMAdmin.choosing_action_with_store)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.DeleteStorage(data['storage'])
    await bot.send_message(
            message.from_user.id,
            f'Склад удален',
            reply_markup=Keyboards.remove()
        )
    await BotAdmin.ReturnToAdminMenu(bot, message)
    
@dp.message_handler(filters.Text(equals='Изменить название'), state=FSMAdmin.choosing_action_with_store)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Введите новое название для склада',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_new_stor_name.set()
    
  
@dp.message_handler( state=FSMAdmin.typing_new_stor_name)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.ChangeStorName(data['storage'], message.text)
    await bot.send_message(
            message.from_user.id,
            f'Назвние ({message.text}) для склада установлено',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    stor_info = StorageService.GetStoreInfo(message.text)
    await bot.send_message(
            message.from_user.id,
            f'Выберите действие со складом\n{stor_info}',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    await FSMAdmin.choosing_action_with_store.set()
    
    
    
@dp.message_handler(filters.Text(equals='Изменить ссылку'), state=FSMAdmin.choosing_action_with_store)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Введите ссылку на склад',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_new_link.set()
    
  
@dp.message_handler(state=FSMAdmin.typing_new_link)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.ChangeStorURL(data['storage'], message.text)
    await bot.send_message(
            message.from_user.id,
            f'Ссылка ({message.text}) для склада {data["storage"]} установлена',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    stor_info = StorageService.GetStoreInfo(data["storage"])
    await bot.send_message(
            message.from_user.id,
            f'Выберите действие со складом\n{stor_info}',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    await FSMAdmin.choosing_action_with_store.set()
    
    
@dp.message_handler(filters.Text(equals='Изменить адрес'), state=FSMAdmin.choosing_action_with_store)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Введите новый адрес склада',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_new_address.set()
    
  
@dp.message_handler(state=FSMAdmin.typing_new_address)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.ChangeStorAddress(data['storage'], message.text)
    await bot.send_message(
            message.from_user.id,
            f'Адрес ({message.text}) для склада {data["storage"]} установлен',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    stor_info = StorageService.GetStoreInfo(data["storage"])
    await bot.send_message(
            message.from_user.id,
            f'Выберите действие со складом\n{stor_info}',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    await FSMAdmin.choosing_action_with_store.set()
    
    
@dp.message_handler(filters.Text(contains='Установить ответственного'), state=FSMAdmin.choosing_action_with_store)
async def handle_message(message: types.Message, state:FSMContext):
    resp_number = ''.join([el if str(el).isdigit() else '' for el in message.text])
    async with state.proxy() as data:
        data['selected_responsible_id'] = resp_number
    await bot.send_message(
            message.from_user.id,
            f'Выберите ответственного #{resp_number}',
            reply_markup=Keyboards.GetResponsiblesKb()
        )
    await FSMAdmin.choosing_responsible_for_storage.set()
    
@dp.message_handler(
    filters.Text(equals="Снять"),
    state=FSMAdmin.choosing_responsible_for_storage
    )
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.SetResponsiblForStorageIdById(
            data['selected_responsible_id'],
            'NULL',
            data['storage']   
        )
    await bot.send_message(
            message.from_user.id,
            f'Ответственный снят',
            reply_markup=Keyboards.remove()
        )
    await BotAdmin.ReturnToAdminMenu(bot,message)
    
@dp.message_handler(
    lambda x : int(x.text.replace(' ', '').split('–')[0]) in ResponsibleService.getResponsiblesIDs(), 
    state=FSMAdmin.choosing_responsible_for_storage
    )
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.SetResponsiblForStorageIdById(
            data['selected_responsible_id'],
            int(message.text.replace(' ', '').split('–')[0]),
            data['storage']   
        )
    await BotAdmin.ReturnToAdminMenu(bot,message)
@dp.message_handler(filters.Text(equals='Изменить телефон'), state=FSMAdmin.choosing_action_with_store)
async def handle_message(message: types.Message, state:FSMContext):
    await bot.send_message(
            message.from_user.id,
            f'Введите новый контакт',
            reply_markup=Keyboards.remove()
        )
    await FSMAdmin.typing_new_phone.set()
    
    
  
@dp.message_handler(state=FSMAdmin.typing_new_phone)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.ChangeStorContacts(data['storage'], message.text)
    await bot.send_message(
            message.from_user.id,
            f'Контакты ({message.text}) для склада {data["storage"]} установлен',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    stor_info = StorageService.GetStoreInfo(data["storage"])
    await bot.send_message(
            message.from_user.id,
            f'Выберите действие со складом\n{stor_info}',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    await FSMAdmin.choosing_action_with_store.set()
    
    
@dp.message_handler(state=FSMAdmin.typing_new_phone)
async def handle_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        StorageService.ChangeStorContacts(data['storage'], message.text)
    await bot.send_message(
            message.from_user.id,
            f'Контакты ({message.text}) для склада {data["storage"]} установлен',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    stor_info = StorageService.GetStoreInfo(data["storage"])
    await bot.send_message(
            message.from_user.id,
            f'Выберите действие со складом\n{stor_info}',
            reply_markup=Keyboards.ActionsWithStorageKb()
        )
    await FSMAdmin.choosing_action_with_store.set()
    
    

  
  
    
@dp.message_handler()
async def handle_message(message: types.Message, state:FSMContext):
    # res = dService.FindInDisma(message.text)
    
    ...
    
    


if __name__ == '__main__':
    print('started')
    scheduler.start()
    schedule()
    executor.start_polling(dp, skip_updates=False)