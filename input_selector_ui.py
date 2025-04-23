from tkinter import ttk, Label, Button, Entry, filedialog, StringVar, OptionMenu

def create_input_selector_ui(app, source_choice, file_path, youtube_link, update_callback):
    Label(app, text="Input Source: ").pack()
    OptionMenu(app, source_choice, "Local File", "YouTube Link", command=lambda _: update_callback()).pack()

    input_container = ttk.Frame(app)
    input_container.pack()

    # File selection frame
    file_frame = ttk.Frame(input_container)
    Button(file_frame, text="Choose File", command=lambda: select_file(file_path)).pack()
    Label(file_frame, textvariable=file_path).pack()

    # YouTube input frame
    youtube_frame = ttk.Frame(input_container)
    Label(youtube_frame, text="YouTube URL:").pack()
    Entry(youtube_frame, textvariable=youtube_link, width=40).pack()
    yt_progress = ttk.Progressbar(youtube_frame, orient="horizontal", length=300, mode="determinate")
    yt_progress.pack(pady=5)

    return file_frame, youtube_frame, yt_progress

def select_file(file_path):
    selected = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp4 *.mp3 *.wav")])
    if selected:
        file_path.set(selected)
