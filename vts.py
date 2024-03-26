import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pydub import AudioSegment
import speech_recognition as sr

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
    if file_path:
        transcribed_text, timestamps = convert_audio_to_text(file_path)
        create_srt_file(transcribed_text, timestamps)

def convert_audio_to_text(audio_file):
    sound = AudioSegment.from_mp3(audio_file)
    recognizer = sr.Recognizer()
    audio_chunks = []
    timestamps = []
    for i in range(0, len(sound), 10000):  # Split audio into chunks of 10 seconds
        audio_chunks.append(sound[i:i+10000])
        timestamps.append((i / 1000, (i + len(sound[i:i+10000])) / 1000))  # Convert milliseconds to seconds

    transcribed_text = ""
    for chunk in audio_chunks:
        with sr.AudioFile(chunk.export(format="wav")) as source:
            audio_data = recognizer.record(source)
        try:
            transcribed_text += recognizer.recognize_google(audio_data, language="ja-JP") + " "
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return transcribed_text, timestamps

def create_srt_file(transcribed_text, timestamps):
    output_file_path = os.path.splitext(filedialog.askopenfilename())[0] + ".srt"
    with open(output_file_path, "w", encoding="utf-8") as f:
        for i, (start, end) in enumerate(timestamps, start=1):
            f.write(f"{i}\n")
            f.write(f"{convert_time_format(start)} --> {convert_time_format(end)}\n")
            f.write(transcribed_text + "\n\n")
    print("SRT File created:", output_file_path)

def convert_time_format(seconds):
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds / 60)
    seconds %= 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"

root = tk.Tk()
root.title("Audio to SRT Converter")

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

root.mainloop()
