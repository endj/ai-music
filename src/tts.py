import subprocess
from pathlib import Path

def text_to_speech(text: str, output_path: str):
    output = Path(output_path)
    aiff_file = "out.aiff"

    subprocess.run(["say", "-o", aiff_file, text], check=True)
    subprocess.run(["ffmpeg", "-i", aiff_file, output, "-y"], check=True)
    subprocess.run(["rm", aiff_file])
