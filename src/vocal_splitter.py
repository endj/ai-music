import shutil

import demucs.separate
import logging
import os
import time
import torch
from pathlib import Path

log = logging.getLogger(__name__)


def split_raw_audio(raw_mp3_path: str, output_dir: str):
    raw_mp3_path_obj = Path(raw_mp3_path)
    output_dir_obj = Path(output_dir)

    if not raw_mp3_path_obj.is_file():
        raise FileNotFoundError(f"Error: The file '{raw_mp3_path}' does not exist.")
    if not output_dir_obj.is_dir():
        raise NotADirectoryError(f"Error: The directory '{output_dir}' does not exist.")

    # Perhaps it's not possible on intel/AMD, maybe works on m1
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log.info(f"Splitting {raw_mp3_path}... on {device}")

    start_time = time.time()
    demucs.separate.main([
        "--out", output_dir,
        "--two-stems", "vocals",
        "--mp3",
        "--device", device,
        raw_mp3_path
    ])
    end_time = time.time()
    print("Finished splitting in", end_time - start_time)

    song_name = raw_mp3_path_obj.stem

    htdemucs_dir = output_dir_obj / "htdemucs" / song_name
    new_dir = output_dir_obj /  "split"

    print(f"Existing dir {str(htdemucs_dir)}")
    print(f"Created dir {str(new_dir)}")

    new_dir.mkdir(parents=True, exist_ok=True)

    print(f"Copying files {os.listdir(htdemucs_dir)}")

    for f in os.listdir(htdemucs_dir):
        src_path = htdemucs_dir / f
        if src_path.is_file():
            dst_path = new_dir / f
            shutil.copy2(src_path, dst_path)

    vocals_path = str(new_dir / "vocals.mp3")
    other_path = str(new_dir / "no_vocals.mp3")

    shutil.rmtree(htdemucs_dir)

    return vocals_path, other_path
