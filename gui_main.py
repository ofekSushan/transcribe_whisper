import os
import threading
from tkinter import (
    Tk,
    Label,
    StringVar,
    OptionMenu,
    ttk,
    messagebox,
    Button,
    BooleanVar,
    Checkbutton,
    Frame,
)
from transcribe_faster import transcribe
from Helper import get_supported_models, DEVICE_OPTIONS
from input_selector_ui import create_input_selector_ui
from youtube_downloader import download_youtube_video


def run_transcription():
    filepath = file_path.get()
    if source_choice.get() == "YouTube Link":
        url = youtube_link.get()
        if not url:
            messagebox.showerror("No URL", "Please enter a YouTube link.")
            return

        progress_bar["value"] = 5
        progress_bar.update()

        try:
            filepath = download_youtube_video(url=url, quality=quality_choice.get())
        except Exception as e:
            messagebox.showerror("Download Failed", f"Failed to download video:\n{e}")
            return
    else:
        if not filepath:
            messagebox.showerror("No file", "Please select a file.")
            return

    if download_only.get():
        messagebox.showinfo("Done", "Download complete (subtitles skipped).")
        return

    progress_bar["value"] = 0
    progress_bar.update()

    def worker():
        try:
            progress_bar["value"] = 10
            progress_bar.update()
            if method_choice.get() == "Faster-Whisper":
                device = DEVICE_OPTIONS[device_choice_label.get()]
                transcribe(
                    filepath,
                    lang_choice.get(),
                    model_choice.get(),
                    device,
                    progress_bar,
                )
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

# Input state
source_choice = StringVar(value="YouTube Link")
file_path = StringVar()
youtube_link = StringVar()
download_only = BooleanVar(value=False)

# Settings state
method_choice = StringVar(value="Faster-Whisper")
lang_choice = StringVar(value="ja")
model_choice = StringVar()
model_list = get_supported_models()
model_choice.set("medium" if "medium" in model_list else model_list[0])
device_choice_label = StringVar(value="Auto")

# Layout
content_frame = Frame(app)
content_frame.pack()


def update_source_inputs():
    if source_choice.get() == "YouTube Link":
        file_frame.pack_forget()
        youtube_frame.pack()
    else:
        youtube_frame.pack_forget()
        file_frame.pack()


file_frame, youtube_frame, yt_progress, quality_choice, source_option_menu = (
    create_input_selector_ui(
        content_frame, source_choice, file_path, youtube_link, update_source_inputs
    )
)
update_source_inputs()


def update_whisper_visibility():
    if download_only.get():
        source_choice.set("YouTube Link")
        update_source_inputs()
        source_option_menu.config(state="disabled")
        whisper_frame.pack_forget()
    else:
        source_option_menu.config(state="normal")
        whisper_frame.pack(pady=(10, 0))


Checkbutton(
    content_frame,
    text="Download Only (No Subtitles)",
    variable=download_only,
    command=update_whisper_visibility,
).pack(pady=(10, 0))

# Whisper Settings
whisper_frame = Frame(content_frame)
ttk.Separator(whisper_frame, orient="horizontal").pack(fill="x", pady=10)
Label(whisper_frame, text="Whisper Settings:", font=("Arial", 12, "bold")).pack(
    pady=(10, 10)
)
Label(whisper_frame, text="Whisper Engine:").pack()
OptionMenu(whisper_frame, method_choice, "Faster-Whisper", "WhisperX").pack()
Label(whisper_frame, text="Language:").pack()
OptionMenu(whisper_frame, lang_choice, "ja", "en").pack()
Label(whisper_frame, text="Model Size:").pack()
OptionMenu(whisper_frame, model_choice, *model_list).pack()
Label(whisper_frame, text="Device:").pack()
OptionMenu(whisper_frame, device_choice_label, *DEVICE_OPTIONS.keys()).pack()
whisper_frame.pack(pady=(10, 0))

# Bottom Section
progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)
Button(app, text="Transcribe", command=run_transcription).pack(pady=10)

app.mainloop()
