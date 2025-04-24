DEVICE_OPTIONS = {"Auto": "auto", "GPU": "cuda", "CPU": "cpu"}

Language_OPTIONS = {
    "Auto": None,
    "Japanese (日本語)": "ja",
    "English": "en",
    "Hebrew (עברית)": "he",
    "Russian (русский)": "ru",
}


def get_supported_models():
    return ["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"]
