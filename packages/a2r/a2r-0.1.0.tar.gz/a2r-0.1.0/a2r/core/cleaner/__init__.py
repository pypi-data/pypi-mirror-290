from a2r.core.cleaner.model import CleanPath
from a2r.core.cleaner.service import CleanManager


def start(*args, **kwargs):
    clean_manager = CleanManager(*args, **kwargs)
    clean_manager.run()


def clean_path_constructor(loader, node):
    # The function is called when the constructor is needed
    fields = loader.construct_mapping(node, deep=True)
    return CleanPath(**fields)
