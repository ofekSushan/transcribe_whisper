from tkinter import ttk, Label, Button, Entry, filedialog, StringVar, OptionMenu


def create_input_selector_ui(
    app, source_choice, file_path, youtube_link, update_callback
):
    Label(app, text="Input Source:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
    source_menu = OptionMenu(
        app,
        source_choice,
        "YouTube Link",
        "Local File",
        command=lambda _: update_callback(),
    )
    source_menu.pack()

    input_container = ttk.Frame(app)
    input_container.pack()

    file_frame = ttk.Frame(input_container)
    Button(
        file_frame, text="Choose File", command=lambda: select_file(file_path)
    ).pack()
    Label(file_frame, textvariable=file_path).pack()

    youtube_frame = ttk.Frame(input_container)
    Label(youtube_frame, text="YouTube URL:").pack()
    Entry(youtube_frame, textvariable=youtube_link, width=40).pack()
    yt_progress = ttk.Progressbar(
        youtube_frame, orient="horizontal", length=300, mode="determinate"
    )
    yt_progress.pack(pady=5)

    quality_choice = StringVar(value="best")
    return file_frame, youtube_frame, yt_progress, quality_choice, source_menu


def select_file(file_path):
    selected = filedialog.askopenfilename(
        filetypes=[("Audio/Video Files", "*.mp4 *.mp3 *.wav")]
    )
    if selected:
        file_path.set(selected)


def set_yt_progress(progress_bar, value):
    progress_bar["value"] = value
    progress_bar.update()
