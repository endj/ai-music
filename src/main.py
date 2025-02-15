import logging

import args
import common
import db
import model_service, job_orchestrator, vocal_transformer, vocal_splitter, music_downloader,tts, sound_mixer
from args import ProcessJob, ListModels, RegisterModel, TransformJob, TTS, SplitJob, DownloadJob, Mix
from pathlib import Path

log = logging.getLogger(__name__)

if __name__ == "__main__":
    common.setup_logger()
    db.migrate_db()

    cmd = args.parse_args()

    if isinstance(cmd, ProcessJob):
        log.debug(f"Processing {cmd}")
        result = model_service.has_models(cmd.models)
        if len(result.missing_models) != 0:
            raise ValueError(f"Missing models {result.missing_models}")
        job_orchestrator.schedule_job(cmd)

    if isinstance(cmd, RegisterModel):
        log.debug(f"Registering {cmd}")
        model_service.register_model(cmd)

    if isinstance(cmd, ListModels):
        log.debug("Listing models")
        model_service.list_available_models()

    if isinstance(cmd, TransformJob):
        log.debug(f"Transforming song {cmd.path} using models {cmd.models}")
        vocal_transformer.transform_vocals(cmd.path, cmd.out, cmd.models)

    if isinstance(cmd, SplitJob):
        log.info(f"Splitting vocals {cmd.path} out {cmd.out}")
        vocal_splitter.split_raw_audio(cmd.path, cmd.out)

    if isinstance(cmd, DownloadJob):
        log.info(f"Downloading song {cmd.url}")
        music_downloader.download_audio(cmd.url, cmd.out)

    if isinstance(cmd, TTS):
        log.info(f"TTS {cmd.text}")
        tts.text_to_speech(cmd.text, cmd.out)

    if isinstance(cmd, Mix):
        log.info(F"Mixing {cmd}")
        sound_mixer.mix_mp3s(Path(cmd.vocals), Path(cmd.background), Path(cmd.out))

    log.info("DONE")