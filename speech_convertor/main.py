import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import pyaudio
import wave

class SpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.root = tk.Tk()
        self.root.title("Speech Recognizer")
        self.label = tk.Label(self.root, text="Press Start to begin recording")
        self.label.pack()
        self.button = tk.Button(self.root, text="Start", command=self.start_recording)
        self.button.pack()
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording, state="disabled")
        self.stop_button.pack()
        self.text_box = tk.Text(self.root)
        self.text_box.pack()
        self.save_button = tk.Button(self.root, text="Save", command=self.save_notes)
        self.save_button.pack()
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text)
        self.clear_button.pack()
        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio)
        self.play_button.pack()

        self.recording = False
        self.thread = None
        self.audio_data = []

    def recognize_speech(self):
        while self.recording:
            try:
                with self.mic as source:
                    audio = self.r.listen(source, timeout=5)
                    text = self.r.recognize_google(audio)
                    self.text_box.insert(tk.END, text + "\n")
                    self.audio_data.append(audio.get_raw_data())
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Speech recognition could not understand audio")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Error requesting results; {e}")

    def start_recording(self):
        self.recording = True
        self.button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.thread = threading.Thread(target=self.recognize_speech)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        self.button.config(state="normal")
        self.stop_button.config(state="disabled")

    def save_notes(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as file:
                file.write(self.text_box.get("1.0", tk.END))
        audio_filename = filename.replace(".txt", ".wav")
        with wave.open(audio_filename, "wb") as wave_file:
            wave_file.setnchannels(1)
            wave_file.setsampwidth(2)
            wave_file.setframerate(16000)
            wave_file.writeframes(b''.join(self.audio_data))

    def clear_text(self):
        self.text_box.delete("1.0", tk.END)

    def play_audio(self):
        audio_filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if audio_filename:
            with wave.open(audio_filename, "rb") as wave_file:
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wave_file.getsampwidth()),
                                channels=wave_file.getnchannels(),
                                rate=wave_file.getframerate(),
                                output=True)
                data = wave_file.readframes(1024)
                while data != b'':
                    stream.write(data)
                    data = wave_file.readframes(1024)
                stream.stop_stream()
                stream.close()
                p.terminate()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    recognizer.run()