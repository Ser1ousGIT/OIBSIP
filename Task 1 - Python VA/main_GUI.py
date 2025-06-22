import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3 as p
import speech_recognition as sr
import datetime as dt
import pyowm as OWM
import webbrowser as wb
import os
import smtplib as smtp
import getpass
from dotenv import load_dotenv
import os as sys_os

load_dotenv()

sound = p.init('sapi5')
voices = sound.getProperty('voices')

def gui_log(text):
    if gui_log_area:
        gui_log_area.insert(tk.END, text + "\n")
        gui_log_area.see(tk.END)
    print(text)

def speak(audio):
    gui_log(f"MyBot: {audio}")
    sound.say(audio)
    sound.runAndWait()

def command():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        gui_log("Listening...")
        mic.pause_threshold = 1
        audio = mic.listen(source)

    try:
        gui_log("Recognizing...")
        question = mic.recognize_google(audio, language='en-in')
        gui_log(f"You said: {question}")
    except Exception:
        gui_log("Could not understand.")
        speak("Repeat. I couldn't get it.")
        return "none"
    return question

def setup():
    gui_log("Running setup.")
    speak("Welcome to MyBot setup! Please type your name.")
    user_name = input("Enter your name: ")

    speak("These are the available voices.")
    for index, voice in enumerate(voices):
        gui_log(f"{index + 1}. {voice.name} ({voice.languages})")
        speak(f"Voice number {index + 1}")

    speak("Please type the number of the voice you want.")
    while True:
        voice_choice = input("Choose voice number: ")
        if voice_choice.isdigit():
            choice = int(voice_choice)
            if 1 <= choice <= len(voices):
                sound.setProperty('voice', voices[choice - 1].id)
                break
            else:
                speak("Invalid number. Try again.")
        else:
            speak("Please type a valid number.")

    speak(f"Thanks {user_name}. Setup complete.")
    return user_name

def greeting(name):
    hour = int(dt.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    elif 18 <= hour < 22:
        speak("Good Evening!")
    else:
        speak("Good Night!")
    speak(f"Hello {name}, I am MyBot, your personal assistant. Speak thy wish.")

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
        gui_log(f"Email failed: {e}")
        speak("Sorry, I couldn't send the email.")

def get_weather(city):
    api_key = sys_os.getenv("OWM_API_KEY")
    owm = OWM.OWM(api_key)
    weather_manager = owm.weather_manager()
    observation = weather_manager.weather_at_place(city)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    status = w.status
    speak(f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius.")

def run_assistant():
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
            sound_dir = "E:\\Songs"
            song = [file for file in os.listdir(sound_dir) if file.lower().endswith('.mp3')]
            if song:
                gui_log(f"Playing: {song[0]}")
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
            speak("Which city would you like to check the weather for?")
            city = command()
            if city != "none":
                get_weather(city)

        elif "exit" in question or "bye" in question:
            speak("Goodbye! Have a great day.")
            break

def start_gui():
    global gui_log_area
    root = tk.Tk()
    root.title("MyBot - Voice Assistant")
    root.geometry("600x400")

    tk.Label(root, text="Welcome to MyBot", font=("Arial", 18)).pack(pady=10)

    gui_log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
    gui_log_area.pack(padx=10, pady=10)

    start_btn = tk.Button(root, text="Start Assistant", font=("Arial", 14), bg="#4CAF50", fg="white",
                          command=lambda: threading.Thread(target=run_assistant, daemon=True).start())
    start_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui_log_area = None  
    start_gui()
