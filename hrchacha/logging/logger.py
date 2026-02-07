import logging
import os
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Date/time based log placement
BASE_LOG_DIR = os.getenv("HRCHACHA_LOG_DIR")
if not BASE_LOG_DIR:
    repo_root = Path(__file__).resolve().parents[2]
    candidate_dir = repo_root / "logs"
    if os.access(repo_root, os.W_OK):
        BASE_LOG_DIR = str(candidate_dir)
    else:
        BASE_LOG_DIR = "/tmp/logs"

# Reuse a single directory per day to avoid log folder spam on reruns
timestamp_dir = datetime.now().strftime("%Y%m%d")
LOG_DIR = Path(BASE_LOG_DIR) / timestamp_dir
LOG_FILE = f"hrchacha_{datetime.now().strftime('%H%M%S')}.log"


def _build_handlers():
    handlers = [logging.StreamHandler()]
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        file_path = LOG_DIR / LOG_FILE
        handlers.append(RotatingFileHandler(file_path, maxBytes=5_000_000, backupCount=3, encoding="utf-8"))
    except Exception as e:
        # If file handler fails, continue with console-only logging
        logging.getLogger(__name__).warning(f"File logging disabled: {e}")
    return handlers


logging.basicConfig(
    handlers=_build_handlers(),
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
