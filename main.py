
from alexa import Alexa



def main():
   
    time_now = Alexa.get_time_of_day()
    Alexa.speak(f"Good {time_now} ,Aya ",'en')
    Alexa.speak("how can i help you today",'en')

    while True:
        audio = Alexa.record_audio()
        command = Alexa.recognize_speech(audio)
        response = Alexa.process_commands(command)
        Alexa.speak("What else can i help you with",'en')
       
        


if __name__ == "__main__":
    main()