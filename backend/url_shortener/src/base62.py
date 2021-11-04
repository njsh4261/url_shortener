from .constants import *

def encode_base62(id):
    div_list = []
    while id > 0:
        div_list.append(id % BASE62)
        id //= BASE62
    return "".join([BASE62_TABLE[i] for i in div_list[::-1]])

def decode_base62(shorten_url):
    try:
        base62_list = [BASE62_TABLE.index(c) for c in shorten_url]
        id = 0
        for i in base62_list:
            id = id * BASE62 + i
        return id
    except ValueError:
        return -1       # 404 error will be raised for a bad URL
