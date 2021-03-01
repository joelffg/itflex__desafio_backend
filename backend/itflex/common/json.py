from json import dumps as json_dumps, loads


def dumps(data):
    if not data:
        return ""

    return json_dumps(data)


__all__ = ["dumps", "loads"]

