import json
import os
from dataclasses import asdict
from typing import Dict

from args import Job


def _save_meta(meta_data: Dict[str, Job]):
    with open("../projects/meta.json", "w") as f:
        meta_dict = {key: asdict(job) for key, job in meta_data.items()}
        json.dump(meta_dict, f)
    return meta_data


def _meta() -> Dict[str, Job]:
    if os.path.isfile("../projects/meta.json"):
        with open("../projects/meta.json") as mf:
            meta_data = json.load(mf)
            return {key: Job(**value) for key, value in meta_data.items()}
    return {}


def create_folder(job: Job) -> str:
    folder_name = job.project_id
    projects = _meta()
    projects[job.project_id] = job
    _save_meta(projects)
    folder_path = f"../projects/{folder_name}"
    os.mkdir(folder_path)
    return folder_path
