import logging
import subprocess
from pathlib import Path
from typing import List

from vocal_transformer import TransformationResult

log = logging.getLogger(__name__)


def _mix_mp3s(transformed_vocal: Path, instrumental: Path, output_file: Path):
    validate_file(transformed_vocal)
    validate_file(instrumental)
    command = [
        "ffmpeg",
        "-i", str(transformed_vocal),
        "-i", str(instrumental),
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=longest[out]",  # Mix audio
        "-map", "[out]",
        str(output_file),
        "-y"
    ]
    log.info(f"Running command {command}")
    result = subprocess.run(
        command,
        capture_output=False,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        log.error(f"ffmpeg returned an error: {result.returncode}")
        raise Exception(f"ffmpeg failed with return code {result.returncode}")


def validate_file(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"Error: The file '{str(path)}' does not exist.")
    return path


def combine(transformed: List[TransformationResult], instrumental_path: str):
    instrumental_path_obj = validate_file(Path(instrumental_path))

    for transformation in transformed:
        log.info(f"Combining {str(transformation.model_output_path)} with {str(instrumental_path_obj)}")

        mixed_output_path = Path(transformation.model_folder_path) / f"{transformation.model_name}_combined.mp3"

        log.info(f"Writing to {str(mixed_output_path)}")

        transformed_vocal = validate_file(Path(transformation.model_output_path))
        _mix_mp3s(transformed_vocal, instrumental_path_obj, mixed_output_path)
        log.info(f"Created {str(mixed_output_path)}")
