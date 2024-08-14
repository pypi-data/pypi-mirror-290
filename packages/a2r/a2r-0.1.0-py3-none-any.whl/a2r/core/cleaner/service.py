import fnmatch
import itertools
import logging
from collections import defaultdict
from pathlib import Path
from typing import List, Any

from a2r.conf import settings
from a2r.core.cleaner.model import CleanPath
from a2r.core.safe_rm import safe_rm_service
from a2r.core.utils import rmdir
from a2r.management.cli import update_md5

logger = logging.getLogger("a2r")


class CleanManager:
    def __init__(
        self,
        config: Path,
        dry_run: bool = False,
    ):
        """
        Args:
            config: Path to configuration file in yaml format
            dry_run: If true, do not remove anything
        """
        self._config = config
        self._dry_run = dry_run

    @property
    def dry_run(self) -> bool:
        return self._dry_run

    def read_config(self) -> List[CleanPath]:
        return settings.read_config(
            self._config, constructors={"!CleanPath": clean_path_constructor}
        )

    def run(self) -> None:
        """Start cleaning procedures"""
        clean_paths = self.read_config()
        for clean_path in clean_paths:
            self.clean(clean_path)

    def clean(self, clean_path: CleanPath):
        if not clean_path.path.exists():
            logger.warning(f"Path does not exist: {clean_path}")
            return

        fmt = clean_path.fmt
        path = clean_path.path

        if clean_path.safe_clean_is_active():
            logger.info(f"Safe cleaning path: {path}")
            self._safe_clean(
                path, fmt, clean_path.safe_to_keep, clean_path.safe_reference_paths
            )

        if clean_path.conditional_clean_is_active():
            logger.info(f"Conditional cleaning path: {path}")
            self._conditional_clean(
                path,
                fmt,
                clean_path.conditional_to_keep,
                clean_path.conditional_expected_files,
            )

        if clean_path.force_clean_is_active():
            logger.info(f"Force cleaning path: {path}")
            self._force_clean(path, fmt, clean_path.force_to_keep)

    def _safe_clean(
        self, path_to_clean: Path, fmt: str, to_keep: int, reference_paths: List[Path]
    ):
        dirs_to_rm = get_dirs_to_rm(path_to_clean, fmt, to_keep)
        for path_to_rm in dirs_to_rm:
            for ref_path in reference_paths:
                update_md5(path_to_rm)
                safe_rm_service.run(
                    path_to_clean=path_to_rm,
                    path_to_keep=ref_path,
                    dry_run=self.dry_run,
                )

    def _conditional_clean(
        self, path_to_clean: Path, fmt: str, to_keep: int, expected_files: set[str]
    ):
        dirs_to_rm = get_dirs_to_rm(path_to_clean, fmt, to_keep)
        for dir_to_rm in dirs_to_rm:
            if not expected_files_are_present(dir_to_rm, expected_files):
                raise ValueError(f"Expected file missing in directory {dir_to_rm}")
            rmdir(dir_to_rm, self.dry_run)

    def _force_clean(self, path_to_clean: Path, fmt: str, to_keep: int):
        dirs_to_rm = get_dirs_to_rm(path_to_clean, fmt, to_keep)
        for dir_to_rm in dirs_to_rm:
            rmdir(dir_to_rm, self.dry_run)


def expected_files_are_present(basedir: Path, expected_files: set[str]) -> bool:
    """
    Args:
        basedir: Path to the directory to check
        expected_files: List of expected files to find into basedir

    Returns:
        True if all expected files are present, False in case of missing files or unexpected files
    """
    # Load all non-hidden files from basedir
    files = [f for f in basedir.glob("*") if f.is_file()]
    filenames = {f.name for f in files}

    # Check each pattern in expected_files
    matched = defaultdict(list)
    for expected_file in expected_files:
        this_match = [
            name for name in filenames if fnmatch.fnmatch(name, expected_file)
        ]
        if this_match:
            matched[expected_file].extend(this_match)

    missing_match = set(expected_files) - set(matched.keys())
    files_found = list(itertools.chain.from_iterable(matched.values()))
    unexpected = set(filenames) - set(files_found)

    return len(missing_match) == 0 and len(unexpected) == 0


def get_dirs_to_rm(
    path_to_clean: Path, fmt: str, to_keep: int
) -> list[Any] | list[Path]:
    """Return a list of directories to remove if the total number of directories is greater than to_keep value"""
    filtered_and_sorted_dirs = sorted([d for d in path_to_clean.glob(fmt)])

    if len(filtered_and_sorted_dirs) <= to_keep:
        return []

    # exclude the most recent to_keep dirs
    return filtered_and_sorted_dirs[:-to_keep]


def clean_path_constructor(loader, node):
    # The function is called when the constructor is necessary
    fields = loader.construct_mapping(node, deep=True)
    return CleanPath(**fields)
