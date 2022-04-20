from neuralintents import GenericAssistant
from textblob import TextBlob
import requests, json, os, speech_recognition, pyttsx3, sys, subprocess
from pygments import highlight, lexers, formatters

code-name = "ash"
name = code-name

recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 150)

def get_audio():
    
    with speech_recognition.Microphone(device_index=14) as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        messages = recognizer.recognize_google(audio)
        messages = messages.lower()
    return messages

def greetings():
    lines = []
    with open('encounters.txt') as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            count += 1
        if count == 0:
            speaker.say(f"Hello, my name is {name}. How may I assist you?")
            speaker.runAndWait()
        elif count >= 1 and count <= 5:
            speaker.say("Hello Johnny, hope you're doing well today?")
            speaker.runAndWait()
        else:
            speaker.say("Hello")
            speaker.runAndWait()
            
def goodbyes():
    encounter = open("encounters.txt", "a")  # append mode
    encounter.write("* \n")
    encounter.close()
    speaker.say("Goodbye")
    speaker.runAndWait()
    sys.exit(0)

def your_name():
    speaker.say(f"My name is {name}")
    speaker.runAndWait()

def music():
    global recognizer
    
    done = False
    
    while done != True:
        try:
            speaker.say("Which playlist would you like to listen to?")
            speaker.runAndWait()
            with speech_recognition.Microphone(device_index=14) as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                messages = recognizer.recognize_google(audio)
                messages = messages.lower().replace(" ", "")
            playlist = f"/home/Paul/Music/{messages}"
            media_player = vlc.MediaPlayer()
            media = vlc.Media(playlist)
            media_player.set_media(media)
            media_player.play()
            time.sleep(5)

            a = False

            while a != True:
                b = str(input("please type pause, play, or stop: "))
                if b.lower() == "pause":
                    media_player.pause()
                elif b.lower() == "stop":
                    media_player.stop()
                    a = True
                elif b.lower() == "play":
                    media_player.play()
                else:
                    print("Please choose play, pause, or stop")
        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()
            
def weather():
    global recognizer

    done = False

    while done != True:
        try:
            response_API = requests.get('http://dataservice.accuweather.com/currentconditions/v1/333373?apikey=TxVfyVdvwGHc7vuwSrzdehvYnpUfESJi')
            data = response_API.text
            parse_json = json.dumps(json.loads(data), indent=4)
            active_case = highlight(parse_json, lexers.JsonLexer(), formatters.TerminalFormatter())
            speaker.say("Here is the current weather conditions.")
            speaker.runAndWait()
            print(active_case)
            done = True
        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()
    
def dates():
    global recognizer

    done = False

    while done != True:
        try:
            date = os.system('date')
            speaker.say(date)
            speaker.runAndWait()
        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()

def todo_add():
    global recognizer
    
    done = False
    
    while done != True:
        try:
            speaker.say("What would you like add to the list?")
            speaker.runAndWait()
            with speech_recognition.Microphone(device_index=14) as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                messages = recognizer.recognize_google(audio)
                messages = messages.lower()
            todo = open("todo.txt", "a")
            todo.write(f"* {messages} \n")
            todo.close()
            speaker.say(f"{messages} was added to the list.")
            speaker.runAndWait()
        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()
    
def todo_remove():
    global recognizer
    
    done = False
    
    while done != True:
        try:
            speaker.say("What is a keyword unique to the activity you wish to remove?")
            speaker.runAndWait()
            with speech_recognition.Microphone(device_index=14) as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                messages = recognizer.recognize_google(audio)
                messages = messages.lower()
            try:
                with open('todo.txt', 'r') as fr:
                    lines = fr.readlines()
                    with open('todo1.txt', 'w') as fw:
                        for line in lines:
                            if line.find(messages) == -1:
                                fw.write(line)
                speaker.say("Activity was deleted")
                speaker.runAndWait()
                os.replace("todo1.txt", "todo.txt")
            except:
                speaker.say("Was unable to delete activity")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()
            

def show_todo():
    lines = []
    speaker.say("Items are in the order they were added.")
    speaker.runAndWait()
    speaker.say("Here's what needs to be done...")
    speaker.runAndWait()
    with open('todo.txt') as f:
        lines = f.readlines()
    for line in lines:
        speaker.say(line)
        speaker.runAndWait()
        
def spellcheck():
    global recognizer
    
    done = False
    
    while done != True:
        try:
            speaker.say("What word do you need help with?")
            speaker.runAndWait()
            with speech_recognition.Microphone(device_index=14) as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                messages = recognizer.recognize_google(audio)
                messages = messages.lower()         
            b = TextBlob(messages)
            speaker.say(str(b.correct()))
        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()
    
def feelings():
    speaker.say("As of right now this is what my health looks like.")
    speaker.runAndWait()
    subprocess.Popen("stacer")
    
        
mappings = {'greeting' : greetings, 'weather' : weather, 'goodbye' : goodbyes, 'date' : dates, 'todo_add' : todo_add, 'todo_remove' : todo_remove, 'todo' : show_todo, 'spellcheck' : spellcheck, 'feeling' : feelings, 'music' : music, "name": your_name}

assistant = GenericAssistant('intents.json', intent_methods=mappings ,model_name="test_model")
assistant.train_model()
assistant.save_model()
#assistant.load_model()

WAKE = f"Hey {name}"

while True:
    text = get_audio()
    if text.count(WAKE) > 0:
        try:
            with speech_recognition.Microphone(device_index=14) as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                messages = recognizer.recognize_google(audio)
                messages = messages.lower()
            assistant.request(messages)
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
    else:
        speaker.say("There is an error in my code")
        speaker.runAndWait()
        sys.exit(0)
