from email import message
from logging import exception
from tokenize import Special
from neuralintents import GenericAssistant
from textblob import TextBlob
import requests, json, os, speech_recognition, pyttsx3, sys
from pygments import highlight, lexers, formatters

recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 100)

def greetings():
    global recognizer

    done = False

    while done != True:
        try:
            lines = []
            with open('encounters.txt') as f:
                lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
            if count == 0:
                speaker.say("Hello, my name is Paul. How may I assist you?")
                speaker.runAndWait
                done = True
            elif count >= 1 and count <= 5:
                speaker.say("Hello Johnny, hope you're doing well today?")
                speaker.runAndWait
                done = True
            else:
                speaker.say("Hello")
                speaker.runAndWait
                done = True
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            
def goodbyes():
    encounter = open("encounters.txt", "a")  # append mode
    encounter.write("* \n")
    encounter.close()
    speaker.say("Goodbye")
    speaker.runAndWait()
    sys.exit(0)

#def music():
#    playlist = str(input("Please choose a playlist: "))
#    Instance = vlc.Instance()
#    player = Instance.media_player_new()
#    Media = Instance.media_new(playlist.lower())
#    Media.get_mrl()
#    player.set_media(Media)
#    player.play()
    
def weather():
    response_API = requests.get('http://dataservice.accuweather.com/currentconditions/v1/333373?apikey=TxVfyVdvwGHc7vuwSrzdehvYnpUfESJi')
    data = response_API.text
    parse_json = json.dumps(json.loads(data), indent=4)
    active_case = highlight(parse_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(active_case)
    
def dates():
    date = os.system('date')
    print(date)
    
def todo_add():
    a = str(input("What would you like to add to the list"))
    todo = open("todo.txt", "a")
    todo.write(f"* {a} \n")
    todo.close()
    
def todo_remove():
    search = input("keyword?")
    try:
        with open('todo.txt', 'r') as fr:
            lines = fr.readlines()
            with open('todo1.txt', 'w') as fw:
                for line in lines:
                    if line.find(search) == -1:
                        fw.write(line)
        print("Deleted")
        os.replace("todo1.txt", "todo.txt")
    except:
        print("Oops! something error")

def show_todo():
    lines = []
    print("Items are in the order they were added.")
    print("Here's what needs to be done...")
    with open('todo.txt') as f:
        lines = f.readlines()
    for line in lines:
        print(line)
        
def spellcheck():
    a = str(input("What word would do you need help with? "))          
    b = TextBlob(a)
    print(str(b.correct()))
    
def feelings():
    os.system("stacer")
    
# future mappings , 'music' : music
        
mappings = {'greeting' : greetings, 'weather' : weather, 'goodbye' : goodbyes, 'date' : dates, 'todo_add' : todo_add, 'todo_remove' : todo_remove, 'todo' : show_todo, 'spellcheck' : spellcheck, 'feeling' : feelings}

assistant = GenericAssistant('intents.json', intent_methods=mappings ,model_name="test_model")
assistant.train_model()
assistant.save_model()
#assistant.load_model()

while True:
    try:
        greetings()
        with speech_recognition.Microphone as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
            messages = recognizer.recognize_google(audio)
            messages = message.lower()
        assistant.request(messages)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()