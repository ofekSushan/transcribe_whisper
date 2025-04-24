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
from tkinter import PhotoImage
from transcribe_faster import transcribe
from Helper import Language_OPTIONS, get_supported_models, DEVICE_OPTIONS
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
                language=Language_OPTIONS[lang_choice_label.get()]
                device = DEVICE_OPTIONS[device_choice_label.get()]
                transcribe(
                    file_path.get(),
                    language,
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
app.title("Transcribe_whisper")
app.geometry("512x668")
try:
    icon = PhotoImage(file="assets/icon.png")
    app.iconphoto(False, icon)
except Exception as e:
    print(f"Could not load icon: {e}")

# DARK MODE COLORS
dark_bg = "#1e1e1e"
light_fg = "#f0f0f0"
highlight = "#3c3c3c"
app.configure(bg=dark_bg)

# ttk style
ttk_style = ttk.Style()
ttk_style.theme_use("clam")
ttk_style.configure("TLabel", background=dark_bg, foreground=light_fg)
ttk_style.configure("TCheckbutton", background=dark_bg, foreground=light_fg)
ttk_style.configure("TButton", background=highlight, foreground=light_fg)
ttk_style.configure("TFrame", background=dark_bg)
ttk_style.configure("TSeparator", background=highlight)
ttk_style.configure(
    "Horizontal.TProgressbar", troughcolor=highlight, background="#5cb85c"
)

source_choice = StringVar(value="YouTube Link")
file_path = StringVar()
youtube_link = StringVar()
download_only = BooleanVar(value=False)

method_choice = StringVar(value="Faster-Whisper")
lang_choice_label = StringVar(value="Auto")

model_choice = StringVar()
model_list = get_supported_models()
model_choice.set("medium" if "medium" in model_list else model_list[0])
device_choice_label = StringVar(value="Auto")

content_frame = Frame(app, bg=dark_bg)
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
    bg=dark_bg,
    fg=light_fg,
    selectcolor=highlight,
).pack(pady=(10, 0))

whisper_frame = Frame(content_frame, bg=dark_bg)
Label(
    whisper_frame,
    text="Whisper Settings:",
    font=("Arial", 12, "bold"),
    bg=dark_bg,
    fg=light_fg,
).pack(pady=(10, 10))
Label(whisper_frame, text="Whisper Engine:", bg=dark_bg, fg=light_fg).pack()
OptionMenu(whisper_frame, method_choice, "Faster-Whisper", "WhisperX").pack()
Label(whisper_frame, text="Language:", bg=dark_bg, fg=light_fg).pack()
OptionMenu(whisper_frame, lang_choice_label, *Language_OPTIONS.keys()).pack()
Label(whisper_frame, text="Model Size:", bg=dark_bg, fg=light_fg).pack()
OptionMenu(whisper_frame, model_choice, *model_list).pack()
Label(whisper_frame, text="Device:", bg=dark_bg, fg=light_fg).pack()
OptionMenu(whisper_frame, device_choice_label, *DEVICE_OPTIONS.keys()).pack()
whisper_frame.pack(pady=(10, 0))

progress_bar = ttk.Progressbar(
    whisper_frame, orient="horizontal", length=300, mode="determinate"
)
progress_bar.pack(pady=10)
Button(app, text="Transcribe", command=run_program, bg=highlight, fg=light_fg).pack(
    pady=10
)

app.mainloop()
