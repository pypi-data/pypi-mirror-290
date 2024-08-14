from a2r.core.safe_rm import service as safe_rm_service


def start(*args, **kwargs):
    safe_rm_service.run(*args, **kwargs)
