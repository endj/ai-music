from args import ProcessJob
import project, db, logging, music_downloader, vocal_splitter, vocal_transformer, sound_mixer

log = logging.getLogger(__name__)

def schedule_job(job: ProcessJob):
    try:
        db.insert_job(job)
        project_folder_path = project.create_folder(job)

        downloaded_song_path = music_downloader.download_audio(job.url, project_folder_path)
        db.update_status(job.project_id, "Raw Song Downloaded", "DOWNLOADED_FILE")

        vocals_path, instrumentals_path = vocal_splitter.split_raw_audio(downloaded_song_path, project_folder_path)
        db.update_status(job.project_id, "Split vocals from instrumental", "SPLIT_VOCALS")

        transformed = vocal_transformer.transform_vocals(vocals_path, project_folder_path, job.models)
        db.update_status(job.project_id, "Transformed Models", "TRANSFORMED_MODELS")

        sound_mixer.combine(transformed, instrumentals_path)
        db.update_status(job.project_id, "Combined outputs", "MIXED_OUTPUTS")

    except Exception as e:
        db.save_error(job.project_id, e)
    log.info(f"Created job {job.project_id}")
