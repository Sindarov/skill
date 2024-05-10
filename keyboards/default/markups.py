from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
btnProfile = KeyboardButton("Profile 👤")
mainMenu.add(btnProfile)

btnBalance = KeyboardButton("Balance 📜")
mainMenu.add(btnBalance)

btnbuy = KeyboardButton("Premium Files 🎁")
mainMenu.add(btnbuy)



