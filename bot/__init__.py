from telegram.ext import Updater, CommandHandler
import logging
import threading

import config
from crawler import Crawler

logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("bot")


class ComicbookTelegramBot:
    def __init__(self, token):
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler('start', handler_start))
        self.updater.dispatcher.add_handler(CommandHandler('comic', handler_comic))

    def start(self):
        self.updater.start_polling()
        # self.updater.idle()

    def stop(self):
        self.updater.stop()


def handler_start(bot, update):
    update.message.reply_text('Hello World!')


def handler_comic(bot, update):
    texts = update.message.text.split()
    if len(texts) > 1:
        def check_comic(is_started=False, is_generating=False):
            result = Crawler.crawl(texts[1])
            data = result['data']

            if data['code'] == 201:
                if not is_started:
                    update.message.reply_text("Task started.")
                    # bot.editMessageText(chat_id=chatid, message_id=messageid, text="Task started.")
                    is_started = True

            elif data['code'] == 200:
                update.message.reply_text("Work done. Sending file...")
                # bot.editMessageText(chat_id=chatid, message_id=messageid, text="Work done. Transferring file...")
                data['url'] = config.URL + data['url']
                bot.sendDocument(chat_id=update.message.chat_id, document=open(result['path'], 'rb'))
                return
            elif data['code'] == 400 or data['code'] == 401:
                update.message.reply_text(data['message'])
                return
            elif data['code'] == 202:
                if not is_generating:
                    reply_message = "Generating comic file...."
                    # bot.editMessageText(chat_id=chatid, message_id=messageid, text=reply_message)
                    update.message.reply_text(reply_message)
                    is_generating = True

            timer = threading.Timer(3.0, check_comic, [is_started, is_generating])
            timer.start()

        check_comic()

    else:
        update.message.reply_text('error')






