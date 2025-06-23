# BMI Calculator with GUI and Data Visualization

A simple Python-based **BMI Calculator** with a GUI using **Tkinter**. This project allows multiple users to:
- Enter height and weight to calculate BMI
- Store historical BMI data
- View BMI trends over time with graphs


# Technical Features

- User-friendly interface using Tkinter
- Accurate BMI calculation using the standard formula
- Automatic categorization into: Underweight, Normal, Overweight, Obese
- Data storage per user in a local `data.json` file
- BMI trend visualization using Matplotlib
- Input validation and error handling
- Lightweight and beginner-friendly code structure


# GUI Preview

> ![GUI](GUI_SS.png)


# **Complete Explanation**

A full explanation of how this project works, including screenshots and use-cases, is posted on LinkedIn.  
👉 https://www.linkedin.com/posts/anandswaroopv_oasisinfobyte-oasisinfobytefamily-internship-activity-7342588316925501440-A1SW?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAEpwJ1kBIUoA6yMGOx-pVGAKQ58bAN7s_fI


# Code Explanation

This project is a simple **BMI Calculator** with a **Tkinter-based GUI** that calculates the user's BMI based on height and weight. It also saves the data locally and can visualize BMI trends over time using graphs.


# Functional Breakdown

| Function/Section         | Description |
|--------------------------|-------------|
| `categorize_bmi(bmi)`    | Categorizes BMI into Underweight, Normal, Overweight, or Obese based on standard thresholds. |
| `save_data(name, bmi)`   | Saves the user's BMI with the current date into a `data.json` file for history tracking. |
| `show_graph(name)`       | Reads historical BMI data for a user and plots a line chart using `matplotlib`. |
| `calculate_bmi()`        | Validates inputs, calculates BMI, categorizes it, displays it, and saves the result. |


# GUI Components

The GUI is built with **Tkinter** and consists of:

- Entry fields for `Name`, `Height (in meters)`, and `Weight (in kg)`
- Buttons to **Calculate BMI** and **Show Graph**
- A label to display the result (BMI value and category)
- Plotting functionality to visualize BMI trends over time

# Data Storage

- All data is stored in a local JSON file named `data.json`.
- Each user's data is stored as a list of BMI entries with date stamps.


# Tools and Libraries Used

| Library         | Purpose |
|-----------------|---------|
| `tkinter`       | GUI framework for building the application window and user interface. |
| `json`          | To read/write user BMI data into a structured local JSON file. |
| `datetime`      | To fetch and store the current date for each BMI entry. |
| `matplotlib`    | To generate and display BMI trend graphs over time. |
| `os`            | To check if `data.json` exists and create it if it doesn't. |
| `tkinter.messagebox` | To show error popups for invalid input or missing data. |


# Requirements

Install dependencies using:

```bash
pip install -r install.txt
```


# Run

```bash
python bmi_calc.py
```

---
