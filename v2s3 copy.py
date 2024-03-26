import tkinter as tk
from tkinter import filedialog
import os
import speech_recognition as sr
import ffmpeg
from googletrans import Translator

class AudioTranscriber:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Japanese Audio Transcriber")
        self.root.geometry("400x200")

        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack()

        self.progress_bar = tk.Canvas(self.root, width=300, height=20, bg='white')
        self.progress_bar.pack()

        self.progress_rect = self.progress_bar.create_rectangle(0, 0, 0, 20, fill='blue')

        self.transcriber_label = tk.Label(self.root, text="1. Select MP3 audio file:")
        self.transcriber_label.pack()

        self.transcriber_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.transcriber_button.pack()

        self.transcriber_button_state = True

        self.transcriber_button = tk.Button(self.root, text="Transcribe", command=self.transcribe, state=tk.DISABLED)
        self.transcriber_button.pack()

        self.audio_file_path = ""
        self.transcript = ""
        self.translator = Translator()

    def browse_file(self):
        self.audio_file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if self.audio_file_path:
            self.transcriber_button.config(state=tk.NORMAL)
            self.transcriber_button_state = False

    def transcribe(self):
        if not self.audio_file_path:
            self.progress_label.config(text="Please select an audio file first.")
            return

        try:
            audio = sr.AudioFile(self.audio_file_path)
            r = sr.Recognizer()
            with audio as source:
                audio_file = r.record(source)
            self.transcript = r.recognize_google(audio_file, language='ja-JP')

            translated_text = self.translator.translate(self.transcript, src='ja', dest='en').text
            subtitles = self.transcript_to_subtitles(translated_text)

            with open("subtitles.srt", "w", encoding="utf-8") as f:
                f.write(subtitles)

            self.progress_label.config(text="Transcription completed.")
        except Exception as e:
            self.progress_label.config(text=f"Error: {str(e)}")

    def transcript_to_subtitles(self, text):
        lines = text.split('\n')
        subtitles = ''
        line_count = 1
        for i, line in enumerate(lines):
            start_time = '00:00:00'
            end_time = '00:00:00'
            subtitle = f"{line_count}\n{start_time} --> {end_time}\n{line}\n\n"
            subtitles += subtitle
            line_count += 1
        return subtitles

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AudioTranscriber()
    app.run()
