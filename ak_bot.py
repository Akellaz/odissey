import sqlite3
import operator
#from typing import Any
from datetime import datetime, date
from aiogram import Bot, Dispatcher

from babel.dates import get_day_names, get_month_names

from aiogram_dialog import Window, Dialog, DialogManager, StartMode, setup_dialogs

from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData

from aiogram.types import CallbackQuery, Message 

from aiogram_dialog.widgets.kbd import (
    Calendar,
    CalendarScope,
    #ManagedCalendar,
    #SwitchTo,
    Button,
    Back,
    Next,
    Multiselect,
    #CalendarUserConfig,
)

from aiogram_dialog.widgets.kbd.calendar_kbd import (
    DATE_TEXT,
    TODAY_TEXT,
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
)

from aiogram_dialog.widgets.text import Const, Format, Jinja, Text
from aiogram_dialog.widgets.input import TextInput

from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, \
    get_user_locale


SELECTED_DAYS_KEY = "selected_dates"



storage = MemoryStorage()
bot = Bot(token="8322108172:AAHM-T1Bi-HzLuMr9lJXLkx-vzXeMdCzkig")
dp = Dispatcher(storage=storage)



class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short", context="stand-alone", locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get(SELECTED_DAYS_KEY, [])
        if serial_date in selected:
            return self.mark
        return await self.other.render_text(data, manager)


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            "wide", context="stand-alone", locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                date_text=MarkedDay("🔴", DATE_TEXT),
                today_text=MarkedDay("⭕", TODAY_TEXT),
                header_text="~~~~~ " + Month() + " ~~~~~",
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text="~~~~~ " + Format("{date:%Y}") + " ~~~~~",
                this_month_text="[" + Month() + "]",
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
            ),
        }


class MySG(StatesGroup):
    window1 = State()  #Выбор Добавить/Посмотреть
    window2 = State()  #Дата и Время
   # window3 = State()  #Имя
    window3 = State()  #Результат




# # ПОСМОТРЕТЬ
async def calendar_show(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer(
        "_",
        reply_markup=await SimpleCalendar().start_calendar()
    )
 
# let's assume this is our window data getter
async def get_time(dialog_manager: DialogManager, **kwargs):


    time_slots_zero1 = [
        ("8:00", '8:00'),
        ("9:00", '9:00'),
        ("10:00", '10:00'),
        ("11:00", '11:00'),
        ("12:00", '12:00'),
        ("13:00", '13:00'),
        ("14:00", '14:00'),
        ("15:00", '15:00'),
        
    ]
    time_slots_zero2 = [
        ("16:00", '16:00'),
        ("17:00", '17:00'),
        ("18:00", '18:00'),
        ("19:00", '19:00'),
        ("20:00", '20:00'),
        ("21:00", '21:00'),
        ("22:00", '22:00'),
        ("23:00", '23:00'),
]

 
    
    connection = sqlite3.connect('ak_data.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT time FROM book WHERE date=?", (g_selected_date,))
    
    time_from_db = [row[0] for row in cursor.fetchall()]
    time_slots = [(key, value) for key, value in time_slots_zero1 if value not in time_from_db]
    time_slots2 = [(key, value) for key, value in time_slots_zero2 if value not in time_from_db]
    

    
    return {
        "time_slots": time_slots,
        "count": len(time_slots),
        "time_slots2": time_slots2,
        "count2": len(time_slots2),
    }
    
# # ДОБАВИТЬ
async def getter(dialog_manager: DialogManager, **kwargs):
    
    checked_time_slots_ids = dialog_manager.find("m_time_slots").get_checked()

    dialog_manager.dialog_data['username'] = kwargs['event_from_user'].username
    author_user = dialog_manager.dialog_data['username']
    #date_db = dialog_manager.find("date").get_value()
    name_db = author_user
    
    connection = sqlite3.connect('ak_data.db')
    cursor = connection.cursor()

    for item in checked_time_slots_ids:
        cursor.execute("INSERT INTO book (name, date, time, author) VALUES ('"+name_db+"','"+str(g_selected_date)+"','"+item+"','"+author_user+"')")      
    connection.commit()
    return {

        "date": str(g_selected_date),
        #"name": dialog_manager.find("name").get_value(),
        "author_user": author_user,
        "times": checked_time_slots_ids,
    }


async def win1_on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):

    global g_selected_date
    g_selected_date = selected_date
    
    await manager.next()

async def win2_on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):

    global g_selected_date
    g_selected_date = selected_date
    
    return g_selected_date

############### WINDOWS PART ###################
dialog = Dialog(
    Window(
        Format("Привет, {event.from_user.username}!"), 
        
        CustomCalendar(
           id="cal",
           on_click=win1_on_date_selected,
       ),  
        state=MySG.window1,
    ),
    

    
    
    Window(
        
        Const("Сначала выбери дату. Просто нажми на нужное число"),
        Const("Затем в нижней части выбери время. Можно несколько слотов"),
        Const("Когда дата нажата и галочки на нужное время стоят, то смело жми Забить!"),
         CustomCalendar(
            id="cal",
            on_click=win2_on_date_selected,
        ),   
         
         
         Multiselect(
                    Format("✓ {item[0]}"),  # Пример: `✓ Apple`
                    Format("{item[0]}"),
                    id="m_time_slots",
                    item_id_getter=operator.itemgetter(1),
                    items="time_slots",
                ),
         Multiselect(
                    Format("✓ {item[0]}"),  # Пример: `✓ Apple`
                    Format("{item[0]}"),
                    id="m_time_slots",
                    item_id_getter=operator.itemgetter(1),
                    items="time_slots2",
                ),
         
         
        Next(text=Const("Забить")),
        getter=get_time,
        state=MySG.window2,
    ),
    


    Window(
        Const("Ура! Время забронировано"),
        Jinja(
            "<b>Дата</b>: {{date}}\n"
            "<b>Время</b>: {{times}}\n"
            #"<b>Имя</b>: {{name}}\n"
            "<b>Автор</b>: {{author_user}}\n"  
        ),
        state=MySG.window3,
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
        choice = f'{date.strftime("%Y-%m-%d")}'
        rsum=[]
        connection = sqlite3.connect('ak_data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT time, name FROM book WHERE date = '"+choice+"'")
        
        for i in cursor.fetchall():
            rsum.append(i)
         
        await callback_query.message.answer(
            f'{date.strftime("%Y-%m-%d")}\n'+'\n'.join(map(str, rsum)),
        )

@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)

setup_dialogs(dp)

if __name__ == '__main__':
    dp.run_polling(bot)

