import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import queue
import google.generativeai as palm
import speech_recognition as sr
import pyttsx3
import os
import pywhatkit
import sys
from dotenv import load_dotenv
import tkinter.font as tkFont

load_dotenv()

PALM_API_KEY = os.getenv("PALM_API_KEY")
palm.configure(api_key=PALM_API_KEY)

class VoiceAssistantApp:
    def __init__(self, master):
        self.window = master
        self.window.title("Voice Assistant")
        self.window.geometry("800x600")

        style = ttk.Style()
        style.theme_use("clam")


        self.window.configure(bg="#f0f0f0")

        self.chat_box = scrolledtext.ScrolledText(master, width=80, height=30, state=tk.DISABLED, bg="#e0e0e0")
        self.chat_box.pack(pady=10)

 
        button_font = tkFont.Font(family="Arial", size=10, weight="bold")
        self.start_button = tk.Button(master, text="Start", command=self.start_listening, bg="#4caf50", fg="white", width=15, height=2)
        self.start_button["font"] = button_font
        self.start_button.pack(side=tk.LEFT, padx=100)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_listening, state=tk.DISABLED, bg="#d32f2f", fg="white", width=15, height=2)
        self.stop_button["font"] = button_font
        self.stop_button.pack(side=tk.RIGHT, padx=100)

        self.response = None
        self.listening_thread = None
        self.stop_event = threading.Event()
        self.tts_queue = queue.Queue()

        self.window.protocol("WM_DELETE_WINDOW", self.stop_listening_on_close)

    def start_listening(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.stop_event.clear()
        self.listening_thread = threading.Thread(target=self.listen_and_reply)
        self.listening_thread.start()
        self.window.after(100, self.check_tts_queue)

    def stop_listening(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.stop_event.set()
        self.window.after(100, self.check_thread_alive)  

    def check_thread_alive(self):
        if self.listening_thread and self.listening_thread.is_alive():
            self.window.after(100, self.check_thread_alive)
        else:
            self.listening_thread = None

    def listen_and_reply(self):
        self.response = palm.chat(messages="Hi")
        self.append_to_chat("AI: " + str(self.response.last))
        self.tts_queue.put(self.response.last)
        while not self.stop_event.is_set():
            query = self.get_voice_input()
            if query:
                if "exit" in query.lower():
                    self.stop_listening_on_close()
                    return
                self.response = self.response.reply(query)
                if self.response:
                    self.append_to_chat("User: " + query)
                    self.append_to_chat("AI: " + str(self.response.last))
                    self.tts_queue.put(self.response.last)
                else:
                    self.tts_queue.put("AI did not provide a valid response.")

    def check_tts_queue(self):
        try:
            text = self.tts_queue.get_nowait()
            self.speak(text)
        except queue.Empty:
            pass
        if not self.stop_event.is_set():
            self.window.after(100, self.check_tts_queue)

    def speak(self, text, voice_id=1):
        if self.stop_event.is_set():
            return
        engine = pyttsx3.init()
        if voice_id:
            voices = engine.getProperty("voices")
            if 0 <= voice_id < len(voices):
                engine.setProperty("voice", voices[voice_id].id)
            else:
                print(f"Voice ID {voice_id} is not valid. Using the default voice.")
        engine.say(text)
        engine.runAndWait()

    def get_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.append_to_chat("Listening...")
            audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            self.append_to_chat("User said: " + query)
            if "exit" in query.lower():
                self.stop_listening_on_close()
                return None
            elif "play" in query.lower():
                query = query.replace("play", "")
                pywhatkit.playonyt(query)
                return ""
            return query
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Can you please repeat?")
            return ""
        except sr.RequestError as e:
            self.append_to_chat(f"Error with the speech recognition service; {e}")
            return ""

    def append_to_chat(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, message + "\n")
        self.chat_box.yview(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    def stop_listening_on_close(self):
        self.stop_listening()
        self.window.destroy() 
        sys.exit() 

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
