import os
import yt_dlp
import re


def sanitize_filename(name):
    return re.sub(r"[\\/:\"*?<>|]+", "", name)


def download_youtube_video(url=None, filepath=None, quality="best", progress_bar=None):
    if filepath:
        return filepath

    if not url:
        raise ValueError("You must provide a YouTube URL if not using local file.")

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info.get("title", "youtube_video"))

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    if quality == "audio":
        filename = f"{title} [audio]"
        format_code = "bestaudio"
        postprocessors = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
        merge = None
        final_ext = ".mp3"
    else:
        if quality == "best":
            actual_height = info.get("height") or info.get("formats", [{}])[0].get(
                "height", 1080
            )
            suffix = f"{actual_height}p"
        else:
            suffix = quality

        filename = f"{title} [{suffix}]"

        if quality == "best":
            format_code = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
        else:
            format_code = f"bestvideo[height={quality.rstrip('p')}][ext=mp4]+bestaudio[ext=m4a]/mp4"

        postprocessors = []
        merge = "mp4"
        final_ext = ".mp4"

    output_path = os.path.join(output_dir, filename)
    if quality == "audio" and output_path.endswith(".mp3"):
        output_path = output_path[:-4]

    if os.path.exists(output_path + final_ext):
        return output_path + final_ext

    def progress_hook(d):
        if not progress_bar:
            return

        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total_bytes:
                try:
                    percent = (downloaded / total_bytes) * 100
                    progress_bar["value"] = percent
                    progress_bar.update()
                except:
                    pass
        elif d["status"] == "finished":
            try:
                progress_bar["value"] = 100
                progress_bar.update()
            except:
                pass

    ydl_opts = {
        "format": format_code,
        "outtmpl": output_path,
        "merge_output_format": merge,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": postprocessors,
        "progress_hooks": [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path + final_ext
