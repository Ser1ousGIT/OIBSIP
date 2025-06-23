import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def k_to_c(k):    return round(k - 273.15, 2)
def k_to_f(k): return round((k - 273.15) * 9/5 + 32, 2)

def get_forecast(lat, lon):
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": "temperature_2m,weathercode",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto"
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
    return r.json()

def get_weather_data(city):
    try:
        resp = requests.get(BASE_URL, params={"q": city, "appid": API_KEY})
        data = resp.json()
        if data.get("cod") != 200:
            return {"error": data.get("message", "Invalid city")}
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        forecast = get_forecast(lat, lon)

        now_idx = forecast["hourly"]["time"].index(forecast["hourly"]["time"][0])
        hourly = []
        for i in range(1,6):
            t = forecast["hourly"]["time"][now_idx + i]
            temp = forecast["hourly"]["temperature_2m"][now_idx + i]
            code = forecast["hourly"]["weathercode"][now_idx + i]
            hourly.append({"dt": t, "temp": temp, "code": code})

        daily = []
        for i in range(1,6):
            daily.append({
                "dt": forecast["daily"]["time"][i],
                "temp": {"max": forecast["daily"]["temperature_2m_max"][i],
                         "min": forecast["daily"]["temperature_2m_min"][i]},
                "weathercode": forecast["daily"]["weathercode"][i]
            })

        return {
            "city": data["name"],
            "temperature_k": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "hourly": hourly,
            "daily": daily
        }
    except Exception as e:
        return {"error": str(e)}

def run_cli():
    print("== Weather App (CLI) ==")
    city = input("Enter city name: ")
    units = input("Choose units (C/F): ").strip().lower()
    data = get_weather_data(city)
    if "error" in data:
        print("Error:", data["error"])
        return
    def fmt(k):
        return k_to_f(k) if units == "f" else k_to_c(k)
    symbol = "°F" if units == "f" else "°C"
    print(f"\nWeather in {data['city']}:")
    print(f"Temperature: {fmt(data['temperature_k'])}{symbol}")
    print(f"Condition: {data['description']}")
    print(f"Humidity: {data['humidity']}%")
    print(f"Wind Speed: {data['wind_speed']} m/s")

    print("\nNext 5 Hours Forecast:")
    for hr in data["hourly"]:
        dt = datetime.datetime.fromisoformat(hr["dt"]).strftime("%I %p")
        print(f"{dt}: {round(hr['temp'],1)}{symbol}")

    print("\nNext 5 Days Forecast:")
    for day in data["daily"]:
        dt = datetime.datetime.fromisoformat(day["dt"]).strftime("%a %d")
        print(f"{dt}: {round(day['temp']['min'],1)} / {round(day['temp']['max'],1)}{symbol}")

class WeatherAppGUI:
    def __init__(self, root):
        self.root = root; self.root.title("Weather App")
        self.root.geometry("450x600"); self.root.resizable(False, False)
        self.unit = tk.StringVar(value="C")
        self.icon_label = None; self.dark_mode = False
        self.setup_ui()

    def setup_ui(self):
        self.city_label = tk.Label(self.root, text="Enter City:", font=("Arial", 14))
        self.city_label.pack(pady=10)
        self.city_entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.city_entry.pack(pady=5)
        unit_frame = tk.Frame(self.root); unit_frame.pack()
        tk.Label(unit_frame, text="Unit:").pack(side=tk.LEFT)
        tk.Radiobutton(unit_frame, text="Celsius", variable=self.unit, value="C").pack(side=tk.LEFT)
        tk.Radiobutton(unit_frame, text="Fahrenheit", variable=self.unit, value="F").pack(side=tk.LEFT)
        tk.Button(self.root, text="Get Weather", command=self.show_weather).pack(pady=10)
        tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode).pack()
        self.result_frame = tk.Frame(self.root); self.result_frame.pack(pady=10)
        self.weather_text = tk.Label(self.result_frame, font=("Arial", 12), justify="left")
        self.weather_text.pack()
        self.forecast_text = tk.Text(self.root, width=50, height=12, font=("Arial", 10), wrap="word")
        self.forecast_text.pack(pady=10)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = "#1e1e1e" if self.dark_mode else "white"; fg = "white" if self.dark_mode else "black"
        self.root.configure(bg=bg)
        for w in [self.city_label, self.weather_text, self.forecast_text]:
            w.configure(bg=bg, fg=fg)
        self.city_entry.configure(bg="white", fg="black")
        if self.icon_label:
            self.icon_label.configure(bg=bg)

    def show_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Input Error", "Please enter a city name."); return
        data = get_weather_data(city)
        if "error" in data:
            messagebox.showerror("API Error", data["error"]); return

        temp_k = data["temperature_k"]
        if self.unit.get() == "C":
            temp = k_to_c(temp_k); sym = "C"
        else:
            temp = k_to_f(temp_k); sym = "F"

        icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
        img = Image.open(BytesIO(requests.get(icon_url).content))
        photo = ImageTk.PhotoImage(img)
        bg = "#1e1e1e" if self.dark_mode else "white"
        if self.icon_label:
            self.icon_label.config(image=photo, bg=bg)
            self.icon_label.image = photo
        else:
            self.icon_label = tk.Label(self.result_frame, image=photo, bg=bg); self.icon_label.image = photo
            self.icon_label.pack()

        info = (f"City: {data['city']}\n"
                f"Temperature: {temp:.1f}°{sym}\n"
                f"Condition: {data['description']}\n"
                f"Humidity: {data['humidity']}%\n"
                f"Wind Speed: {data['wind_speed']} m/s")
        self.weather_text.config(text=info)

        forecast = "\nNext 5 Hours Forecast:\n"
        for hr in data["hourly"]:
            dt = datetime.datetime.fromisoformat(hr["dt"]).strftime("%I %p")
            forecast += f"{dt}: {round(hr['temp'],1)}°{sym}\n"

        forecast += "\nNext 5 Days Forecast:\n"
        for d in data["daily"]:
            dt = datetime.datetime.fromisoformat(d["dt"]).strftime("%a %d")
            forecast += f"{round(d['temp']['min'],1)}°/{round(d['temp']['max'],1)}°{sym}\n"

        self.forecast_text.delete("1.0", tk.END)
        self.forecast_text.insert(tk.END, forecast)

if __name__ == "__main__":
    print("Choose mode:\n1. CLI\n2. GUI")
    mode = input("Enter 1 or 2: ").strip()
    if mode == "1":
        run_cli()
    elif mode == "2":
        root = tk.Tk()
        app = WeatherAppGUI(root)
        root.mainloop()
    else:
        print("Invalid choice. Exiting...")
