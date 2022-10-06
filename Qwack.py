import logging, re, aiohttp, asyncio
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from collections import namedtuple

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

delete_list = []


async def random():
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    query = ''
    async with session.get('https://random-d.uk/api/random{}'.format(query)) as r:
        if r.status == 200:
            body = await r.json()
            response = namedtuple('Response', ['message', 'url'])
            return response(message=body['message'], url=body['url'])
        else:
            raise CouldNotGetDuckError(r.status)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Non servo ad un cazzo, solo coprire le bestemmie")


async def qwack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_async = await random()
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Bestemmia rilevata")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=random_async.url)
    delete_list.append(update.message.message_id + 1)


async def del_qwack(context: ContextTypes.DEFAULT_TYPE):
    if delete_list:
        await context.bot.delete_message(chat_id='-1001283327584', message_id=delete_list.pop())


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [InlineQueryResultArticle(
        id=query.upper(),
        title='Caps',
        input_message_content=InputTextMessageContent(query.upper())
    )]
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


class CouldNotGetDuckError(Exception):
    pass


if __name__ == '__main__':
    application = ApplicationBuilder().token('867893257:AAH3rmAkppqD69XdI4G3Fj8sK7Z7GA0BY5g').build()
    job_queue = application.job_queue

    start_handler = CommandHandler('start', start)
    qwack_Dio_handler = MessageHandler(filters.Regex(re.compile(r'.*[D|d][I|i][O|o].*', re.IGNORECASE)), qwack)
    qwack_Madonna_handler = MessageHandler(filters.Regex(re.compile(r'.*[M|a]donna.*', re.IGNORECASE)), qwack)
    qwack_Gesu_handler = MessageHandler(filters.Regex(re.compile(r'.*[G|g]es[u|ú|ù].*', re.IGNORECASE)), qwack)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(qwack_Dio_handler)
    application.add_handler(qwack_Madonna_handler)
    application.add_handler(qwack_Gesu_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler)
    job_queue.run_repeating(del_qwack, interval=60, first=600)

    application.run_polling()
