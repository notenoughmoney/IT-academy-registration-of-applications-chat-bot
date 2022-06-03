from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.base import InputFile
from aiogram import types

def column(matrix, i): return [row[i] for row in matrix]


def getReasonId(array, text):
    for item in array:
        if item[0] == text:
            return item[1]


def getReasonText(array, id):
    for item in array:
        if item[1] == id:
            return item[0]


def getRequestByTgId(array, id):
    for item in array:
        if item["tg_id"] == id:
            return item


def getIdByTgId(array, tg_id):
    for item in array:
        if item.get("tg_id") == int(tg_id):
            return item.get("id")


# формирует описание конкретной заявки ДЛЯ ПОЛЬЗОВАТЕЛЯ
def form_text_req(info, tg_id):
    caption = f"ID: {tg_id}\n\n"
    caption += f"Заявка: {info.get('specific_name')}\n\n"
    caption += f"Описание: {info.get('messages')[0].get('text')}\n\n"
    caption += f"Дата: {info.get('date')[0:10]} {info.get('date')[11:16]} \n\n"
    caption += f"Статус: {info.get('stage').get('name')}\n"

    if info.get('messages')[0].get('files'):
        path = types.InputFile.from_url("http://tucana.org:3100/" + info.get('messages')[0].get('files')[0].get('path'), filename="1.png")
    else:
        path = None
    return [caption, path]


# формирует список всех заявок, в зависимости от list
def form_text_list(page, pages, reqs, list):
    text = None
    if list == "my":
        text = "Ваши заявки:\n\n"
    elif list == "exchange":
        text = "Биржа заявок\nДля вашего отдела доступны:\n\n"
    elif list == "todo":
        text = "Заявки к выполнению:\n\n"

    text += f"Страница {page} из {pages}\n\n"
    i = len(reqs) - (page - 1) * 5
    if len(reqs) == 0:
        return "Вы пока не подавали заявок"
    while i > len(reqs) - page * 5:
        req = getRequestByTgId(reqs, i)
        if req is None:
             break
        else:
            if list == "my":
                text += f"{i}.\n" \
                        f"Заявка: {req.get('specific_name')}\n" \
                        f"Дата подачи: {req.get('date')[0:10]} {req.get('date')[11:16]} \n" \
                        f"Статус: {req.get('stage').get('name')} \n\n"
            elif list == "exchange":
                text += f"{i}.\n" \
                        f"Заявка: {req.get('request').get('specific_name')}\n" \
                        f"Дата подачи: {req.get('request').get('date')[0:10]} {req.get('request').get('date')[11:16]} \n" \
                        f"Статус: {req.get('request').get('stage').get('name')} \n\n"
        i -= 1
    return text


# формирует клавиатуру для списка заявок ДЛЯ ПОЛЬЗОВАТЕЛЯ
def form_keyboard(page, pages, length, c):
    btnArray = [None] * 5
    btn_left = None
    btn_right = None

    if c is None:
        # сначала кнопки, привязанные к заявкам
        for i in range(5):
            btnArray[i] = InlineKeyboardButton(f"{length - i}", callback_data=f"show_{length - i}") if (length - i > 0) else None
        # потом кнопку вправо
        btn_right = InlineKeyboardButton(">", callback_data="right") if (page < pages) else None
    elif c.data == 'left':
        btn_left = InlineKeyboardButton("<", callback_data="left") if (page - 1 > 1) else None
        btn_right = InlineKeyboardButton(">", callback_data="right") if (page - 1 < pages) else None
        # сколько заявок доступно на текущей странице
        onPage = 5 if ((page - 1) * 5 <= length) else length % 5
        for i in range(onPage):
            btnArray[i] = InlineKeyboardButton(f"{length - (page - 2) * 5 - i}", callback_data=f"show_{length - (page - 2) * 5 - i}")
    elif c.data == 'right':
        btn_left = InlineKeyboardButton("<", callback_data="left") if (page + 1 > 1) else None
        btn_right = InlineKeyboardButton(">", callback_data="right") if (page + 1 < pages) else None
        # сколько заявок доступно на текущей странице
        onPage = 5 if ((page + 1) * 5 <= length) else length % 5
        for i in range(onPage):
            btnArray[i] = InlineKeyboardButton(f"{length - page * 5 - i}", callback_data=f"show_{length - page * 5 - i}")

    # формируем клавиатуру
    keyboard = InlineKeyboardMarkup()
    # кнопки назад и вперёд уже сформированы
    # формириуем массив кнопок, которые отправятсся пользователю
    buttonsToSend = []
    # если кнопка равна None, то не заносим её в массив
    for btn in [btn_left, *btnArray, btn_right]:
        if btn is not None:
            buttonsToSend.append(btn)
    keyboard.row(*buttonsToSend)
    return keyboard

