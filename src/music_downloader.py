import typing, logging
import yt_dlp
log = logging.getLogger(__name__)

def download_audio(url: str, output_folder: str):
    ydl_opts = {
        'format': 'bestaudio/best',  # Select best audio quality
        'outtmpl': f'{output_folder}/original.%(ext)s',  # Output filename format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Convert audio to a specific format
            'preferredcodec': 'wav',  # Change this to 'wav', 'opus', etc. if needed
            'preferredquality': '192',  # Adjust bitrate
        }],
        'quiet': False,  # Set to True to suppress output
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    log.info(f"Downloaded {url} to {output_folder}/original.wav")
    return f"{output_folder}/original.wav"
