import argparse
import os
import urllib.parse
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Union, List


@dataclass(frozen=True)
class ProcessJob:
    url: str
    models: List[str]
    project_id: str
    created: str


@dataclass(frozen=True)
class RegisterModel:
    path: str
    name: str


@dataclass(frozen=True)
class ListModels:
    pass  # No extra arguments needed


def validate_voice(voice: str):
    if voice is None:
        raise Exception("Voice null")


def validate_youtube_url(url: str):
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname is None:
        raise Exception(f"Got invalid url {url}")
    if parsed.hostname != "www.youtube.com":
        raise Exception(f"Not youtube link, got hostname {parsed.hostname}")

def parse_models(models_csv: str) -> List[str]:
    return models_csv.split(",")


def validate_pth_file(path: str):
    """Ensure the file exists and has a .pth extension."""
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File does not exist: {path}")
    if not path.endswith(".pth"):
        raise argparse.ArgumentTypeError(f"File must have a .pth extension: {path}")


def parse_args() -> Union[ProcessJob, RegisterModel, ListModels]:
    parser = argparse.ArgumentParser(description="AI Music CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # "model" parent command
    model_parser = subparsers.add_parser("model", help="Model-related commands")
    model_subparsers = model_parser.add_subparsers(dest="subcommand", required=True)

    # model register
    register_parser = model_subparsers.add_parser("register", help="Register a new model")
    register_parser.add_argument("--path", required=True, help="Path to .pth file")
    register_parser.add_argument("--name", required=True, help="Unique name of the model")

    # model list
    model_subparsers.add_parser("list", help="List available models")

    # "process" command
    process_parser = subparsers.add_parser("process", help="Process a song with a model")
    process_parser.add_argument("--url", required=True, help="YouTube URL to process")
    process_parser.add_argument("--models", required=True, help="CSV string of AI model's")

    args = parser.parse_args()

    # Return the correct dataclass based on the command
    if args.command == "process":
        validate_youtube_url(args.url)
        models = parse_models(args.models)
        return ProcessJob(url=args.url, models=models, project_id=str(uuid.uuid4()), created=str(datetime.now()))
    elif args.command == "model":
        if args.subcommand == "register":
            validate_pth_file(args.path)
            return RegisterModel(path=args.path, name=args.name)
        elif args.subcommand == "list":
            return ListModels()

    raise ValueError("Unknown command")
