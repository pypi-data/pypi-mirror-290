import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from rich.progress import track

from a2r.conf import settings
from a2r.core.utils import user_confirm

logger = logging.getLogger("a2r")


def load_files(
    root_dir: Path, exclude_dirs: List[Path] = None
) -> Dict[str, List[Path]]:
    """
    Use information MD5_FILE to load the file form the filesystem
    Args:
        root_dir: Root dir to load
        exclude_dirs: List of directories to exclude when loading
    Returns:
        A dict with the md5 as a key and the list of files associated with the same md5
    """
    if exclude_dirs is None:
        exclude_dirs = []
    ########################
    # LOADING MD5_FILE
    ########################
    logger.info(f"Searching recursively {settings.MD5_FILE} in {root_dir}")
    md5_files = [
        f for f in root_dir.rglob(settings.MD5_FILE) if f.parent not in exclude_dirs
    ]

    ########################
    # LOAD MD5_FILE CONTENT
    ########################
    files_found_dict = defaultdict(list)
    total_files = len(md5_files)
    for count, md5_f in enumerate(md5_files):
        md5_files_dict = read_md5_file(md5_f)

        for md5, file_list in track(
            md5_files_dict.items(),
            description=f"- ({count + 1}/{total_files}) {md5_f}:",
            show_speed=True,
        ):
            if len(file_list) == 0:
                continue
            files_found_dict[md5].extend(file_list)

    return files_found_dict


def read_md5_file(md5_file: Path) -> Dict[str, List[Path]]:
    """
    Read the md5 file composed as a list of pair: 'MD5 filename'
    Args:
        md5_file: path of md5 file
    Returns:
        A dict with the md5 as a key and the list of files associated with the same md5
    """
    md5_file_dict = defaultdict(list)
    root = md5_file.parent

    with open(md5_file) as f:
        md5_file_list = f.read().splitlines()

    if len(md5_file_list) == 0:
        logger.warning(f"{md5_file} is empty")
        return md5_file_dict

    for md5_filename in md5_file_list:
        md5, filename, *_ = md5_filename.split()
        logger.debug(f"Read: {md5} {filename}")

        current_file = root / filename
        md5_file_dict[md5].append(current_file)

    return md5_file_dict


def start_cleaning(
    to_keep: Dict[str, List[Path]],
    to_clean: Dict[str, List[Path]],
    dry_run: bool,
) -> (List[Path], List[Path]):
    """
    Remove from filesystem all the files from files_to_clean if a match is found with reference file.
    The match is based on the md5 and the filename.
    Both conditions must be satisfied to delete the file
    Args:
        to_keep: Dict with the map md5 and files used as reference
        to_clean: Dict with the map md5 and files to clean
        dry_run: If True, no delete action is executed, only log is printed
    """
    deleted = []
    not_deleted = []
    not_exists_file = []

    for md5, current_files_to_clean in to_clean.items():
        if md5 not in to_keep:
            files_not_deleted = [f.as_posix() for f in current_files_to_clean]
            logger.info(
                f"Nothing to clean for md5: {md5} - files: {', '.join(files_not_deleted)}"
            )
            not_deleted.extend(current_files_to_clean)
            continue

        current_files_to_keep = to_keep[md5]

        # extract files that have also filename in common
        current_filenames_to_keep = {f.name for f in current_files_to_keep}
        current_filenames_to_clean = {f.name for f in current_files_to_clean}

        # get filenames in common in two lists
        filenames_to_clean = current_filenames_to_keep & current_filenames_to_clean

        # remove a file only if both md5 and filename match
        files_to_clean = [
            f for f in current_files_to_clean if f.name in filenames_to_clean
        ]
        files_not_to_clean = [
            f for f in current_files_to_clean if f.name not in filenames_to_clean
        ]

        # update statistics
        not_deleted.extend(files_not_to_clean)

        for current_file in files_to_clean:
            logger.info(f"rm {current_file.as_posix()}")

            if not current_file.exists():
                not_exists_file.append(current_file)
                continue

            if not dry_run:
                os.remove(current_file)
                deleted.append(current_file)

    return deleted, not_deleted, not_exists_file


def rm(dry_run: bool, file_to_remove: Path) -> bool:
    """
    Remove a file from filesystem
    Args:
        dry_run: If True print only log information
        file_to_remove: Absolute path of the file to remove
    """
    if not file_to_remove.exists():
        return False
    if not dry_run:
        os.remove(file_to_remove)
    return True


def run(
    path_to_keep: Path,
    path_to_clean: Path,
    force_mode: bool,
    dry_run: bool,
):
    ########################
    # PRINT INFO TO USER
    ########################
    logger.info(f"To keep: '{path_to_keep.as_posix()}'")
    logger.info(f"To clean: '{path_to_clean.as_posix()}'")

    if dry_run:
        logger.info("Dry run enable, file deletion disabled")

    if force_mode:
        logger.info("Force mode enabled")
    elif not user_confirm():
        logger.info("Exiting...")
        exit(0)

    ########################
    # LOAD FILES TO KEEP
    ########################
    logger.info(f"Loading reference files from: {path_to_keep}")
    # if dir_to_keep contains also dir_to_clean, this is excluded to avoid a clean with itself
    reference_files = load_files(path_to_keep, exclude_dirs=[path_to_clean])

    ########################
    # LOAD FILES TO REMOVE
    ########################
    logger.info(f"Loading files to clean from: {path_to_clean}")
    files_to_clean = load_files(path_to_clean)

    ########################
    # CLEANING
    ########################
    deleted, not_deleted, not_exists = start_cleaning(
        reference_files, files_to_clean, dry_run
    )

    n_deleted = len(deleted)
    n_not_deleted = len(not_deleted)
    n_not_exists = len(not_exists)
    total = n_deleted + n_not_deleted + n_not_exists
    logger.info(f"Total file analyzed: {total}")
    logger.info(f"Deleted: {n_deleted}/{total}")
    logger.info(f"Not exists: {n_not_exists}/{total}")
    logger.info(f"Not deleted: {n_not_deleted}/{total}")

    for file_not_deleted in not_deleted:
        logger.debug(f"Not deleted: {file_not_deleted}")
