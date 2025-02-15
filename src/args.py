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
class SplitJob:
    path: str
    out: str

@dataclass(frozen=True)
class TransformJob:
    path: str
    out: str
    models: List[str]

@dataclass(frozen=True)
class RegisterModel:
    path: str
    name: str

@dataclass(frozen=True)
class DownloadJob:
    url: str
    out: str

@dataclass(frozen=True)
class ListModels:
    pass

@dataclass(frozen=True)
class TTS:
    text: str
    out: str

@dataclass(frozen=True)
class Mix:
    vocals: str
    background: str
    out: str

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
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File does not exist: {path}")
    if not path.endswith(".pth"):
        raise argparse.ArgumentTypeError(f"File must have a .pth extension: {path}")


def parse_args() -> Union[ProcessJob, RegisterModel, ListModels, TransformJob, SplitJob, DownloadJob, TTS, Mix]:
    parser = argparse.ArgumentParser(description="AI Music CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # mix parent command
    mix_parse = subparsers.add_parser("mix", help="Mixes two mp3s")
    mix_parse.add_argument("--vocals", required=True, help="Vocal")
    mix_parse.add_argument("--background", required=True,help="Background")
    mix_parse.add_argument("--out", required=True,help="Where to write result")

    # "tts" parent command
    tts_parse = subparsers.add_parser("tts", help="Generates mp3 from text")
    tts_parse.add_argument("--text", required=True, help="Text to say")
    tts_parse.add_argument("--out", required=True, help="Where to write result")

    # "download" parent command
    youtube_parser = subparsers.add_parser("youtube", help="Downloads song from youtube")
    youtube_parser.add_argument("--url", required=True, help="url for song")
    youtube_parser.add_argument("--out", required=True,help="Where to write result")

    # "Split" parent command
    split_parser = subparsers.add_parser("split", help="Splits vocals for a song")
    split_parser.add_argument("--path", required=True, help="Path to .mp3 file")
    split_parser.add_argument("--out", required=True, help="Where to write result")

    # "transform" parent command
    transform_parser = subparsers.add_parser("transform", help="Transform MP3 using a model")
    transform_parser.add_argument("--path", required=True, help="Path to .mp3 file")
    transform_parser.add_argument("--out", required=True, help="Where to write result")
    transform_parser.add_argument("--models", required=True, help="What models to use")

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

    if args.command == "process":
        validate_youtube_url(args.url)
        models = parse_models(args.models)
        return ProcessJob(url=args.url, models=models, project_id=str(uuid.uuid4()), created=str(datetime.now()))
    if args.command == "model":
        if args.subcommand == "register":
            validate_pth_file(args.path)
            return RegisterModel(path=args.path, name=args.name)
        elif args.subcommand == "list":
            return ListModels()
    if args.command == "transform":
        models = parse_models(args.models)
        return TransformJob(path=args.path, out=args.out, models=models)
    if args.command == "split":
        return SplitJob(path=args.path, out=args.out)
    if args.command == "youtube":
        validate_youtube_url(args.url)
        return DownloadJob(url=args.url, out=args.out)
    if args.command == "tts":
        return TTS(text=args.text, out=args.out)
    if args.command == "mix":
        return Mix(vocals=args.vocals, background=args.background, out=args.out)

    raise ValueError("Unknown command")
