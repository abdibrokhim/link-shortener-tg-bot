from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, filters, CallbackContext)
import urllib
import requests

TELEGRAM_BOT_TOKEN = ''  # get it from https://t.me/BotFather
API_KEY = ''  # get it from https://cutt.ly/


async def start(update: Update, context):
    """ start function """

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Try /shorten <long link>',
    )


async def shorten(update: Update, context: CallbackContext):
    """ shortener function """

    args = context.args
    if len(args) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Try /shorten <long link>',
        )
    else:
        arg = ' '.join(args)
        url = urllib.parse.quote(arg)
        response = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(API_KEY, url, ))
        result = response.json()
        link = result['url']['shortLink']

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=link,
        )


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shorten", shorten))
    app.add_handler(MessageHandler(filters.ALL, start))
    print('updated ... ')

    app.run_polling()
