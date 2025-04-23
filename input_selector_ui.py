from tkinter import ttk, Label, Button, Entry, filedialog, StringVar, OptionMenu

def create_input_selector_ui(app, source_choice, file_path, youtube_link, update_callback):
    Label(app, text="Input Source:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
    OptionMenu(app, source_choice, "Local File", "YouTube Link", command=lambda _: update_callback()).pack()

    # Container to hold both file_frame and youtube_frame
    input_container = ttk.Frame(app)
    input_container.pack()

    # --- File selection frame ---
    file_frame = ttk.Frame(input_container)
    Label(file_frame, text="").pack()  # Spacer above
    Button(file_frame, text="Choose File", command=lambda: select_file(file_path)).pack()
    Label(file_frame, textvariable=file_path).pack()

    # --- YouTube link input frame ---
    youtube_frame = ttk.Frame(input_container)
    Label(youtube_frame, text="").pack()  # Spacer above
    Label(youtube_frame, text="YouTube URL:").pack()
    Entry(youtube_frame, textvariable=youtube_link, width=40).pack()
    yt_progress = ttk.Progressbar(youtube_frame, orient="horizontal", length=300, mode="determinate")
    yt_progress.pack(pady=5)

    # Separator below both input types
    Label(file_frame, text="").pack()  # Spacer above
    ttk.Separator(app, orient="horizontal").pack(fill='x', pady=10)

    return file_frame, youtube_frame, yt_progress

def select_file(file_path):
    selected = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp4 *.mp3 *.wav")])
    if selected:
        file_path.set(selected)
