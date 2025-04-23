from tkinter import ttk, Label, Button, Entry, filedialog, StringVar, OptionMenu


def create_input_selector_ui(
    app, source_choice, file_path, youtube_link, update_callback
):
    dark_bg = "#1e1e1e"
    light_fg = "#f0f0f0"
    highlight = "#3c3c3c"

    Label(
        app, text="Input Source:", font=("Arial", 12, "bold"), bg=dark_bg, fg=light_fg
    ).pack(pady=(10, 5))
    source_menu = OptionMenu(
        app,
        source_choice,
        "YouTube Link",
        "Local File",
        command=lambda _: update_callback(),
    )
    source_menu.configure(bg=highlight, fg=light_fg, activebackground=dark_bg)
    source_menu.pack()

    input_container = ttk.Frame(app)
    input_container.pack()

    file_frame = ttk.Frame(input_container)
    Label(file_frame, text="", bg=dark_bg).pack(pady=5)
    Button(
        file_frame,
        text="Choose File",
        command=lambda: select_file(file_path),
        bg=highlight,
        fg=light_fg,
    ).pack()
    Label(file_frame, textvariable=file_path, bg=dark_bg, fg=light_fg).pack()

    youtube_frame = ttk.Frame(input_container)
    Label(youtube_frame, text="", bg=dark_bg).pack(pady=5)
    Label(youtube_frame, text="YouTube URL:", bg=dark_bg, fg=light_fg).pack()
    Entry(
        youtube_frame,
        textvariable=youtube_link,
        width=40,
        bg=dark_bg,
        fg=light_fg,
        insertbackground=light_fg,
    ).pack()
    Label(youtube_frame, text="", bg=dark_bg).pack(pady=2)
    yt_progress = ttk.Progressbar(
        youtube_frame, orient="horizontal", length=300, mode="determinate"
    )
    yt_progress.pack(pady=5)

    quality_choice = StringVar(value="best")
    quality_menu = OptionMenu(
        youtube_frame, quality_choice, "best", "1080p", "720p", "480p", "360p", "audio"
    )
    quality_menu.configure(bg=highlight, fg=light_fg, activebackground=dark_bg)
    quality_menu.pack()

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
