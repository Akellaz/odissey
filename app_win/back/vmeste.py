import sqlite3
import operator
from datetime import datetime, date
from aiogram import Bot, Dispatcher, types
from aiogram_dialog import Window, Dialog, DialogManager, StartMode, setup_dialogs
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope, Button, Back, Next, Multiselect
from aiogram_dialog.widgets.text import Const, Format, Jinja, Text
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ChatType

SELECTED_DAYS_KEY = "selected_dates"

# Сохраните токен бота здесь
TOKEN = "YOUR_BOT_TOKEN_HERE"
GROUP_ID = "-100xxxxxxxxxx"  # ID вашей группы ВМЕСТЕ

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

class MySG(StatesGroup):
    window1 = State()  # Дата
    window2 = State()  # Дата и Время
    window3 = State()  # Результат

# Остальная логика календаря остается прежней...

# Функция обработки команды /send_schedule
@dp.message(Command("send_schedule"))
async def send_schedule(message: types.Message, dialog_manager: DialogManager):
    """
    Отправляет расписание выбранной даты и времени в указанную группу.
    """
    try:
        # Получаем данные из диалогового менеджера
        dialog_data = dialog_manager.dialog_data
        author_user = dialog_data.get('author_user', '')
        times = dialog_data.get('times', [])
        selected_date = dialog_data.get('date', None)
        
        if not all([author_user, times, selected_date]):
            raise ValueError("Недостаточно данных для формирования расписания.")
            
        schedule_message = f"<b>Расписание:</b>\n\n<b>Дата:</b> {selected_date}\n<b>Автор:</b> {author_user}\n<b>Записанные часы:</b> {' '.join(times)}"
        
        # Проверяем тип чата перед отправкой
        chat_type = message.chat.type
        if chat_type != ChatType.PRIVATE:
            await bot.send_message(chat_id=message.chat.id, text="Эта команда доступна только в приватных сообщениях.", reply_to_message_id=message.message_id)
            return
        
        # Отправляем сообщение в группу
        await bot.send_message(chat_id=GROUP_ID, text=schedule_message, parse_mode='HTML')
        await message.answer("Расписание успешно отправлено!")
    
    except Exception as e:
        print(f"Ошибка отправки расписания: {e}")
        await message.answer("Возникла ошибка при отправке расписания.")

# Инициализация диалога и стартовая точка
@dp.message(Command("start"))
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)

# Запуск бот-поллинга
if __name__ == "__main__":
    setup_dialogs(dp)
    dp.run_polling(bot)
