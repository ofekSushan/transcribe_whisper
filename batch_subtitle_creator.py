import os
from faster_whisper import WhisperModel

# Use medium model for balance of speed and quality
model = WhisperModel("medium", compute_type="float16")

def format_timestamp(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# Scan all .mp4 files in current directory
for filename in os.listdir("."):
    if filename.endswith(".mp4"):
        print(f"Transcribing: {filename}")
        segments, _ = model.transcribe(filename, language="ja")

        base_name = os.path.splitext(filename)[0]
        srt_path = f"{base_name}.srt"

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                f.write(f"{i+1}\n")
                f.write(f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n")
                f.write(segment.text.strip() + "\n\n")
        print(f"Saved: {srt_path}")
