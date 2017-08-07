"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import webbrowser

## A counter is used once as a cookie for the initial name greeting, overcoming the server's statelessness
counter = {'key' : 0}

## Pre-defined words

GREETINGS = ["hello", "sup", "hi", "yo", "what's up", "how YOU doin'", "what's going on"]

SWEAR_USER = ["fuck", "shit", "ass"]
SWEAR_BOT = ["Please refrain from using that kind of language", "I am rubber you are glue", "Sticks and bones etc."]

JOKE_USER = ["joke", "funny", "bored"]
JOKE_BOT = ["How do you fix a wet cellphone? You put it in rice, then a bunch of Chinese come and fix it.", "What is an object-oriented way to become wealthy? Inheritance.", "a SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'"]

CONFUSED_BOT = ["00111111 (that's ? in binary, human)", "DOES NOT COMPUTE", "Try again, but this time, with FEELING"]

CRY_USER = ["you suck", "boring", "quiet", "shut up"]
CRY_BOT = ["That was uncalled for", "Robots have feelings too you know..."]

AFRAID_USER = ["water", "infinite loop", "Michal Tsafir"]
AFRAID_BOT = ["Yipyipyipyipyip!!!!", "MERCY!", "You win!"]

EXCITED_USER = ["Python", "Bottle", "Server", "Back-end"]
EXCITED_BOT = ["OMGOMGOMGOMGOMG!!!!", "Sooooo cool!", "Love it"]

BORED_USER = ["HTML", "CSS", "JS", "Front-end"]
BORED_BOT = ["mmhmm...", "a ha...", "fascinating...", "ZZZzzz"]

YES_USER = ["yes", "affermative", "positive", "confirm", "yup", "yep"]
YES_BOT = ["But like same though, but let's talk about something else now.","I feel the exact same way! Ask me to do something cool."]

QUESTION_BOT = ["The answer is 42", "What do I know, I'm just a chat bot", "...maybe?", "I wanna say... yes? no?", "Go fish"]

@route('/', method='GET')
def index():
    return template("chatbot.html")

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    ## Counter is used once outside of the main input check function
    if counter['key'] == 0:
        counter['key'] += 1
        return json.dumps({"animation": "inlove", "msg": "Hello " + user_message + ", nice to meet you!"})
    ## The input is handled in a single function, which returns an appropriate animation + message from the pre-defined words
    bot_response = inputCheck(user_message)
    return json.dumps(bot_response)

def inputCheck(input):
    ## The fuunction calls another function to validate its IF conditions
    if wordsCheck(GREETINGS, input):
        return {"animation": "dancing", "msg": random.choice(GREETINGS)}
    if wordsCheck(SWEAR_USER, input):
        return {"animation": "no", "msg": random.choice(SWEAR_BOT)}
    if wordsCheck(JOKE_USER, input):
        return {"animation": "laughing", "msg": random.choice(JOKE_BOT)}
    if wordsCheck(CRY_USER, input):
        return {"animation": "crying", "msg": random.choice(CRY_BOT)}
    if wordsCheck(AFRAID_USER, input):
        return {"animation": "afraid", "msg": random.choice(AFRAID_BOT)}
    if wordsCheck(BORED_USER, input):
        return {"animation": "bored", "msg": random.choice(BORED_BOT)}
    if wordsCheck(EXCITED_USER, input):
        return {"animation": "excited", "msg": random.choice(EXCITED_BOT)}
    if wordsCheck(YES_USER, input):
        return {"animation": "ok", "msg": random.choice(YES_BOT)}
    if "dog" in input:
        return ({"animation": "dog", "msg": webbrowser.open("https://www.youtube.com/watch?v=swmuqGWgZCc")})
    if "?" in input:
        return {"animation": "waiting", "msg": random.choice(QUESTION_BOT)}
    else:
        return {"animation": "confused", "msg": random.choice(CONFUSED_BOT)}

def wordsCheck(WORDS, input):
    for word in WORDS:
        if word in input:
            return True

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})

@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')

@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')

@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()