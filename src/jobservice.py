from args import ProcessJob
import project, db, logging, music_downloader, vocal_splitter, vocal_transformer

log = logging.getLogger(__name__)

def schedule_job(job: ProcessJob):
    try:
        db.insert_job(job)
        project_folder_path = project.create_folder(job)

        downloaded_song_path = musicdownloader.download_audio(job.url, project_folder_path)
        db.update_status(job.project_id, "Raw Song Downloaded")

        vocals_path, instrumentals_path = vocalSplitter.split_raw_audio(downloaded_song_path, project_folder_path)
        db.update_status(job.project_id, "Split vocals from instrumental")

        vocaltransformer.transform_vocals(vocals_path, instrumentals_path, project_folder_path, job.models)
        #transformed_path = vocaltransformer.transform_vocals(vocals_path, folder_path, job.voice)


    except Exception as e:
        db.save_error(job.project_id, e)
    log.info(f"Created job {job.project_id}")
