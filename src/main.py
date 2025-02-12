import logging

import args
import common
import db
import model_service, job_orchestrator
from args import ProcessJob, ListModels, RegisterModel

log = logging.getLogger(__name__)

if __name__ == "__main__":
    common.setup_logger()
    db.migrate_db()

    command = args.parse_args()

    if isinstance(command, ProcessJob):
        log.debug(f"Processing {command}")
        result = model_service.has_models(command.models)
        if len(result.missing_models) != 0:
            raise ValueError(f"Missing models {result.missing_models}")
        job_orchestrator.schedule_job(command)
    elif isinstance(command, RegisterModel):
        log.debug(f"Registering {command}")
        model_service.register_model(command)
    elif isinstance(command, ListModels):
        log.debug("Listing models")
        model_service.list_available_models()
    else:
        raise ValueError("Unknown job typ")
