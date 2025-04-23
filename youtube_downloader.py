import os
import yt_dlp
import re

def sanitize_filename(name):
    # Remove invalid characters for safe file saving
    return re.sub(r'[\\/:"*?<>|]+', '', name)

def download_youtube_video(url, quality="best"):
    """
    Downloads a YouTube video or audio using the title as filename inside the /output directory.
    
    Returns:
        str: Full path to downloaded file
    """

    # Get video info (title)
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info.get("title", "youtube_video"))

    # Prepare the output folder
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Define full output path based on quality
    if quality == "audio":
        filename = title + ".mp3"
        format_code = "bestaudio"
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        merge = None
    elif quality == "best":
        filename = title + ".mp4"
        format_code = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
        postprocessors = []
        merge = "mp4"
    else:
        filename = title + ".mp4"
        format_code = f"bestvideo[height={quality.rstrip('p')}][ext=mp4]+bestaudio[ext=m4a]/mp4"
        postprocessors = []
        merge = "mp4"

    output_path = os.path.join(output_dir, filename)

    # If file already exists, skip download
    if os.path.exists(output_path):
        return output_path

    ydl_opts = {
        'format': format_code,
        'outtmpl': output_path,
        'merge_output_format': merge,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': postprocessors,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path
