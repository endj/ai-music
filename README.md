# AI Music CLI

## Install

* Python 3.10 =<
* FFMPEG
* pip install -r requirements.txt

## Overview
CLI is for generating AI song voice-overs.
## Commands

### `process`
Processes a song from YouTube using a specified AI model. Output is written to `projects/<randomId>/models/<model>/<model>_combined.mp3`


#### Arguments:
- `--url` (required): YouTube URL to fetch song from.
- `--models` (required): Comma-separated string of AI model names. Need to be registered with `model register` command

---

### `model register`
Registers a new AI model. Copies the pth file to `/models/<name>/<pthFile>`

#### Arguments:
- `--path` (required): Path to a `.pth` file.
- `--name` (required): Unique name of the model.

---

### `model list`
Lists available AI models.

#### Arguments:
None

---

### Event log

Sqlite file `db/music.db` contains a log of events in `projects` and `project_events` table
