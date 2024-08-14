import logging
import shutil
from pathlib import Path

logger = logging.getLogger("a2r")


def rmdir(p: Path, dry_run: bool = False) -> None:
    logger.info(f"Executing: shutil.rmtree({p})")

    if dry_run:
        return
    try:
        shutil.rmtree(p)
    except PermissionError:
        logger.warning(f"Permission denied for {p}")
    except OSError as e:
        logger.error(f"Error: {e}")
        raise e


def user_confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("OK to push to continue [Y/N]? ").lower()
    return answer == "y"
