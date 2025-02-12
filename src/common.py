import logging as log

RED = "\033[31m"
RESET = "\033[0m"

class RedErrorFormatter(log.Formatter):
    def format(self, record):
        msg = super().format(record)
        if record.levelno == log.ERROR:  # Only color error messages red
            return f"{RED}{msg}{RESET}"
        return msg  # Keep everything else default

def setup_logger():
    log.basicConfig(level=log.INFO,
                    format="%(levelname)s[%(asctime)s]: %(message)s",
                    datefmt="%Y%m%d_%H:%M:%SZ",
                    handlers=[log.StreamHandler()]
                    )
    logger = log.getLogger()
    for handler in logger.handlers:
        handler.setFormatter(RedErrorFormatter("%(levelname)s[%(asctime)s]: %(message)s"))
