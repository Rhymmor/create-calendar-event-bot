import logging
from bot import Bot

def set_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def main():
    set_logging()
    bot = Bot()
    bot.start()

try:
    main()
except KeyboardInterrupt:
    exit()
