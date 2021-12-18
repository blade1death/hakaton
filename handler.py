from main import bot, dp, admin_id
from aiogram.types import Message


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler()
async def echo(message: Message):
    text = f"{message.text}"
    await bot.send_message(chat_id=message.from_user.id, text=text)
