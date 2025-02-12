from args import Job
import project, db, logging, musicdownloader, vocalSplitter, vocaltransformer

log = logging.getLogger(__name__)

def schedule_job(job: Job):
    try:
        db.insert_job(job)
        folder_path = project.create_folder(job)

        output_file = musicdownloader.download_audio(job.url, folder_path, job.project_id)
        db.update_status(job.project_id, "Raw Song Downloaded")

        (vocals_path, other) = vocalSplitter.split_raw_audio(output_file, folder_path)
        db.update_status(job.project_id, "Split vocals from instrumental")
        log.info(f"Split vocals into {vocals_path} and {other}")

        #transformed_path = vocaltransformer.transform_vocals(vocals_path, folder_path, job.voice)


    except Exception as e:
        db.save_error(job.project_id, e)
    log.info(f"Created job {job.project_id}")
