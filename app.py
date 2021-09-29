import re
import telegram
from telegram.ext.filters import Filters
import speech_recognition as sr
#import ftransc.core as fr
from flask import Flask, request, session , copy_current_request_context
from telebot.credentials import bot_token, bot_user_name,URL
#from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import asyncio
#from websockets import serve
import websockets
import signal
import os

global bot
global TOKEN


TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

async_mode= None

my_bot  = ChatBot(
    'Ayobol',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
    'chatterbot.logic.MathematicalEvaluation',
    'chatterbot.logic.BestMatch'
    ],
    database_uri=None,
)

small_talk = ['bawo ni?',
    'enle o!',
    'Eka ro?',
    'Eka san',
    'Bawo ni nibe yen o',
    "Pẹlẹ o ", " Bawo ni o se wa?", " Pẹlẹ o bawo ni ", " Bawo ni nibe yen o ", " kilode ",
    "omo odun melo ni e?", " nigba wo ni ojo ibi re?", " Nigbawo ni wọn bi ọ?",
    "Mo wa ni gbogbo ọsẹ ", " mi o ni eto kankan ", " n ko lowo loni ",
    'Bawo ni o ṣe n ṣe',
    'Bawo ni nibe yen o',
    'mo wa dada',
    'o dara o ṣeun.',
    'inu mi dun ati ba e soro',
    'kini mole shey fun e',
    'bami ki ile o',
    'eyaaa pele omo mi',
    'ki ni oruko e?',
    'ayobol ni oruko mi .mo ma ran e lowo pelu ile e']
commands1 = ['pa fan', "mo ti tan fan " ,
        'moti pa fan yen',"fan ti wa ni pipade", "mo to pa fan"]
age= ["omo odun melo ni e?",  " nigba wo ni ojo ibi re?", " Nigbawo ni wọn bi ọ?", "omo odun merinlelogun ni mi", " A bi mi ni ọdun 1996", "Ọjọ -ibi mi jẹ Oṣu Keje Ọjọ 3 ati pe a bi mi ni ọdun 1996", "03/07/1996"]

goodbye  = [
" o dabọ ","ki ile o", 'ka sun re', " ri ọ ", " titi a o tun pade ", "nigbamii","O dara lati ba ọ sọrọ ", " Ma a ri e laipe ", " Sọ laipẹ!"
]
commands2 = ['tan ino',
        'ino ti tan', "ina ti tan ", "mo ti pa ina naa", " ololufẹ naa wa ni titan "]




list_trainer = ListTrainer(my_bot)
for item in (small_talk, commands1,commands2, age, goodbye):
    list_trainer.train(item)


def ai(msg):
    res = my_bot.get_response(msg)
    
    if 'pa ino' in msg:
        return {'response': res, 'command' :"{'state':false, 'component':25}"}
    elif 'tan ino' in msg:
        return {'response': res, 'command' :"{'state':true, 'component':25}"}
    elif 'pa fan' in msg:
        return {'response': res, 'command' :"{'state':false, 'component':26}"}
    elif 'tan fan' in msg:
        return {'response': res, 'command' :"{'state':true, 'component':26}"}
    elif 'pa ilekun' in msg:
        return {'response': res, 'command' : "{'state':false, 'component':27}"}
    elif 'si ilekun' in msg:
        return {'response': res, 'command' : "{'state':true, 'component':27}"}

    return {'response': res, 'command' : 0}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    global sender
    sender ='ok'
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = f'Pele o , oruko mini {bot_user_name},'
        # send the welcoming message
        update.message.reply_text(f'kabo {update.effective_user.first_name}'+ bot_welcome)
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    elif update.message.voice :
        duration = update.message.voice.duration
        print('transcribe_voice.Message duration '+ duration)

        #fetch the voice from message

        voice = bot.getFile(update.message.voice.file_id)
        voice.download('file.wav')
        #fr.transcode(voice.download('file.ogg'), 'wav')
        r = sr.Recognizer()

        with sr.WavFile('file.wav') as source :
            audio = r.record(source)

            try: 
                txt = r.recognize_google(audio) 
                #txt =  my_bot.get_response(txt)
            except sr.UnknownValueError as e:
                print(f'Speech to Text Service could not generate request {e}')
            
            update.message.reply_text(txt)
    else:
        try:
            # clear shitty texts for ai
            text = re.sub(r"\W", "_", text) 
            ola  = ai(text)
           # print(ola)
            command = ola['command']
            if command != 0:
                #send message
                sender = ola['command']
                
            update.message.reply_text(ola['response'].text)
        except Exception:
    
            update.message.reply_text(ola['response'].text)

    return 'ok'


 




@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook(f'{URL}{TOKEN}')
   if s:
       return "webhook setup ok"
   else:
       
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'



async def echo(websocket, path):
    while True:
        #can only emit string
        await websocket.send(sender)
        await asyncio.sleep(1)

        #broadcast message to telegram
     #   async for message in websocket:

       #     await websocket.send()

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        echo,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop


