
import asyncio
from aiogram import Bot,Dispatcher, executor


admin_id=1274214471
Bot_Token="5041117492:AAEpyQl4e9IX2_5dPVSbqLU1iNN4PdYUCJ8"
loop=asyncio.get_event_loop()
bot=Bot(Bot_Token,parse_mode="HTML")
dp=Dispatcher(bot,loop=loop)
if __name__=="__main__":
    from handler import dp, send_to_admin
    executor.start_polling(dp,on_startup=send_to_admin)