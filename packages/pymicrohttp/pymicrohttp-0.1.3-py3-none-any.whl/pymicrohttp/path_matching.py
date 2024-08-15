import re


def match_path(pattern: str, path: str) -> dict | None:
    results = {}

    pattern_chunks = pattern.split('/')
    path_chunks = path.split('/')

    if len(pattern_chunks) != len(path_chunks):
        return None

    for pattern_chunk, path_chunk in zip(pattern_chunks, path_chunks):
        if pattern_chunk.startswith(':'):
            param = pattern_chunk[1:]
            results[param] = path_chunk
        elif pattern_chunk != path_chunk:
            return None

    return results

assert match_path('/:id', '/123') == {'id': '123'}
assert match_path('/u/hello', '/u/hello') == {}
assert match_path('/u/hello', '/u/error') == None

assert match_path('/u/:id/hello', '/u/uwu/hello') == { 'id': 'uwu' }
assert match_path('/g/:id/hello', '/g/1243/hello') == { 'id': '1243' }

assert match_path('/u/:id/hello', '/u/uwu/error_here') == None
assert match_path('/error_here/:id/hello', '/u/uwu/error_here') == None

assert match_path('/i/:id/:hello', '/i/uwu/somevalue') == { 'id': 'uwu', 'hello': 'somevalue' }
assert match_path('/:u/g/hello', '/uwu/g/hello') == { 'u': 'uwu' }
assert match_path('/u/:id/:group/:chnl', '/u/uwu/g1/c1') == { 'id': 'uwu', 'group': 'g1', 'chnl': 'c1' }
