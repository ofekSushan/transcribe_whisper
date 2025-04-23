import os
import time
from faster_whisper import WhisperModel
from Helper import get_supported_models


def format_timestamp(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def transcribe(filepath, language, model_size, device, progress_bar):
    if model_size not in get_supported_models():
        raise ValueError(f"Model '{model_size}' is not supported.")

    if device == "auto":
        model = WhisperModel(model_size, compute_type="int8_float16")
    else:
        model = WhisperModel(model_size, compute_type="int8_float16", device=device)

    segments_gen, info = model.transcribe(filepath, language=language)
    segments = list(segments_gen)

    base = os.path.splitext(filepath)[0]
    out_path = base + ".srt"

    with open(out_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            progress_bar["value"] = (i / len(segments)) * 90 + 10
            progress_bar.update()
            f.write(f"{i+1}\n")
            f.write(
                f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n"
            )
            f.write(segment.text.strip() + "\n\n")
