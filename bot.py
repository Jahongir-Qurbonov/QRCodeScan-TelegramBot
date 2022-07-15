from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CallbackContext, CommandHandler
from pyzbar.pyzbar import decode
from PIL import Image
from os import remove

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

token = "_token_"

updater = Updater(token=token, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
dispatcher = updater.dispatcher

...
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Botimizga xush kelibsiz!\nMenga QR Cod tashlang men undagi ma'lumotni olib beraman.")


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Menga QR Cod tashlang men undagi ma'lumotni olib beraman.")


def decode_qr(update: Update, context: CallbackContext):
	foto = context.bot.getFile(update.message['photo'][0]['file_id'])
	foto.download('temp.png')
	try:
		result = decode(Image.open('temp.png'))
		context.bot.send_message(chat_id=update.message.chat_id, text=result[0].data.decode("utf-8"))
		remove("temp.png")
	except Exception:
		context.bot.send_message(chat_id=update.message.chat_id, text="Rasm xira yoki unda QR kod yo'q")
...

dispatcher.add_handler(MessageHandler(Filters.photo, decode_qr))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text  & (~Filters.command), echo))

updater.start_polling()
