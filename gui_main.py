import os
import threading
from tkinter import Tk, Label, StringVar, OptionMenu, ttk, messagebox, Button
from transcribe_faster import transcribe
from Helper import get_supported_models, DEVICE_OPTIONS
from input_selector_ui import create_input_selector_ui

def run_transcription():
    filepath = file_path.get()
    method = method_choice.get()
    lang = lang_choice.get()

    if source_choice.get() == "YouTube Link":
        url = youtube_link.get()
        if not url:
            messagebox.showerror("No URL", "Please enter a YouTube link.")
            return
        filepath = "placeholder_downloaded_file.mp3"  # simulate download result

    if not filepath:
        messagebox.showerror("No file", "Please select a file.")
        return

    progress_bar["value"] = 0
    progress_bar.update()

    def worker():
        try:
            progress_bar["value"] = 10
            progress_bar.update()

            if method == "Faster-Whisper":
                device = DEVICE_OPTIONS[device_choice_label.get()]
                transcribe(filepath, lang, model_choice.get(), device, progress_bar)
            else:
                messagebox.showinfo("Not Implemented", "WhisperX support coming soon!")

            progress_bar["value"] = 100
            progress_bar.update()
            messagebox.showinfo("Done", "Transcription complete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            progress_bar["value"] = 0

    threading.Thread(target=worker).start()

app = Tk()
app.title("Whisper GUI")

# --- Input toggle state ---
source_choice = StringVar(value="Local File")
file_path = StringVar()
youtube_link = StringVar()

# --- GUI Settings ---
method_choice = StringVar(value="Faster-Whisper")
lang_choice = StringVar(value="ja")
model_choice = StringVar()
model_list = get_supported_models()
model_choice.set("medium" if "medium" in model_list else model_list[0])
device_choice_label = StringVar(value="Auto")

# --- Input selector ---
def update_source_inputs():
    if source_choice.get() == "Local File":
        youtube_frame.pack_forget()
        file_frame.pack()
    else:
        file_frame.pack_forget()
        youtube_frame.pack()

file_frame, youtube_frame, yt_progress = create_input_selector_ui(
    app, source_choice, file_path, youtube_link, update_source_inputs
)

update_source_inputs()

# --- Rest of GUI ---

Label(app, text="Whisper Settings:", font=("Arial", 12, "bold")).pack(pady=(20, 10))

Label(app, text="Whisper Engine:").pack()
OptionMenu(app, method_choice, "Faster-Whisper", "WhisperX").pack()

Label(app, text="Language:").pack()
OptionMenu(app, lang_choice, "ja", "en").pack()

Label(app, text="Model Size:").pack()
OptionMenu(app, model_choice, *model_list).pack()

Label(app, text="Device:").pack()
OptionMenu(app, device_choice_label, *DEVICE_OPTIONS.keys()).pack()

progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

Label(app, text="").pack()  # Spacer

Button(app, text="Transcribe", command=run_transcription).pack(pady=10)

app.mainloop()
