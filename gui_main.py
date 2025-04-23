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
from input_selector_ui import create_input_selector_ui, set_yt_progress
from youtube_downloader import download_youtube_video


def set_main_progress(value):
    progress_bar["value"] = value
    progress_bar.update()


def run_program():
    if source_choice.get() == "YouTube Link":
        url = youtube_link.get()
        if not url:
            messagebox.showerror("No URL", "Please enter a YouTube link.")
            return

        set_yt_progress(yt_progress, 5)

        def download_thread():
            set_yt_progress(yt_progress, 10)
            try:
                filepath_result = download_youtube_video(
                    url=url, quality=quality_choice.get(), progress_bar=yt_progress
                )
                file_path.set(filepath_result)
                set_yt_progress(yt_progress, 100)

                if download_only.get():
                    messagebox.showinfo(
                        "Done", "Download complete (subtitles skipped)."
                    )
                    set_yt_progress(yt_progress, 0)
                else:

                    def wrapped_transcription():
                        run_Wisper()
                        set_yt_progress(yt_progress, 0)

                    app.after(10, wrapped_transcription)

            except Exception as e:
                messagebox.showerror(
                    "Download Failed", f"Failed to download video:\n{e}"
                )
                set_yt_progress(yt_progress, 0)

        threading.Thread(target=download_thread).start()
        return
    else:
        if not file_path.get():
            messagebox.showerror("No file", "Please select a file.")
            return

        if download_only.get():
            messagebox.showinfo("Done", "Download complete (subtitles skipped).")
            return

        run_Wisper()


def run_Wisper():
    set_main_progress(0)

    def worker():
        try:
            set_main_progress(10)
            if method_choice.get() == "Faster-Whisper":
                device = DEVICE_OPTIONS[device_choice_label.get()]
                transcribe(
                    file_path.get(),
                    lang_choice.get(),
                    model_choice.get(),
                    device,
                    progress_bar,
                )
            else:
                messagebox.showinfo("Not Implemented", "WhisperX support coming soon!")

            set_main_progress(100)
            messagebox.showinfo("Done", "Transcription complete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            set_main_progress(0)

    threading.Thread(target=worker).start()


app = Tk()
app.title("Whisper GUI")

source_choice = StringVar(value="YouTube Link")
file_path = StringVar()
youtube_link = StringVar()
download_only = BooleanVar(value=False)

method_choice = StringVar(value="Faster-Whisper")
lang_choice = StringVar(value="ja")
model_choice = StringVar()
model_list = get_supported_models()
model_choice.set("medium" if "medium" in model_list else model_list[0])
device_choice_label = StringVar(value="Auto")

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

whisper_frame = Frame(content_frame)
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

progress_bar = ttk.Progressbar(whisper_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)
Button(app, text="Transcribe", command=run_program).pack(pady=10)

app.mainloop()
