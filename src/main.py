import args
import common
import db
import logging
import modelservice, jobservice, vocal_splitter, vocal_transformer
from args import ProcessJob, ListModels, RegisterModel

log = logging.getLogger(__name__)

if __name__ == "__main__":
    common.setup_logger()
    db.migrate_db()


    vocal_transformer.transform_vocals(
        vocals_path="../projects/6ff6fde7-92db-44b7-81b7-533c21139707/split/vocals.mp3",
        instrumental_path="../projects/6ff6fde7-92db-44b7-81b7-533c21139707/split/no_vocals.mp3",
        output_path="../projects/6ff6fde7-92db-44b7-81b7-533c21139707",
        models=["mercury"]
    )
    os.exit(0)

    command = args.parse_args()

    if isinstance(command, ProcessJob):
        log.debug(f"Processing {command}")
        result = modelservice.has_models(command.models)
        if len(result.missing_models) != 0:
            raise ValueError(f"Missing models {result.missing_models}")
        #jobservice.schedule_job(command)
    elif isinstance(command, RegisterModel):
        log.debug(f"Registering {command}")
        modelservice.register_model(command)
    elif isinstance(command, ListModels):
        log.debug("Listing models")
        modelservice.list_available_models()
    else:
        raise ValueError("Unknown job typ")
