from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher
from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
import sqlite3
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import StartMode
from aiogram_dialog import setup_dialogs
from aiogram.filters.callback_data import CallbackData
from datetime import date
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Const, Jinja
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale

session = AiohttpSession(proxy='http://proxy.server:3128')




storage = MemoryStorage()
bot = Bot(token="8322108172:AAHM-T1Bi-HzLuMr9lJXLkx-vzXeMdCzkig", session=session)
dp = Dispatcher(storage=storage)

class MySG(StatesGroup):
    window1 = State()  #Выбор Добавить/Посмотреть
    window2 = State()  #Дата
    window3 = State()  #Время
    window4 = State()  #Имя
    window5 = State()  #Результат

# # ПОСМОТРЕТЬ
async def calendar_show(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer(
        "_",
        reply_markup=await SimpleCalendar().start_calendar()
    )

async def getter(dialog_manager: DialogManager, **kwargs):

    date_db = dialog_manager.find("date").get_value()
    time_db = dialog_manager.find("time").get_value()
    name_db = dialog_manager.find("name").get_value()

    connection = sqlite3.connect('routes.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO ORG (name, date, time) VALUES ('"+name_db+"','"+date_db+"','"+time_db+"')")
        connection.commit()
        return {
            "date": dialog_manager.find("date").get_value(),
            "time": dialog_manager.find("time").get_value(),
            "name": dialog_manager.find("name").get_value(),
        }

    except:
        return {
            "date": dialog_manager.find("date").get_value(),
            "time": dialog_manager.find("time").get_value(),
            "name": 'Это время занято',
        }

dialog = Dialog(
    Window(
        Format("Привет, {event.from_user.username}!"),
        Button(
            Const("Добавить"),
            id="go",
            on_click=Next(),
            ),
        Button(
            Const("Посмотреть"),
            id="button1",
            on_click=calendar_show,
            ),
        state=MySG.window1,
    ),
    Window(
        Const("Шаг 1"),
        Const("Введите дату в формате dd/mm/yyyy"),
        TextInput(id="date", on_success=Next()),
        Back(text=Const("Назад")),
        state=MySG.window2,
    ),
    Window(
        Const("Шаг 2"),
        Const("Введите время в формате hh:mm"),
        TextInput(id="time", on_success=Next()),
        Back(text=Const("Назад")),
        state=MySG.window3,
    ),
    Window(
        Const("Шаг 3"),
        Const("Введите имя"),
        TextInput(id="name", on_success=Next()),
        Back(text=Const("Назад")),
        state=MySG.window4,
    ),
    Window(
        Jinja(
            "<b>Дата</b>: {{date}}\n"
            "<b>Время</b>: {{time}}\n"
            "{{name}}"
        ),
        state=MySG.window5,
        getter=getter,
        parse_mode="html",
    ),
)
dp.include_router(dialog)

# ПОСМОТРЕТЬ # Simple calendar usage
@dp.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2025, 9, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        choice = f'{date.strftime("%d/%m/%Y")}'
        rsum=[]
        connection = sqlite3.connect('routes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT time, name FROM ORG WHERE date = '"+choice+"'")

        for i in cursor.fetchall():
            rsum.append(i)

        await callback_query.message.answer(
            f'{date.strftime("%d/%m/%Y")}\n'+'\n'.join(map(str, rsum)),
        )

@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)

setup_dialogs(dp)

if __name__ == '__main__':
    dp.run_polling(bot)

