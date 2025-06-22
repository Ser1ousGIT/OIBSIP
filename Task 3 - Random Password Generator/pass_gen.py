import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("420x480")
        self.root.resizable(True, True)

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Password Length").pack()
        self.length_var = tk.IntVar(value=12)
        tk.Entry(self.root, textvariable=self.length_var, width=10).pack(pady=5)

        self.include_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Include Letters (a-z, A-Z)", variable=self.include_letters).pack(anchor='w', padx=20)
        tk.Checkbutton(self.root, text="Include Numbers (0-9)", variable=self.include_numbers).pack(anchor='w', padx=20)
        tk.Checkbutton(self.root, text="Include Symbols (!@#$)", variable=self.include_symbols).pack(anchor='w', padx=20)

        tk.Label(self.root, text="Exclude Characters").pack(pady=5)
        self.exclude_entry = tk.Entry(self.root, width=30)
        self.exclude_entry.insert(0, "")
        self.exclude_entry.pack(pady=5)

        tk.Button(self.root, text="Generate Password", command=self.generate_password, bg="#4CAF50", fg="white", width=25).pack(pady=10)
        
        self.password_box = tk.Entry(self.root, font=("Consolas", 14), justify="center", width=30)
        self.password_box.pack(pady=10)

        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, bg="#000000", fg="white", width=25).pack(pady=5)

    def generate_password(self):
        length = self.length_var.get()
        exclude_chars = self.exclude_entry.get()

        if length < 4:
            messagebox.showerror("Error", "Password length should be at least 4.")
            return

        selected_sets = []
        if self.include_letters.get():
            selected_sets.append(string.ascii_letters)
        if self.include_numbers.get():
            selected_sets.append(string.digits)
        if self.include_symbols.get():
            selected_sets.append(string.punctuation)

        if not selected_sets:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        combined_chars = ''.join(set(c for s in selected_sets for c in s if c not in exclude_chars))
        if not combined_chars:
            messagebox.showerror("Error", "All characters were excluded. Cannot generate password.")
            return

        password = []
        for s in selected_sets:
            chars = [c for c in s if c not in exclude_chars]
            if not chars:
                messagebox.showerror("Error", "Excluded characters removed all of one type.")
                return
            password.append(random.choice(chars))

        while len(password) < length:
            password.append(random.choice(combined_chars))

        random.shuffle(password)
        generated = ''.join(password[:length])

        self.password_box.delete(0, tk.END)
        self.password_box.insert(0, generated)

    def copy_to_clipboard(self):
        password = self.password_box.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        else:
            messagebox.showwarning("Empty", "No password to copy.")

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        import os
        os.system("pip install pyperclip")

    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
