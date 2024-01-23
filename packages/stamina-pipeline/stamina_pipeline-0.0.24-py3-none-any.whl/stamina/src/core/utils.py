def fix_path(old_path, new_sep='/'):
    """
    Will make sure all path have the same / or \.
    """
    _path = old_path.replace('\\', '/')
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('//', '/')

    if _path.endswith('/'):
        _path = _path[:-1]

    _path = _path.replace('/', new_sep)

    new_path = _path
    return new_path