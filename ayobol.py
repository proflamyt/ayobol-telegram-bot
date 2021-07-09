from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.ext.filters import Filters
import speech_recognition as sr
import logging
import ftransc.core as fr
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ' , level = logging.INFO  )

def start(bot, context):
    context.message.reply_text(
        "Hello, its ayobol's chatbot, oll"
    )



def hello(bot, update):
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def help(bot,  update):
    update.message.reply_text('Chatbot Ayobol niyi , kilofe shey ? \n'+
    'teh nkan tofe sibi\n'+
    '/start restarts the chatbot' +
    '/help prints this help\n' +
    '/hello triggers the hello'
    )

def transcribe_voice(bot,context):
    duration = context.message.voice.duration
    logger.info('transcribe_voice.Message duration '+ duration)

    #fetch the voice from message

    voice = bot.getFile(context.message.voice.file_id)

    ft.transcode(voice.download('file.ogg'), 'wav')
    r = sr.Recognizer()

    with sr.WavFile('file.wav') as source :
        audio = r.record(source)

        try: 
            txt = r.recognize_google(audio)
            logger.info(txt)
        except sr.UnknownValueError as e:
            logger.warn(f'Speech to Text Service could not generate request {e}')
        
        context.message.reply_text(txt)




updater = Updater('')

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, transcribe_voice))

updater.start_polling()
updater.idle()