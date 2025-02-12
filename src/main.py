import common, db, args, logging, project, jobservice, vocalSplitter, vocaltransformer

log = logging.getLogger(__name__)

if __name__ == "__main__":
    common.setup_logger()
    db.migrate_db()

   # vocalSplitter.split_raw_audio("../projects/6ff6fde7-92db-44b7-81b7-533c21139707/Symphony Of Destruction.mp3", "../projects/6ff6fde7-92db-44b7-81b7-533c21139707")
   # vocaltransformer.transform_vocals("../projects/6ff6fde7-92db-44b7-81b7-533c21139707/htdemucs/Symphony Of Destruction/vocals.mp3", "../projects/6ff6fde7-92db-44b7-81b7-533c21139707","male")
    job = args.parse_args()
    jobservice.schedule_job(job)


