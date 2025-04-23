import os
from faster_whisper import WhisperModel

def is_model_downloaded(model_name, download_root="./models"):
    model_path = os.path.join(download_root, model_name)
    return os.path.isdir(model_path) and os.path.isfile(os.path.join(model_path, "model.bin"))

def download_model(model_name, download_root="./models"):
    if is_model_downloaded(model_name, download_root):
        print(f"✅ Model '{model_name}' is already downloaded.")
    else:
        print(f"⬇ Downloading model '{model_name}' to '{download_root}'...")
        WhisperModel(model_name, download_root=download_root)
        print(f"✅ Model '{model_name}' downloaded successfully.")

# ✏️ Change this to the model you want to test
model_to_download = "medium"  # or "tiny", "large-v3", etc.

download_model(model_to_download)
