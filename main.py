import logging
from bot import start_bot

def set_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def main():
    set_logging()
    start_bot()

try:
    main()
except KeyboardInterrupt:
    exit()
