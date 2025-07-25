import logging
import os
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from datetime import datetime
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def fn_create():
    current_time = datetime.now()
    timestamp_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename_with_timestamp = f"log_{timestamp_str}"
    return filename_with_timestamp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def typephoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This message is of type photo")

async def typevideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This message is of type video")

async def typeaudio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This message is of type audio")

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(chat_id=update.effective_chat.id, document="https://python-telegram-bot.org/static/testfiles/telegram.gif")

# async def savefile(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     file_id = update.message.document.file_id
#     new_file = await context.bot.get_file(file_id)
#     directory = "downloads"
#     filename = fn_create()
#     full_path = os.path.join(directory, filename)
#     try:
#         await new_file.download_to_drive(full_path)
#     except:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="There is some error contact admin")
#     finally:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="File saved successfully")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    typephoto_handler = MessageHandler(filters.PHOTO, typephoto)
    typevideo_handler = MessageHandler(filters.VIDEO, typevideo)
    typeaudio_handler = MessageHandler(filters.AUDIO, typeaudio)
    greeting_handler = CommandHandler('greet', greet)
    savefile_handler = MessageHandler(filters.Document, savefile)
    # Main handlers
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(typephoto_handler)
    application.add_handler(typevideo_handler)
    application.add_handler(typeaudio_handler)
    application.add_handler(greeting_handler)
    # application.add_handler(savefile_handler)
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(unknown_handler)
    application.run_polling()