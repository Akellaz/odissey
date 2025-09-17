from aiogram import Bot, Dispatcher
from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
import sqlite3
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Multiselect
from aiogram_dialog.widgets.text import Const, Format
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StatesGroup, State
from aiogram_dialog import Window
#from aiogram_dialog.widgets.kbd import Button
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import StartMode, SubManager, ChatEvent
from aiogram_dialog import setup_dialogs
from aiogram.filters.callback_data import CallbackData
from datetime import date 
from aiogram_dialog.widgets.kbd import Calendar, Group, Row 
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Const, Jinja
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale
#from aiogram_dialog.widgets.kbd import  Button, ScrollingGroup
import operator

storage = MemoryStorage()
bot = Bot(token="8322108172:AAHM-T1Bi-HzLuMr9lJXLkx-vzXeMdCzkig")
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
    
    
# let's assume this is our window data getter
async def get_data(dialog_manager: DialogManager, **kwargs):
    

    #checked_items_ids = dialog_manager.find("m_fruits").get_checked()
    
    fruits = [
        ("8:00", '8:00'),
        ("9:00", '9:00'),
        ("10:00", '10:00'),
        ("11:00", '11:00'),
        ("12:00", '12:00'),
        ("13:00", '13:00'),
        ("14:00", '14:00'),
        ("15:00", '15:00'),
        
    ]
    fruits2 = [
        ("16:00", '16:00'),
        ("17:00", '17:00'),
        ("18:00", '18:00'),
        ("19:00", '19:00'),
        ("20:00", '20:00'),
        ("21:00", '21:00'),
        ("22:00", '22:00'),
        ("23:00", '23:00'),
    ]
    
    return {
        "fruits": fruits,
        "count": len(fruits),
        "fruits2": fruits2,
        "count2": len(fruits2),
        #"times": checked_items_ids,
    }
    
    
# # ДОБАВИТЬ
async def getter(dialog_manager: DialogManager, **kwargs):
    
    checked_items_ids = dialog_manager.find("m_fruits").get_checked()
    

    dialog_manager.dialog_data['firstname'] = kwargs['event_from_user'].first_name
    dialog_manager.dialog_data['lastname'] = kwargs['event_from_user'].last_name
    dialog_manager.dialog_data['username'] = kwargs['event_from_user'].username

    author_first = dialog_manager.dialog_data['firstname']
    author_last = dialog_manager.dialog_data['lastname']
    author_user = dialog_manager.dialog_data['username']

    date_db = dialog_manager.find("date").get_value()
    #time_db = dialog_manager.find("time").get_value()
    name_db = dialog_manager.find("name").get_value()
    
    connection = sqlite3.connect('ak_data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO book (name, date, author) VALUES ('"+name_db+"','"+date_db+"','"+author_user+"')")      
    connection.commit()
    return {
        "date": dialog_manager.find("date").get_value(),
        #"time": time_db,
        "name": dialog_manager.find("name").get_value(),
        "author_first": author_first,
        "author_last": author_last,
        "author_user": author_user,
        "times": checked_items_ids,
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
        #Const("Введите время в формате hh:mm"),
        #TextInput(id="time", on_success=Next()),

        Multiselect(
                   Format("✓ {item[0]}"),  # Пример: `✓ Apple`
                   Format("{item[0]}"),
                   id="m_fruits",
                   item_id_getter=operator.itemgetter(1),
                   items="fruits",
               ),
        Multiselect(
                   Format("✓ {item[0]}"),  # Пример: `✓ Apple`
                   Format("{item[0]}"),
                   id="m_fruits",
                   item_id_getter=operator.itemgetter(1),
                   items="fruits2",
               ),
  
        #Back(text=Const("Назад")),
        Next(text=Const("вперед")),
        getter=get_data,
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
            #"<b>Время</b>: {{time}}\n"
            "{{name}}\n"
            "{{author_first}}\n"
            "{{author_last}}\n"
            "{{author_user}}\n"
            "<b>фрукт</b>: {{times}}\n"

            
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
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        choice = f'{date.strftime("%d/%m/%Y")}'
        rsum=[]
        connection = sqlite3.connect('ak_data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT time, name FROM book WHERE date = '"+choice+"'")
        
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

'''
       Group(
    Row(
        Button(Const("8:00"), id="8", on_click=Next()),
        Button(Const("9:00"), id="9"),
        Button(Const("10:00"), id="10"),
        Button(Const("11:00"), id="11"),
        Button(Const("12:00"), id="12"),
        Button(Const("13:00"), id="13"),
        Button(Const("14:00"), id="14"),
        Button(Const("15:00"), id="15"),
       
    ),
        Row(
        Button(Const("16:00"), id="16"),
        Button(Const("17:00"), id="17"),
        Button(Const("18:00"), id="18"),
        Button(Const("19:00"), id="19"),
        Button(Const("20:00"), id="20"),
        Button(Const("21:00"), id="21"),
        Button(Const("22:00"), id="22"),
        Button(Const("23:00"), id="23"),
    ), 
    ),

    cursor.execute("SELECT time FROM book WHERE date = '"+date_db+"'")
    results = cursor.fetchall()

    for i in results:
        if results[i] == time_db:
            time_db = None
''' 
