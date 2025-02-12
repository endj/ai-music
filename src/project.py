import json
import os
from dataclasses import asdict
from typing import Dict

from args import ProcessJob

META = "../projects/meta.json"

def _save_meta(meta_data: Dict[str, ProcessJob]):
    with open(META, "w") as f:
        meta_dict = {key: asdict(job) for key, job in meta_data.items()}
        json.dump(meta_dict, f)
    return meta_data


def _meta() -> Dict[str, ProcessJob]:
    if os.path.isfile(META):
        with open(META) as mf:
            meta_data = json.load(mf)
            return {key: ProcessJob(**value) for key, value in meta_data.items()}
    return {}


def create_folder(job: ProcessJob) -> str:
    folder_name = job.project_id
    projects = _meta()
    projects[job.project_id] = job
    _save_meta(projects)
    folder_path = f"../projects/{folder_name}"
    os.mkdir(folder_path)
    return folder_path
