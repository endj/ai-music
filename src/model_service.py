import json
import logging
import os
import shutil
from dataclasses import asdict
from typing import Dict, List, Union
from dataclasses import dataclass

from args import RegisterModel

log = logging.getLogger(__name__)

META = "../models/meta.json"

@dataclass(frozen=True)
class Model:
    original_path: str
    name: str
    folder_path: str
    model_path: str

@dataclass(frozen=True)
class ModelQuery:
    missing_models: List[str]

def copy_file(file_path: str, directory_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist or not file")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Dir {directory_path} does not exist or not a path")
    shutil.copy(file_path, directory_path)


def _save_meta(meta_data: Dict[str, Model]):
    with open(META, "w") as f:
        meta_dict = {key: asdict(job) for key, job in meta_data.items()}
        json.dump(meta_dict, f)
    return meta_data


def _meta() -> Dict[str, Model]:
    if os.path.isfile(META):
        with open(META) as mf:
            meta_data = json.load(mf)
            return {key: Model(**value) for key, value in meta_data.items()}
    return {}

def get_model(name: str) -> Model:
    models = _meta()
    if name in models:
        return models[name]
    raise Exception(f"Model with name {name} not found")

def register_model(model: RegisterModel):
    models = _meta()
    if model.name in models:
        raise Exception(f"Model with name {model.name} already exists")

    folder_path = f"../models/{model.name}"

    new_model = Model(
        original_path=model.path,
        name=model.name,
        folder_path=folder_path,
        model_path=f"{folder_path}/{os.path.basename(model.path)}"
    )

    models[model.name] = new_model
    _save_meta(models)
    os.mkdir(folder_path)
    copy_file(model.path, folder_path)
    log.info(f"Registered model {new_model}")
    return folder_path


def list_available_models():
    models = _meta()
    model_names = "\n".join(["- " + m.name for m in models.values()])
    log.info(f"Available models:\n{model_names}")

def has_models(models: List[str]) -> ModelQuery:
    stored_models = _meta()
    missing_models = [m for m in models if m not in stored_models]
    return ModelQuery(missing_models)
