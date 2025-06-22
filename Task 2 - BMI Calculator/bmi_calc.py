import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import datetime
import matplotlib.pyplot as plt

DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_data(name, bmi):
    date = str(datetime.date.today())
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        if name not in data:
            data[name] = []
        data[name].append({"date": date, "bmi": bmi})
        f.seek(0)
        json.dump(data, f, indent=4)

def show_graph(name):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    if name not in data:
        messagebox.showerror("Error", "No data found for this user.")
        return
    dates = [entry["date"] for entry in data[name]]
    bmis = [entry["bmi"] for entry in data[name]]

    plt.figure(figsize=(6, 4))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='blue')
    plt.title(f"BMI Trend for {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if not name:
            raise ValueError("Name is required.")
        if not (30 < weight < 300) or not (1.0 < height < 2.5):
            raise ValueError("Please enter realistic values.")

        bmi = round(weight / (height ** 2), 2)
        category = categorize_bmi(bmi)
        result_label.config(text=f"BMI: {bmi} ({category})")

        save_data(name, bmi)

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

root = tk.Tk()
root.title("BMI Calculator")

root.geometry("350x300")
root.resizable(False, False)

tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Height (m):").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Weight (kg):").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)
tk.Button(root, text="Show Graph", command=lambda: show_graph(name_entry.get().strip())).pack()

result_label = tk.Label(root, text="", font=('Arial', 12), fg='green')
result_label.pack(pady=10)

root.mainloop()
