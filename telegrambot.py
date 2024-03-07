# coding: UTF-8

import config
from bot import ComicbookTelegramBot


if __name__ == "__main__":
    bot = ComicbookTelegramBot(config.TELEGRAM_BOT_TOKEN)
    bot.start()
