done = False

while done != True:
    try:
        with speech_recognition.Microphone as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
            messages = recognizer.recognize_google(audio)
            messages = message.lower()
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()