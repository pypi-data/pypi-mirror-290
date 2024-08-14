import hashlib
from pathlib import Path

from a2r.conf import settings


def from_file(f: Path, chunk_size: int = 8192) -> str:
    """

    Args:
        f: Path to the file.
        chunk_size: Size of each chunk to read from the file.

    Returns:
        The MD5 hash of the file as a hexadecimal string.
    """
    md5_hash = hashlib.md5()

    with f.open("rb") as fp:
        for chunk in iter(lambda: fp.read(chunk_size), b""):  # Read the file in chunks
            md5_hash.update(chunk)  # Update the hash object with each chunk

    return md5_hash.hexdigest()


def md5_glob(p: Path, **kwargs) -> (Path, str):
    files = [f for f in p.glob("*") if f.is_file() and f.name != settings.MD5_FILE]

    for f in files:
        yield f, from_file(f, **kwargs)


def update_dir_md5(path: Path, **kwargs):
    md5_f = path / settings.MD5_FILE
    content = {}
    file_content = {}

    # read input files content if exists
    if md5_f.exists():
        with md5_f.open("r") as fp:
            data = fp.readlines()
        # revert file order from 'md5 filename' to 'filename md5'
        file_content = {row.split()[1]: row.split()[0] for row in data}

    # check if f is present
    for f, md5 in md5_glob(path, **kwargs):
        if f.name not in file_content:
            content[md5] = f.name

    for md5, f in content.items():
        with md5_f.open("a") as fp:
            fp.write(f"{md5} {f}\n")
