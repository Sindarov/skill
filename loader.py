import logging
from aiogram import Bot, Dispatcher, executor, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards.default import markups
from db import Database
from keyboards.inline import inline_btns
from aiogram.types import ParseMode

logging.basicConfig(level=logging.INFO)

db = Database('database.db')
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     if message.chat.type == 'private':
#         if await check_sub_channels(config.CHANNELS, message.from_user.id):
#             await bot.send_message(message.from_user.id, f"Hi, "
#                 f"{message.from_user.first_name}!\n\n🤓🫵Do not miss the CHANCE!\n\n",
#                         reply_markup=markups.mainMenu)
#             if not db.user_exists(message.from_user.id):
#                 start_command = message.text
#                 referrer_id = str(start_command[7:])
#                 if str(referrer_id) != "":
#                     if str(referrer_id) != str(message.from_user.id):
#                         db.add_user(message.from_user.id, referrer_id)
#                         try:
#                             await bot.send_message(referrer_id,
#                                                    f"Using your referral link "
#                                                    f"{message.from_user.first_name}"
#                                                    f"(@{message.from_user.username}) has registered")
#                         except:
#                             pass
#                     else:
#                         db.add_user(message.from_user.id)
#                         await bot.send_message(message.from_user.id,
#                                                "Do not register using the referral link of yours !")
#                 else:
#                     db.add_user(message.from_user.id)
#
#         else:
#             await bot.send_message(message.from_user.id, config.not_sub_message,
#                                    reply_markup=inline_btns.show_channels())
# start_msg = ""
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     global start_msg
#     start_msg = message.text
#     if message.chat.type == 'private':
#         await bot.send_message(message.from_user.id, f"Hi, {message.from_user.first_name}!\n\n🤓🫵Do not miss the CHANCE!\n\n")
#         print(db.user_exists(message.from_user.id))
#         if db.user_exists(message.from_user.id):
#
#             if await check_sub_channels(config.CHANNELS, message.from_user.id):
#                 await bot.send_message(message.from_user.id, "Choose one of the options below 👇", reply_markup=markups.mainMenu)
#             else:
#                 await bot.send_message(message.from_user.id, config.not_sub_message,
#                                        reply_markup=inline_btns.show_channels())
#
#         if not db.user_exists(message.from_user.id):
#             start_command = message.text
#             referrer_id = str(start_command[7:])
#             if str(referrer_id) != "":
#                 if await check_sub_channels(config.CHANNELS, message.from_user.id):
#                     if str(referrer_id) != str(message.from_user.id):
#                         db.add_user(message.from_user.id, referrer_id)
#
#                         try:
#                             await bot.send_message(referrer_id,
#                                                    f"Using your referral link "
#                                                    f"{message.from_user.first_name}"
#                                                    f"(@{message.from_user.username}) has registered")
#                         except:
#                             print("xatolik")
#                     else:
#                         db.add_user(message.from_user.id)
#                         await bot.send_message(message.from_user.id,
#                                                "Do not register using the referral link of yours !")
#                 else:
#                     await bot.send_message(message.from_user.id, config.not_sub_message,
#                                            reply_markup=inline_btns.show_channels())
#             else:
#                 if await check_sub_channels(config.CHANNELS, message.from_user.id):
#                     db.add_user(message.from_user.id)
#                 else:
#                     await bot.send_message(message.from_user.id, config.not_sub_message,
#                                            reply_markup=inline_btns.show_channels())
#


start_msg = ""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global start_msg
    start_msg = message.text

    if message.chat.type == 'private':

        await bot.send_message(message.from_user.id,
                               f"Hi, {message.from_user.first_name}!\n\nDo not miss the chance🎯\n\nYou are in the right path✅")

        if db.user_exists(message.from_user.id):

            if await check_sub_channels(config.CHANNELS, message.from_user.id):
                await bot.send_message(message.from_user.id, "Choose one of the options below 👇",
                                       reply_markup=markups.mainMenu)
            else:
                await bot.send_message(message.from_user.id, config.not_sub_message,
                                       reply_markup=inline_btns.show_channels())
        else:
            start_command = message.text
            referrer_id = str(start_command[7:])

            if referrer_id != "":
                if await check_sub_channels(config.CHANNELS, message.from_user.id):
                    if referrer_id != str(message.from_user.id):
                        # Add user with referrer_id
                        db.add_user(message.from_user.id, referrer_id)
                        await bot.send_message(message.from_user.id, "Choose one of the options below 👇",
                                               reply_markup=markups.mainMenu)

                        try:
                            # Notify referrer
                            await bot.send_message(referrer_id,
                                                   f"Using your referral link {message.from_user.first_name} (@{message.from_user.username}) has registered")
                        except Exception as e:
                            print("Error notifying referrer:", e)
                    else:
                        # Add user without referrer_id (self-referral)
                        db.add_user(message.from_user.id)
                        await bot.send_message(message.from_user.id, "Do not register using your own referral link!")
                        await bot.send_message(message.from_user.id, "Choose one of the options below 👇",
                                               reply_markup=markups.mainMenu)
                else:
                    # User not subscribed, send a message with channel options
                    await bot.send_message(message.from_user.id, config.not_sub_message,
                                           reply_markup=inline_btns.show_channels())
            else:
                if await check_sub_channels(config.CHANNELS, message.from_user.id):
                    # Add user without referrer_id
                    db.add_user(message.from_user.id)
                    await bot.send_message(message.from_user.id, "Choose one of the options below 👇",
                                           reply_markup=markups.mainMenu)
                else:
                    # User not subscribed, send a message with channel options
                    await bot.send_message(message.from_user.id, config.not_sub_message, reply_markup=inline_btns.show_channels())


print(start_msg)






@dp.message_handler(text="Profile 👤")
async def bot_message(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Hurmatli foydalanuvchi, ball yig'ish uchun ushbu referalni do'stlaringiz "
                           f"bilan ulashing \n\n     ---    \n\n https://t.me/{config.BOT_NICKNAME}?start={message.from_user.id}\n\n\nBitta referal = 1 point")


@dp.message_handler(text="Balance 📜")
async def check_balance(message: types.Message):
    db.count_referrer(message.from_user.id)
    user_id = message.from_user.id
    balance = db.get_user_balance(user_id)
    if balance is None:
        balance = 0
    if balance == 0:
        await message.answer(f"Your current balance: {balance} point")
    else:
        await message.answer(f"Your current balance: {balance} points")


@dp.callback_query_handler(text="subchanneldone")
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    if await check_sub_channels(config.CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id, f"Welcome, {message.from_user.first_name}",
                               reply_markup=markups.mainMenu)

        if str(start_msg[7:]) != str(message.from_user.id):
            db.add_user(message.from_user.id, start_msg[7:])

            try:
                await bot.send_message(int(start_msg[7:]),
                                       f"Using your referral link "
                                       f"{message.from_user.first_name}"
                                       f"(@{message.from_user.username}) has registered")
            except:
                print("xatolik")
        else:
            db.add_user(message.from_user.id)

            await bot.send_message(message.from_user.id,
                                   "Do not register using the referral link of yours !")



    else:
        await bot.send_message(message.from_user.id, config.not_sub_message, reply_markup=inline_btns.show_channels())



# @dp.callback_query_handler(text="Buy Something")
# async def balance_handler(message: types.Message):
#     db.count_referrer(message.from_user.id)
#     user_id = message.from_user.id
#     amount_spent = 5
#     await bot.delete_message(message.from_user.id, message.message.message_id)
#     if not db.purchased(message.from_user.id):
#         user_balance = db.get_user_balance(user_id)
#         if user_balance is None:
#             user_balance = 0
#         if user_balance >= amount_spent:
#             if db.deduct_balance(user_id, amount_spent):
#                 # Inform the user about the successful purchase
#                 await bot.send_message(message.from_user.id, f"Your Purchase was successful‼✅\n\nYour updated balance: "
#                                                              f"{user_balance - amount_spent} points")
#                 chat_id = -1002125536910
#                 invite_link = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)
#                 await bot.send_message(message.from_user.id, f"Here is your invite link: {invite_link.invite_link}")
                
#                 db.DSAT_purchased(message.from_user.id)
#                 db.del_ref(message.from_user.id)
#             else:
#                 await bot.send_message(message.from_user.id, "Failed to deduct balance. Please try again later.")
#         else:
#             await bot.send_message(message.from_user.id, f"You don't have enough points. You need to gain {amount_spent - user_balance} more points !")

#     else:
#         await bot.send_message(message.from_user.id, f"You have already purchased this product, {message.from_user.first_name}(@{message.from_user.username})☺")


@dp.callback_query_handler(text="Buy Something2")
async def balance_handler(message: types.Message):
    db.count_referrer(message.from_user.id)
    user_id = message.from_user.id
    amount_spent = 5
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if not db.purchased2(message.from_user.id):
        user_balance = db.get_user_balance(user_id)
        if user_balance is None:
            user_balance = 0
        if user_balance >= amount_spent:
            if db.deduct_balance(user_id, amount_spent):
                # Inform the user about the successful purchase
                await bot.send_message(message.from_user.id, f"Your Purchase was successful‼✅\n\nYour updated balance: "
                                                             f"{user_balance - amount_spent} points")
                chat_id = -1002135414566
                invite_link = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)
                await bot.send_message(message.from_user.id, f"Here is your invite link: {invite_link.invite_link}")

                db.DSAT_purchased2(message.from_user.id)
                db.del_ref(message.from_user.id)
            else:
                await bot.send_message(message.from_user.id, "Failed to deduct balance. Please try again later.")
        else:
            await bot.send_message(message.from_user.id,
                                   f"You don't have enough points. You need to gain {amount_spent - user_balance} more points !")

    else:
        await bot.send_message(message.from_user.id,
                               f"You have already purchased this product, {message.from_user.first_name}(@{message.from_user.username})!☺")


@dp.message_handler(text="Premium Files 🎁")
async def bot_message(message: types.Message):
    await message.answer(f"We want to provide you the PREMIUM PACKETS 🎯\n\nEach of the choices below worth 5 points‼", reply_markup=inline_btns.premium_contents())




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
