import logging, model_service
from dataclasses import dataclass
import os
import subprocess
import time
from typing import List
from pathlib import Path

log = logging.getLogger(__name__)

@dataclass(frozen=True)
class TransformationResult:
    model_output_path: str
    model_folder_path: str
    model_name: str

def run_rvc_cli(vocal_file_path: Path, output_file: Path, model_path: Path):

    command = [
        "python",
        "-m",
        "rvc_python",
        "cli",
        "-i",
        str(vocal_file_path),
        "-o",
        str(output_file),
        "-mp",
        str(model_path)
    ]
    env = os.environ.copy()  # Create a copy of the current environment
    env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"  # Set the environment variable

    try:
        result = subprocess.run(
            command, capture_output=False, text=True, check=True, env=env, cwd=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return result.returncode # Return the exit code for checking success/failure
    except subprocess.CalledProcessError as e:
        log.error(f"Error running RVC CLI: {e}")
        return e.returncode # Return the error code
    except FileNotFoundError:
        log.error("Error: rvc_python module or Python not found. Check your environment.")
        raise Exception("rvc_python module or Python not found")
    except Exception as e:
        log.error(f"An error occurred: {e}")
        raise e


def transform_vocals(vocals_path: str, instrumental_path: str, project_folder_path: str, models: List[str]) -> List[TransformationResult]:
    vocals_path_obj = Path(vocals_path)
    instrumental_path_obj = Path(instrumental_path)
    output_path_obj = Path(project_folder_path)

    if not vocals_path_obj.is_file():
        raise FileNotFoundError(f"Error: The file '{vocals_path}' does not exist.")
    if not instrumental_path_obj.is_file():
        raise FileNotFoundError(f"Error: The file '{instrumental_path}' does not exist.")
    if not output_path_obj.is_dir():
        raise NotADirectoryError(f"Error: The directory '{project_folder_path}' does not exist.")

    model_output = output_path_obj / "models"
    model_output.mkdir(parents=True, exist_ok=True)

    results = []

    log.info(f"Transforming:\n Vocals: {vocals_path}\n instrumental: {instrumental_path}\n output: {project_folder_path}\n models: {str(models)}")
    for model_name in models:
        model_meta = model_service.get_model(model_name)
        model_path = Path(model_meta.model_path)
        if not model_path.is_file():
            raise FileNotFoundError(f"Error: The file '{model_meta.model_path}' does not exist.")

        output_folder = model_output / model_name
        output_folder.mkdir(parents=True, exist_ok=True)

        model_output_path = output_folder / f"{model_name}.mp3"

        print("Transforming using model",model_name)
        start_time = time.time()
        run_rvc_cli(vocals_path_obj, model_output_path, model_path)
        end_time = time.time()
        print("Finished transforming in", end_time - start_time)
        results.append(TransformationResult(
            str(model_output_path),
            str(output_folder),
            model_name
        ))

    return results