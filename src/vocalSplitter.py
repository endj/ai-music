import demucs.separate
import logging
import os
import time
import torch

log = logging.getLogger(__name__)


def split_raw_audio(raw_mp3_path: str, output_dir: str):
    if not os.path.isfile(raw_mp3_path):
        raise FileNotFoundError(f"Error: The file '{raw_mp3_path}' does not exist.")
    if not os.path.isdir(output_dir):
        raise NotADirectoryError(f"Error: The directory '{output_dir}' does not exist.")

    # Perhaps it's not possible on intel/AMD, maybe works on m1
    device = "cuda" if torch.cuda.is_available() else "cpu"

    log.info(f"Splitting {raw_mp3_path}... on {device}")

    start = time.time()
    demucs.separate.main([
        "--out", output_dir,
        "--two-stems", "vocals",
        "--mp3",
        "--device", device,  # Force GPU usage
        raw_mp3_path
    ])
    end = time.time()
    print("Finished splitting in", end - start)

    song_name = os.path.splitext(os.path.basename(raw_mp3_path))[0]
    vocals_path = os.path.join(output_dir, "htdemucs", song_name, "vocals.mp3")
    other_path = os.path.join(output_dir, "htdemucs", song_name, "no_vocals.mp3")
    return (vocals_path, other_path)
