from main import bot, dp
from aiogram.types import Message

@dp.message_handler()
async def echo(message: Message):
    text = f"{message.text}"
    await bot.send_message(chat_id=message.from_user.id, text=text)
