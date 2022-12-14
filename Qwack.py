import logging, re, aiohttp, asyncio
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from collections import namedtuple

#
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# List of images to be deleted
delete_list = []


# System to retrieve random images of ducks
async def random():
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    query = ''
    async with session.get('https://random-d.uk/api/random{}'.format(query)) as r:
        if r.status == 200:
            body = await r.json()
            await session.close()
            response = namedtuple('Response', ['message', 'url'])
            return response(message=body['message'], url=body['url'])
        else:
            raise CouldNotGetDuckError(r.status)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Non servo ad un cazzo, solo coprire le bestemmie")

    
# Main function: delete the message with the blasphemy and send a random photo of ducks
async def qwack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_async = await random()
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Bestemmia rilevata")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=random_async.url)
    delete_list.append(update.message.message_id + 1)

    
# Cleaner function, every certain time (see below) it activates and deletes the photos of the ducks
async def del_qwack(context: ContextTypes.DEFAULT_TYPE):
    if delete_list:
        # -1001283327584 For the "provebot" channel, you need to insert the correct ID for other groups
        await context.bot.delete_message(chat_id='-1001283327584', message_id=delete_list.pop())

        
# Function that I needed to keep, has no bearing on the project, you can ignore it
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

# Unknown command management function, you can ignore it
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


class CouldNotGetDuckError(Exception):
    pass


if __name__ == '__main__':
    # Put your token below
    application = ApplicationBuilder().token('PLACE TOKEN HERE').build()
    # Initialize a job queue
    job_queue = application.job_queue

    # control area
    start_handler = CommandHandler('start', start)
    qwack_Dio_handler = MessageHandler(filters.Regex(re.compile(r'.*[D|d][I|l|i|1|\|][O|o|0].*', re.IGNORECASE)), qwack)
    qwack_Madonna_handler = MessageHandler(filters.Regex(re.compile(r'.*[M|a]donna.*', re.IGNORECASE)), qwack)
    qwack_Gesu_handler = MessageHandler(filters.Regex(re.compile(r'.*[G|g]es[u|??|??].*', re.IGNORECASE)), qwack)
    qwack_Cristo_handler = MessageHandler(filters.Regex(re.compile(r'([C|c][??|r][I|l|i|1|\|]st[O|o|0])', re.IGNORECASE)), qwack)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # handeler contol area
    application.add_handler(start_handler)
    application.add_handler(qwack_Dio_handler)
    application.add_handler(qwack_Madonna_handler)
    application.add_handler(qwack_Gesu_handler)
    application.add_handler(qwack_Cristo_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler)
    # auto-deletion queue trigger timer
    job_queue.run_repeating(del_qwack, interval=300, first=600)

    # job for continuous polling
    application.run_polling()
