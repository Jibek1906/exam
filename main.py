import asyncio
import logging

from bot_config import dp, bot, database

from handlers.start import start_router
from handlers.filing_a_complaint import filing_a_complaint_router

async def on_startup(bot):
    database.create_tables()

async def main():
    dp.include_router(start_router)
    dp.include_router(filing_a_complaint_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())