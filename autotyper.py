import tkinter as tk
import pyautogui
import time
import threading
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import keyboard
from tkinter import messagebox
from PIL import Image, ImageTk


class AutoTyper:

    def __init__(self):
        self.is_running = True
        self.is_typing = False
        self.app = tk.Tk()
        self.app.title("Auto Typer")
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame = tk.Frame(self.app)
        self.frame.pack(pady=20, padx=20)
        
        self.build_gui()


    def on_closing(self):
        self.is_running = False
        self.app.destroy()

    def start_typing(self):
        if not self.is_typing:
            self.is_typing = True
            thread = threading.Thread(target=self.auto_type)
            thread.start()

    def stop_typing(self):
        self.is_typing = False

    def auto_type(self):
        text = self.text_input.get("1.0", tk.END)
        start_delay = float(self.start_delay_spinbox.get())
        char_delay = float(self.char_delay_spinbox.get())
        word_delay = float(self.word_delay_spinbox.get())

        self.start_button.config(state=tk.DISABLED)
        print(f"Starting in {start_delay} seconds...")
        time.sleep(start_delay)

        word = ''
        for char in text:
            if not self.is_running or not self.is_typing or keyboard.is_pressed('esc') or keyboard.is_pressed('F10'):
                print("Stopped typing!")
                self.is_typing = False
                break
            
            if char == ' ':
                pyautogui.typewrite(word + ' ', interval=char_delay)
                word = ''
                if word_delay > 0:
                    time.sleep(word_delay)
            else:
                word += char

        if word:
            pyautogui.typewrite(word, interval=char_delay)

        self.start_button.config(state=tk.NORMAL)
        self.is_typing = False

    def build_gui(self):
        frame = tk.Frame(self.app)
        frame.pack(pady=20, padx=20)

        info_label = tk.Label(frame, text="Enter the text below and press the Start button or F9 to begin auto-typing. Press 'Esc' or F10 to stop typing.")
        info_label.pack(pady=10)

        self.text_input = tk.Text(frame, width=50, height=10)
        self.text_input.pack(pady=10)

        start_delay_label = tk.Label(frame, text="Start delay (seconds):")
        start_delay_label.pack(pady=(10, 0))
        self.start_delay_spinbox = tk.Spinbox(frame, from_=0, to=1000, width=5, increment=0.1)
        self.start_delay_spinbox.pack(pady=(0, 10))

        char_delay_label = tk.Label(frame, text="Delay between characters (seconds):")
        char_delay_label.pack(pady=(10, 0))
        self.char_delay_spinbox = tk.Spinbox(frame, from_=0, to=100, width=5, increment=0.1)
        self.char_delay_spinbox.pack(pady=(0, 10))

        word_delay_label = tk.Label(frame, text="Delay after each word (seconds):")
        word_delay_label.pack(pady=(10, 0))
        self.word_delay_spinbox = tk.Spinbox(frame, from_=0, to=100, width=5, increment=0.1)
        self.word_delay_spinbox.pack(pady=(0, 10))

        self.start_button = tk.Button(frame, text="Start Typing", command=self.start_typing)
        self.start_button.pack(pady=10)

        keyboard.add_hotkey('F9', self.start_typing)
        keyboard.add_hotkey('F10', self.stop_typing)
        keyboard.add_hotkey('esc', self.stop_typing)
    def import_text(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx"), ("All Files", "*.*")])
        if file_path:
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_input.delete("1.0", tk.END)  # Clear existing text
                    self.text_input.insert(tk.END, content)
            elif file_path.endswith('.docx'):
                try:
                    from docx import Document
                    doc = Document(file_path)
                    content = '\n'.join([para.text for para in doc.paragraphs])
                    self.text_input.delete("1.0", tk.END)
                    self.text_input.insert(tk.END, content)
                except ImportError:
                    tk.messagebox.showerror("Error", "Please install python-docx to import Word documents.")
            else:
                tk.messagebox.showerror("Error", "Unsupported file type.")

    def export_text(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx"), ("All Files", "*.*")])
        if file_path:
            content = self.text_input.get("1.0", tk.END).strip()
            if file_path.endswith('.txt'):
                with open(file_path, 'w') as file:
                    file.write(content)
            elif file_path.endswith('.docx'):
                try:
                    from docx import Document
                    doc = Document()
                    doc.add_paragraph(content)
                    doc.save(file_path)
                except ImportError:
                    tk.messagebox.showerror("Error", "Please install python-docx to export to Word documents.")
                else:
                    tk.messagebox.showerror("Error", "Unsupported file type.")



    def run(self):
        self.app.mainloop()


