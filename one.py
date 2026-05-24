import tkinter as tk
from threading import Thread
import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import time
import wikipedia
import math

# --- CORE SETUP ---
recognizer = sr.Recognizer()

def speak(text):
    update_ui(f"JARVIS: {text}")
    try:
        # Initializing inside the function ensures the audio driver is active
        engine = pyttsx3.init()
        engine.setProperty('rate', 220) # High speed for JARVIS feel
        engine.say(text)
        engine.runAndWait()
        # Explicitly stop the engine to free the driver for the next call
        engine.stop()
    except Exception as e:
        print(f"Speech error: {e}")

def update_ui(text):
    chat_log.configure(state='normal')
    chat_log.insert(tk.END, f"{text}\n\n")
    chat_log.configure(state='disabled')
    chat_log.see(tk.END)

# --- COMMAND HANDLER ---
def processCommand(command):
    cmd = command.lower().strip()
    if "open google" in cmd:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "camera" in cmd:
        os.system("start microsoft.windows.camera:")
        speak("Camera on.")
    elif "exit" in cmd or "stop" in cmd:
        speak("Goodbye.")
        root.destroy()
        os._exit(0)
    else:
        try:
            results = wikipedia.summary(cmd, sentences=1)
            speak(results)
        except:
            speak("No results.")

# --- UI ANIMATION ---
def animate_circle():
    angle = 0
    while True:
        angle += 0.2
        pulse = 5 * math.sin(angle)
        canvas.delete("pulse")
        canvas.create_oval(75-pulse, 75-pulse, 225+pulse, 225+pulse, 
                           outline="#00ccff", width=2, tags="pulse")
        for i in range(0, 10):
            offset = math.sin(angle + i) * 15
            canvas.create_line(100 + (i*10), 150 - offset, 100 + (i*10), 150 + offset, 
                               fill="#00ffcc", width=3, tags="pulse")
        time.sleep(0.04)

# --- JARVIS CORE LOOP ---
def main_loop():
    time.sleep(1)
    speak("Jarvis online.")
    while True:
        try:
            with sr.Microphone() as source:
                status_var.set("● STANDBY")
                canvas.itemconfig(inner_circle, fill="#050505")
                # Speed hack: Very short ambient adjustment
                recognizer.adjust_for_ambient_noise(source, duration=0.1)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=2)
                word = recognizer.recognize_google(audio).lower()
            
            if "jarvis" in word:
                status_var.set("● ACTIVE")
                canvas.itemconfig(inner_circle, fill="#112233")
                speak("Yes") # Quickest response possible
                
                with sr.Microphone() as source:
                    # Low timeout means it stops listening the moment you stop talking
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    command = recognizer.recognize_google(audio)
                    update_ui(f"USER: {command}")
                    processCommand(command)
        except:
            continue

# --- UI DESIGN ---
def start_gui():
    global root, status_var, chat_log, canvas, inner_circle
    root = tk.Tk()
    root.title("JARVIS")
    root.geometry("900x550")
    root.configure(bg="#050505")

    main_container = tk.Frame(root, bg="#050505")
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    left_frame = tk.Frame(main_container, bg="#050505")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(left_frame, width=300, height=300, bg="#050505", highlightthickness=0)
    canvas.pack(pady=10)
    inner_circle = canvas.create_oval(80, 80, 220, 220, outline="#00ccff", width=1)
    
    status_var = tk.StringVar(value="● READY")
    tk.Label(left_frame, textvariable=status_var, fg="#00ffcc", bg="#050505", 
             font=("Courier New", 14, "bold")).pack()

    right_frame = tk.Frame(main_container, bg="#0a0a0a", highlightbackground="#00ccff", highlightthickness=1)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
    
    chat_log = tk.Text(right_frame, bg="#0a0a0a", fg="#00ffcc", font=("Consolas", 11), 
                        state='disabled', wrap='word', bd=0)
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    Thread(target=main_loop, daemon=True).start()
    Thread(target=animate_circle, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    start_gui()