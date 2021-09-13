import re
import telegram
from telegram.ext.filters import Filters
import speech_recognition as sr
#import ftransc.core as fr
from flask import Flask, request, session , copy_current_request_context
from telebot.credentials import bot_token, bot_user_name,URL
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
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
    database_uri='sqlite:///db.sqlite3'
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
    
    if 'ino' in msg:
        return {'response': res, 'command' :1}
    if 'fan' in msg:
        return {'response': res, 'command' :2}
    if 'ilekun' in msg:
        return {'response': res, 'command' :3}

    return {'response': res, 'command' : 0}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
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
        bot_welcome = f'Chatbot ayobol niyi,{update.effective_user.first_name}'
        # send the welcoming message
        update.message.reply_text(f'Hello {update.effective_user.first_name}'+ bot_welcome)
        #bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    elif Filters.voice :
        duration = update.message.voice.duration
        print('transcribe_voice.Message duration '+ duration)

        #fetch the voice from message

        voice = bot.getFile(update.message.voice.file_id)
    
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
            command = ola['command']
            if command > 0:
                emit('my_response', {'data': command })
            update.message.reply_text(ola['response'])
        except Exception:
    
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

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



@socket_.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)








