from huggingface_hub import list_models

print("⏳ Fetching models from Hugging Face...")
try:
    prefix = "guillaumekln/faster-whisper-"
    models = list_models()
    filtered = [m.modelId.replace(prefix, "") for m in models if m.modelId.startswith(prefix)]

    print("✅ Models fetched:")
    for name in filtered:
        print(" -", name)

except Exception as e:
    print("❌ Failed to fetch models:")
    print(e)
