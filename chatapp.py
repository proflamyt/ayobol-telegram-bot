from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

execute =True
def training():
     my_bot  = ChatBot(
        'Ayobol',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
            'chatterbot.logic.TimeLogicAdapter',
            'chatterbot.logic.BestMatch'
        ],
        database_uri='sqlite:///database.sqlite3'
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
     execute= False
     return my_bot









def main():
    if execute == True:
        my_bot = training()
    res = chatbot_response('pele o',my_bot)
    print(res)


def chatbot_response(msg, my_bot):
    res = my_bot.get_response(msg)
    
    if 'ino' in msg:
        return {'response': res, 'command' :1}
    if 'fan' in msg:
        return {'response': res, 'command' :2}
    if 'ilekun' in msg:
        return {'response': res, 'command' :3}

    return {'response': res, 'command' : 0}



main()