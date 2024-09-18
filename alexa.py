import webbrowser
import os
from playsound import playsound
from gtts import gTTS # to convert text to audio speech
import threading
import random
import speech_recognition as sr
import pyaudio
from datetime import datetime
from googletrans import Translator
import time
import pygame
import pyautogui 
import pywhatkit as kit
import pyjokes

main_lang='en'
class voice_assistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()  
        self.translator = Translator()
        

    #Captures audio from the microphone.
    def record_audio(self):
        with sr.Microphone() as mic:
            print("Listening to the speaker...")
            self.recognizer.adjust_for_ambient_noise(mic, duration=1)  # Pass 'mic' as the source
            audio = self.recognizer.listen(mic)
        return audio
    
    #Converts audio to text.
    def recognize_speech(self,audio):
        try:
            text=self.recognizer.recognize_google(audio,language="en-US")
            print(f"you said: {text}")
            return text
        except sr.UnknownValueError:
            sr_error ="Sorry, I didn't catch that."
            print(sr_error)
            return sr_error
        except sr.RequestError:
            sr_error ="Sorry, there's an issue with the speech recognition service."
            print(sr_error)
            return sr_error
           
        
    
    # Converts text responses to speech.
    def speak(self,play_audio,target_lang):     
        try:
            tts = gTTS(text=play_audio, lang=target_lang)
            filename = "response.mp3"
            tts.save(filename)
    
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()
            os.remove(filename)
        except AssertionError:
            speak_error ="the speaker ended his speech"
            print(speak_error)
            return 
        except ValueError:
            speak_error ="Sorry, the spoken language is not supported."
            print(speak_error)
            return speak_error
        except RuntimeError:
            speak_error ="Sorry, there's an error in the language dictionary."
            print(speak_error)
            return speak_error



    #searching for specific words
    def search_for_word(self, keywords, text):
     for keyword in keywords:
        if keyword in text:
            return True
     return False


    #Interprets and acts on the text command.
    def process_commands(self,command):
        command = command.lower()  # This makes the function case-insensitive.
        if self.search_for_word(["info","personal detail","information"],command):
            self.self_introduction()
        elif self.search_for_word(["translate","change language","language","languages"],command):
            self.translate(command)
        elif self.search_for_word(["time","watch","clock"],command):
            self.time_now()
        elif self.search_for_word(["date","day","week","month","calender"],command):
            self.date_today()
        elif self.search_for_word(["open browser","tab","browser","new tab","google"],command):
            self.open_browser()
        elif self.search_for_word(["search","search in google"],command):
            self.search(command)
        elif self.search_for_word(["message","whatsapp","open whatsapp"],command):
            self.open(command)
        elif self.search_for_word(["youtube","open youtube"],command):
            self.open_youtube()
        elif self.search_for_word(["github","open github"],command):
            self.open_github
        elif self.search_for_word(["chatgpt","open chatgpt","chat gpt"],command):
            self.open_chatgpt
        elif self.search_for_word(["open mail","mail","email","send mail","new mail"],command):
            self.open(command)   
        elif self.search_for_word(["tell me a joke","joke","iam sad","unhappy","lighten me up"],command):
            self.tell_ajoke() 
        elif self.search_for_word(["song","spotify","open spotify"],command):
            self.open(command)
        elif self.search_for_word(["cmd","command prompt","open cmd","open command prompt","terminal"],command):
            self.open(command)
        elif self.search_for_word(["screenshot","take a screenshot","capture","save the screen"],command):
            self.screenshot()
        elif self.search_for_word(["weather","tell me the weather","weather today","climate"],command):
            self.weather()
        elif self.search_for_word(["file","open file","create file"],command):
            self.file()
        elif self.search_for_word(["bye","close","exit"],command):
            self.exit_programme()
    

    def self_introduction(self):
        self.speak("your name is Aya Ashraf , your age is 22 , you live in cairo , egypt",main_lang)
        

    def get_time_of_day(self):
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "morning"
        elif 12 <= current_hour < 17:
            return "afternoon"
        elif 17 <= current_hour < 21:
            return "evening"
        else:
            return "night"
        
    def time_now(self):
        current_time = datetime.now()
        time_array = [current_time.hour, current_time.minute, current_time.second]
        if time_array[0] == 0:
            time_array[0] = 12
            time_message = f"It's midnight, {time_array[1]} minutes and {time_array[2]} seconds."
        elif time_array[0] < 12:
            time_message = f"It's {time_array[0]} o'clock, {time_array[1]} minutes and {time_array[2]} seconds in the morning."
        elif time_array[0] == 12:
            time_message = f"It's noon, {time_array[1]} minutes and {time_array[2]} seconds."
        else:
            time_array[0] -= 12
            time_message = f"It's {time_array[0]} o'clock, {time_array[1]} minutes and {time_array[2]} seconds in the afternoon."
        
        self.speak(time_message, main_lang)

    def date_today(self):
        current_date = datetime.now().date()
        date_message = f"Today's date is {current_date.day} {current_date.strftime('%B')} {current_date.year}." 
        self.speak(date_message, main_lang)

    def translate(self,text):
        self.speak("what's your target language?",main_lang)
        audio = Alexa.record_audio()
        target_lang= self.recognize_speech(audio)
        target_lang = target_lang.lower()

        # Determine language code
        if self.search_for_word(["french"],target_lang):
            lang='fr'
        elif self.search_for_word(["spanish"],target_lang):
            lang='es'
        elif self.search_for_word(["arabic"],target_lang):
            lang='ar'
        elif self.search_for_word(["german"],target_lang):
            lang='de'
        else:
            self.speak("Sorry, I don't support that language.", main_lang)
            return
        
        # Ask for text to translate
        self.speak("what's the text you wanna translate",main_lang)
        audio = Alexa.record_audio()
        translate_text= self.recognize_speech(audio)
        translate_text = translate_text.lower()
        try:
            # Perform translation
            translated = self.translator.translate(translate_text, dest=lang)
            translated_text = translated.text
            self.speak(translated_text, lang)
        except Exception as e:
            print(f"Translation failed: {e}")
            return "Sorry, I couldn't translate the text."

    def exit_programme(self):
        self.speak("bye bye aya , Have a nice day",main_lang)
        exit()

    def open(self,text):
        # Minimize all windows
        pyautogui.hotkey('win', 'd')
        time.sleep(2)
        pyautogui.hotkey('win')
        time.sleep(2)
        if self.search_for_word(["email"],text):
            open_word = 'email'
        elif self.search_for_word(["spotify"],text):
            open_word = 'spotify'
        elif self.search_for_word(["whatsapp"],text):
            open_word = 'whatsapp'
        elif self.search_for_word(["terminal","cmd","command prompt"],text):
            open_word = 'cmd'
        pyautogui.typewrite(open_word)
        time.sleep(2)
        pyautogui.moveTo(600,350)
        pyautogui.click(clicks=2,duration=1)
        # Give it some time to open
        time.sleep(5)
        # Maximize the window using hotkey
        pyautogui.hotkey('win', 'up')

    
    def open_browser(self):
        webbrowser.open_new("https://www.google.com/")

    def open_youtube(self):
        webbrowser.open_new("https://www.youtube.com/")
    
    def open_github(self):
        webbrowser.open_new("https://www.github.com/")
    
    def open_chatgpt(self):
        webbrowser.open_new("https://www.chatgpt.com/")

    def screenshot(self):
        pyautogui.hotkey('win','prtscr')
        self.speak("the screenshot is taken",main_lang)
    
    def search(self,query):
        kit.search(query)
        
    def weather(self):
        self.speak("Which city would you like to check the weather for?",main_lang)
        audio = Alexa.record_audio()
        city= self.recognize_speech(audio)
        query = f"weather in {city} today"
        kit.search(query)
        self.speak(f"Showing you the weather in {city}.", main_lang)
        
    def tell_ajoke(self):
        joke= pyjokes.get_joke()
        self.speak(joke, main_lang) 

    def file(self):
        self.speak("do you want to open an existed file or create a new one",main_lang)
        audio = Alexa.record_audio()
        file_action= self.recognize_speech(audio)
        if self.search_for_word(["open","existed","old"],file_action):
            self.open_existed_file()
        elif self.search_for_word(["create","new","open new"],file_action):
            self.create_file()
        else:
            self.speak("sorry couldn't understand you ", main_lang)


    def open_existed_file(self):
         # Ask the user for the file name
        self.speak("Please tell me the name of the file you want to open.", main_lang)
        audio = self.record_audio()
        file_name = self.recognize_speech(audio)
        file_name = file_name.lower().strip()  # Convert to lower case and strip spaces

        # Ask for file extension if needed
        self.speak("Please tell me the file extension, for example, 'txt' or 'pdf'.", main_lang)
        audio = self.record_audio()
        file_extension = self.recognize_speech(audio)
        file_extension = file_extension.lower().strip()
        if self.search_for_word(["text",file_extension]):
            file_extension="txt"
        elif self.search_for_word(["pdf",file_extension]):
            file_extension="pdf"
        # Construct full file name with extension
        full_file_name = f"{file_name}.{file_extension}"

        # Check if the file exists
        if os.path.exists(full_file_name):
            try:
                # Open the file
                os.startfile(full_file_name)
                self.speak(f"Opening {full_file_name}.", main_lang)
            except Exception as e:
                self.speak(f"Sorry, I couldn't open the file. Error: {e}", main_lang)
        else:
            self.speak(f"Sorry, I couldn't find the file {full_file_name}.", main_lang)

    def create_file(self):
         # Ask for the file name
            self.speak("What would you like to name the file?", main_lang)
            file_name_audio = self.record_audio()  # Record file name
            file_name = self.recognize_speech(file_name_audio)

            # Sanitize file name
            file_name = file_name.strip().replace(" ", "_") + ".txt"

            # Ask for the content to write in the file
            self.speak("Please speak the content to write in the file.", main_lang)
            content_audio = self.record_audio()  # Record the speech content
            content = self.recognize_speech(content_audio)

            # Create and write to the file
            with open(file_name, "w") as file:
                file.write(content)

            self.speak(f"The file {file_name} has been created and your speech has been written to it.", main_lang)



Alexa=voice_assistant()

