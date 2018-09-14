def make_limit_and_offset(request_get):
    try:
        limit = int(request_get['limit'])
    except KeyError or TypeError:
        limit = 100
    try:
        offset = int(request_get['offset'])
    except KeyError or TypeError:
        offset = 0
    return limit, offset
