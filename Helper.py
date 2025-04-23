DEVICE_OPTIONS = {
    "Auto": "auto",
    "GPU": "cuda",
    "CPU": "cpu"
}

def get_supported_models():
    return [
        "tiny",
        "base",
        "small",
        "medium",
        "large-v1",
        "large-v2",
        "large-v3"
    ]
