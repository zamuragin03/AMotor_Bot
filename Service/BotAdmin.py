from Keyboards import Keyboards
from States import FSMAdmin

async def ReturnToAdminMenu(bot, message,):
    await bot.send_message(
        message.from_user.id,
        'Выберите действие',
        reply_markup=Keyboards.GetAdminKb()
    )
    await FSMAdmin.choosing_action.set()