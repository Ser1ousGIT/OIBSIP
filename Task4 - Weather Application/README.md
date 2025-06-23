# Python Weather App (CLI + GUI)

A fully functional weather application built using **Python** that supports both **Command-Line Interface (CLI)** and **Graphical User Interface (GUI)** modes. This app fetches current weather using **OpenWeatherMap API** and forecasts using **Open-Meteo API**.


# Technical Features

- Get current weather info by city name
- Temperature in Celsius or Fahrenheit
- Next 5-hour forecast (Open-Meteo)
- Next 5-day forecast (Open-Meteo)
- Toggle Dark Mode button in GUI version
- Weather condition icons
- Uses `.env` file for API key management
- Error handling for invalid input or API errors


# Technologies Used

- `requests` – For API calls
- `tkinter` – For GUI interface
- `PIL` (Pillow) – For weather icons
- `dotenv` – For environment variable management
- `OpenWeatherMap` – Current weather data
- `Open-Meteo` – Hourly and daily forecast


# GUI Preview

> ![GUI](GUI_SS.png)


# Requirements

Install dependencies using:

```bash
pip install -r install.txt
```

Change the OWM API key to your own in the .env file.


# Run

```bash
python weather_app.py
```

