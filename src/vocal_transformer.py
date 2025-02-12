import logging, modelservice
from typing import List
from pathlib import Path

log = logging.getLogger(__name__)

def transform_vocals(vocals_path: str, instrumental_path: str, output_path: str, models: List[str]):
    vocals_path_obj = Path(vocals_path)
    instrumental_path_obj = Path(instrumental_path)
    output_path_obj = Path(output_path)

    if not vocals_path_obj.is_file():
        raise FileNotFoundError(f"Error: The file '{vocals_path}' does not exist.")
    if not instrumental_path_obj.is_file():
        raise FileNotFoundError(f"Error: The file '{instrumental_path}' does not exist.")
    if not output_path_obj.is_dir():
        raise NotADirectoryError(f"Error: The directory '{output_path}' does not exist.")


    log.info(f"Transforming:\n Vocals: {vocals_path}\n instrumental: {instrumental_path}\n output: {output_path}\n models: {str(models)}")
    for model in models:
        model_meta = modelservice.get_model(model)

        print("Transforming using model",model)

    return None