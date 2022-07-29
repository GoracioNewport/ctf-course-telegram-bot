import telebot
import time
from mathgenerator import mathgen as mg

bot = telebot.TeleBot("5462291150:AAGyNHY_hq9usWdUfNItub7iqcbBVnOrofE", parse_mode=None)

user_stage = dict()
time_limit = 60

generated_problems = [
    mg.genById(0),
    mg.genById(1),
    mg.genById(2),
    mg.genById(3),
    mg.genById(6),
    mg.genById(8),
    mg.genById(31),
    mg.genById(53),
    mg.genById(90),
    mg.genById(5),
    mg.genById(14),
    mg.genById(62),
    mg.genById(19),
    mg.genById(9),
    mg.genById(10),
    mg.genById(30),
    mg.genById(42),
    ["What is 30th element of the periodic table? [Two letters, uppercase and lowercase", "Zn"],
    ["Are you a robot? [Yes/No]", "Yes"],
    ["How old is Vanya Dolgikh?", "18"],
    ["Do you want to get a flag? [Yes, No]", "Yes"]
]

round_limit = len(generated_problems)

def send_stage(user_id):
    if user_id not in user_stage:
        message = "You need to begin the round first! /round_begin"

    elif (time.time() - user_stage[user_id]['start_time']) > time_limit:
        message = "Time's up! Restart the round by typing /round_begin"
        del user_stage[user_id]

    else:

        cs = user_stage[user_id]['stage']
        
        message, sol = generated_problems[cs]
        if cs == 8 or cs == 12: 
            message += "[Yes/No]"


        user_stage[user_id]['next_answer'] = sol
        user_stage[user_id]['stage'] += 1

    bot.send_message(user_id, message)

@bot.message_handler(commands=['start'])
def send_start(msg):
    bot.reply_to(msg, "Hello. You want a flag, huh?.. Okay, I'll give it to you, but only if you'll manage to solve all of my math problems... In 60 seconds. \nDo /round_begin, when you're ready")

@bot.message_handler(commands=['round_begin'])
def send_round_begin(msg):
    global user_stage
    user_stage[msg.from_user.id] = {
        'start_time': time.time(),
        'stage': 0
    } 

    send_stage(msg.from_user.id)

@bot.message_handler(func=lambda m: True)
def handle_answer(msg):
    user_id = msg.from_user.id
    next_stage = False
    message = ""
    if user_id not in user_stage:
        message = "You need to begin the round first! /round_begin"
 
    elif (time.time() - user_stage[user_id]['start_time']) > time_limit:
        message = "Time's up! Restart the round by typing /round_begin"
        del user_stage[user_id]

    else:
        
        if msg.text != user_stage[user_id]['next_answer']:
            message = "Wrong Answer :( Restart the round by typing /round_begin"
            del user_stage[user_id]

        else:
            message = "Stage №" + str(user_stage[user_id]['stage']) + "/" + str(round_limit) + " completed. Great job!"

            if user_stage[user_id]['stage'] == round_limit:
                message += "\nFINAL CHALLENGE: Reverse a binary tree\n\njk, take the flag, you deserver it. gctf_authorised_math_expert"
                del user_stage[user_id]
            else:
                next_stage = True
    
    bot.send_message(user_id, message)

    if next_stage:
        send_stage(user_id) 

bot.infinity_polling()

