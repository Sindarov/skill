from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import config

def show_channels():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for channel in config.CHANNELS:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
        keyboard.insert(btn)

    btnDoneSub = InlineKeyboardButton(text="Tekshirish ✔", callback_data='subchanneldone')
    keyboard.insert(btnDoneSub)
    return keyboard

def premium_contents():
    prcon = InlineKeyboardMarkup(row_width=1)

    prcon.insert(InlineKeyboardButton(text="New Diyorbek January Marathon ⚡", callback_data='Buy Something'))
    prcon.insert(InlineKeyboardButton(text=" 5 STARS ⚡", callback_data='Buy Something2'))


    return prcon

