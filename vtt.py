import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pydub import AudioSegment
import speech_recognition as sr

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
    if file_path:
        convert_audio_to_text(file_path)

def convert_audio_to_text(audio_file):
    output_file = os.path.splitext(audio_file)[0] + ".txt"
    sound = AudioSegment.from_mp3(audio_file)
    recognizer = sr.Recognizer()
    audio_chunks = []
    for i in range(0, len(sound), 10000):  # Split audio into chunks of 10 seconds
        audio_chunks.append(sound[i:i+10000])

    text = ""
    for chunk in audio_chunks:
        with sr.AudioFile(chunk.export(format="wav")) as source:
            audio_data = recognizer.record(source)
        try:
            text += recognizer.recognize_google(audio_data, language="ja-JP") + " "
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        progress_bar.step(10)  # Update progress bar

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print("Transcribed Text saved in:", output_file)

root = tk.Tk()
root.title("Audio to Text Converter")

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack()

root.mainloop()
