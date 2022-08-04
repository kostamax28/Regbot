from aiogram import Bot, types

from aiogram.dispatcher import Dispatcher

from aiogram.utils import executor

from aiogram import types

from aiogram.dispatcher.filters import Text

from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.dispatcher import FSMContext

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN, ADMIN_ID

bot = Bot(token=TOKEN)

dp = Dispatcher(bot,storage=MemoryStorage())

errormsg=["🚫Вы не состоите в привате."]

class Mydialog(StatesGroup):

    otvet = State()

@dp.message_handler(commands=['start'])

async def process_start_command(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton(text="🔗Привязать")

    keyboard.add(button_1)

    button_2 = "⛓Отвязать"

    keyboard.add(button_2)

    await bot.send_message(message.from_user.id, f"🌟Привет, я бот который поможет тебе зарегистрировать твой HWID в чите FireLine\n🆔 Твой айди: {message.from_user.id}", reply_markup=keyboard)

@dp.message_handler(Text(equals="🔗Привязать"))

async def with_puree(message: types.Message):

    if message.from_user.username==None:

        await bot.send_message(message.from_user.id, "🚫У вас нету никнейма!")

    else:

        user_channel_status = await bot.get_chat_member(chat_id='-1001799340034', user_id=message.from_user.id)

        if user_channel_status["status"] != 'left':

            await message.reply("✅Осталось совсем чуть чуть.")

            await bot.send_message(message.from_user.id, "❓ Отправь HWID для регистрации:")

            await Mydialog.otvet.set()

        else:

            await bot.send_message(message.from_user.id, errormsg[0])

@dp.message_handler(state=Mydialog.otvet)

async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:

        data['text'] = message.text

        user_message = data['text']

        await bot.send_message(message.from_user.id, '✅Готово, ожидайте 15 секунд, и HWID будет зарегестрирован'.)

        buttons = [

            types.InlineKeyboardButton(text="User", url=f"tg://resolve?domain={message.from_user.username}")

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        keyboard.add(*buttons)

        await bot.send_message(ADMIN_ID, f'\n🖥HWID: {user_message}: ID: {message.from_user.id}\n\n👍Действие: Попытка регистрации\n', reply_markup=keyboard)

        

    await state.finish()

@dp.message_handler(lambda message: message.text == "⛓Отвязать")

async def without_puree(message: types.Message):

    if message.from_user.username==None:

        await bot.send_message(message.from_user.id, "🚫У вас нету никнейма!")

    else:

        user_channel_status = await bot.get_chat_member(chat_id='-1001799340034', user_id=message.from_user.id)

        if user_channel_status["status"] != 'left':

            buttons = [

            types.InlineKeyboardButton(text="User", url=f"tg://resolve?domain={message.from_user.username}")

            ]

            keyboard = types.InlineKeyboardMarkup(row_width=1)

            keyboard.add(*buttons)

            await bot.send_message(ADMIN_ID, f'\n🖥HWID : {message.from_user.id}\n\n👍Действие: Попытка отвязки\n', reply_markup=keyboard)

            await message.reply("✅Готово, ожидайте 15 секунд, и HWID будет отвязан".)

        else:

            await bot.send_message(message.from_user.id, errormsg[0])

if __name__ == '__main__':

    executor.start_polling(dp)

