import argparse, urllib.parse, uuid
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen = True)
class Job:
    project_id: str
    url: str
    voice: str
    created: str

def validate_voice(voice: str):
    if voice is None:
        raise Exception("Voice null")

def validate_youtube_url(url: str):
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname is None:
        raise Exception(f"Got invalid url {url}")
    if parsed.hostname != "www.youtube.com":
        raise Exception(f"Not youtube link, got hostname {parsed.hostname}")

def parse_args() -> Job:
    parser = argparse.ArgumentParser(description="Music App")
    parser.add_argument(
        "--url", type=str, required=True,
        help="Youtube URL to process"
    )
    parser.add_argument(
        "--voice", type=str, required=True, choices=['male', 'female'],
        help="The AI voice option"
    )

    args = parser.parse_args()
    validate_youtube_url(args.url)

    project_id = str(uuid.uuid4())
    created = str(datetime.now())
    return Job(project_id, args.url, args.voice, created)


