import pyttsx3


if __name__ == '__main__':
    engine = pyttsx3.init()
    engine.say("I will speak this text")
    engine.runAndWait()
    engine.say("Hi Avi")
    engine.runAndWait()
