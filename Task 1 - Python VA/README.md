# MyBot - AI Voice Assistant in Python

This is the first project for my OIBSIP internship in Python Programming. "Task 1"; an advanced Voice Assistant in Python. 
---
MyBot is a personal voice assistant built using Python.
It leverages speech recognition to perform various tasks such as checking the weather, sending emails, setting reminders, controlling smart devices (simulated), and answering general knowledge questions via Wikipedia.


# Technical Features

- **Voice Interaction** using `speech_recognition` and `pyttsx3`
- **Initial Setup** for user name and preferred voice
- **Open Websites** like Google and YouTube via voice commands
- **Play Local Music** stored on your computer
- **Get Current Date and Time**
- **Get Weather Updates** using the OpenWeatherMap API
- **Send Emails** via Gmail SMTP
- **Set Voice-Based Reminders**
- **Simulated Smart Home Device Control**
- **Ask General Knowledge Questions** via Wikipedia


# **Complete Explanation**

A full breakdown and explanation of this project has been shared on LinkedIn.  
👉 [View Full Explanation on LinkedIn]([https://www.linkedin.com/in/your-profile-placeholder](https://www.linkedin.com/posts/anandswaroopv_oasisinfobyte-oasisinfobytefamily-internship-activity-7342568522029432833-KADo?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAEpwJ1kBIUoA6yMGOx-pVGAKQ58bAN7s_fI))


# Code Explanation

This voice assistant project is modularly structured and performs various automation tasks using Python libraries:


# Function Overview

| Function Name              | Description |
|---------------------------|-------------|
| `setup()`                 | Runs the first-time configuration: asks user name and allows voice selection from system voices. |
| `command()`               | Uses microphone input and Google’s API to convert speech to text. |
| `speak(audio)`            | Converts text to speech using `pyttsx3`. Used for assistant responses. |
| `send_email()`            | Prompts user for recipient, subject, and message. Sends email via Gmail SMTP using app password. |
| `get_weather(city)`       | Fetches real-time weather using OpenWeatherMap API and reads out temperature and status. |
| `check_reminders()`       | Continuously checks the current time against stored reminders and speaks them when due. |
| `set_reminder()`          | Allows users to schedule task reminders via voice. |
| `control_smart_home()`    | Simulates turning appliances on/off (e.g., light, fan, AC) based on keywords. |
| `answer_general_question()` | Performs a Wikipedia search and reads a 2-line summary of the topic. |


# Main Execution Flow

Once the app starts:
1. `setup()` initializes user profile.
2. `greeting(name)` welcomes user based on time of day.
3. An infinite loop listens for commands and matches keywords to trigger the corresponding function.


# Tools and Libraries Used

| Tool/Library          | Purpose |
|-----------------------|---------|
| `speech_recognition`  | Converts user speech to text via Google Speech API. |
| `pyttsx3`             | Text-to-speech engine for speaking responses. |
| `pyowm`               | Fetches weather data from OpenWeatherMap. |
| `wikipedia`           | Grabs summary info from Wikipedia for general queries. |
| `smtplib`             | Sends emails using Gmail SMTP server. |
| `dotenv`              | Loads API keys securely from `.env` file. |
| `datetime`            | Gets current time/date for greetings and reminders. |
| `webbrowser`          | Opens popular sites like YouTube and Google. |


# Requirements

Install dependencies using:

```bash
pip install -r install.txt
```

Change the OWM API key to your own in the .env file.


# Run

```bash
python main.py
```






---

