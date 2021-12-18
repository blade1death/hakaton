
import asyncio
from aiogram import Bot,Dispatcher, executor
Bot_Token="5074249875:AAE-z-JmX0HbO0QlH-M4k4DRPODXQr_aja0"
loop=asyncio.get_event_loop()
bot=Bot(Bot_Token,parse_mode="HTML")
dp=Dispatcher(bot,loop=loop)
if __name__=="__main__":
    from handler import dp, send_to_admin
    executor.start_polling(dp,on_startup=send_to_admin)