from dotenv import load_dotenv
import pyttsx3 as p
import speech_recognition as sr
import datetime as dt
import pyowm as OWM
import webbrowser as wb
import os
import smtplib as smtp
import getpass
import time
import wikipedia

load_dotenv()

sound = p.init('sapi5')
voices = sound.getProperty('voices')

reminders = []

def command():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak please.")
        mic.pause_threshold = 1
        audio = mic.listen(source)

    try:
        print("Processing your words.")
        question = mic.recognize_google(audio, language='en-in')
        print(f"Your words: {question}\n")
    except Exception:
        print("Didn't process. Repeat please.")
        speak("Repeat. I couldn't get it.")
        return "none"
    return question

def speak(audio):
    sound.say(audio)
    sound.runAndWait()

def setup():
    print("Running initial setup.")
    speak("Welcome to MyBot setup! State your name.")
    while True:
        user_name = input()
        if user_name != "none":
            break

    speak("These are the available voices.")
    print("\nAvailable voices:")
    for index, voice in enumerate(voices):
        print(f"{index + 1}. {voice.name} ({voice.languages})")
        speak(f"Voice number {index + 1}. {voice.name} ({voice.languages})")

    speak("Mention the number of the voice you want.")
    while True:
        voice_choice = input()
        if voice_choice.isdigit():
            choice = int(voice_choice)
            if 1 <= choice <= len(voices):
                sound.setProperty('voice', voices[choice - 1].id)
                break
            else:
                speak("Invalid number. Please try again.")
        else:
            speak("Please say a valid number.")

    speak(f"Thanks {user_name}. Setup complete.")
    return user_name

def greeting(name):
    hour = int(dt.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    elif hour >= 18 and hour < 22:
        speak("Good Evening")
    else:
        speak("Good Night!")
    speak(f"Hello {name}, I am MyBot, your personal voice assistant. Speak thy wish.")

def send_email():
    sender_email = input("Enter your email: ")
    sender_password = getpass.getpass("Enter your password (app password): ")
    speak("To whom do you want to send the email?")
    recipient = input("Enter recipient email: ")
    speak("What should be the subject?")
    subject = command()
    speak("Please dictate the body of the email.")
    body = command()

    try:
        msg = smtp.SMTP('smtp.gmail.com', 587)
        msg.ehlo()
        msg.starttls()
        msg.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{body}"
        msg.sendmail(sender_email, recipient, message)
        msg.quit()
        speak("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        speak("Sorry, I couldn't send the email.")

def get_weather(city):
    owm = OWM.OWM(os.getenv("OWM_API_KEY"))
    weather_manager = owm.weather_manager()
    observation = weather_manager.weather_at_place(city)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    status = w.status
    speak(f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius.")

def check_reminders():
    now = dt.datetime.now().strftime("%H:%M")
    for reminder in reminders:
        if reminder["time"] == now and not reminder["notified"]:
            speak(f"Reminder: {reminder['task']}")
            reminder["notified"] = True

def set_reminder():
    speak("What should I remind you?")
    task = command()
    speak("At what time? Please say in HH:MM format.")
    time_str = command()
    reminders.append({"task": task, "time": time_str, "notified": False})
    speak(f"Reminder set for {time_str} to {task}")

def control_smart_home(question):
    devices = ["light", "fan", "ac"]
    for device in devices:
        if device in question:
            if "on" in question:
                speak(f"Turning on the {device}.")
                return
            elif "off" in question:
                speak(f"Turning off the {device}.")
                return
    speak("Couldn't recognize the command.")

def answer_general_question(query):
    speak("Searching on Wikipedia.")
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except Exception as e:
        speak("Didn't find anything about it on Wikipedia.")

if __name__ == "__main__":
    user_name = setup()
    greeting(user_name)

    while True:
        question = command().lower()

        if 'hello' in question:
            speak(f'Hello {user_name}, how can I assist you?')

        elif 'open youtube' in question:
            wb.open("https://www.youtube.com")

        elif 'open google' in question:
            wb.open("https://www.google.com")

        elif 'play song' in question:
            sound_dir = "E:\Songs"
            song = [file for file in os.listdir(sound_dir) if file.lower().endswith('.mp3')]
            if song:
                print(f"Playing: {song[0]}")
                os.startfile(os.path.join(sound_dir, song[0]))
            else:
                speak("No MP3 files found in the specified directory.")

        elif 'get time' in question:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'get date' in question:
            strDate = dt.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {strDate}")

        elif "email" in question:
            send_email()

        elif "weather" in question:
            speak("Sure, which city would you like to check the weather for?")
            city = command()
            if city != "none":
                get_weather(city)

        elif "remind me" in question or "set reminder" in question:
            set_reminder()

        elif "turn on" in question or "turn off" in question:
            control_smart_home(question)

        elif "what is" in question or "who is" in question or "tell me about" in question:
            answer_general_question(question)

        elif "exit" in question or "bye" in question:
            speak("Goodbye.")
            quit()
