import subprocess
import sys
import os
import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO, filename="bot_log.txt",
                    filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def setup_venv():
    venv_path = os.path.join('venv', 'Scripts', 'python.exe')
    if not os.path.exists(venv_path):
        logging.info("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to create virtual environment: {e}")
            sys.exit(1)

    logging.info("Installing dependencies...")
    try:
        subprocess.run([venv_path, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install dependencies: {e}")
        sys.exit(1)


async def run_bot():
    from gui.routers import setup_routers
    dp = Dispatcher(storage=MemoryStorage())
    setup_routers(dp)
    from gui.routers import bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def main():
    setup_venv()
    logging.info("Starting bot...")
    try:
        asyncio.run(run_bot())
    except Exception as e:
        logging.error(f"Bot failed to start: {e}")


if __name__ == '__main__':
    main()
