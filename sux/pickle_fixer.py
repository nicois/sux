"""
To work around the problem of python3 not properly unpickling
python2's datetime objects.

Taken from http://stackoverflow.com/questions/22840092/unpickling-data-from-python-2-with-unicode-strings-in-python-3
"""


def bytes_to_unicode(ob):
    t = type(ob)
    if t in (list, tuple):
        l = [str(i, 'utf-8') if type(i) is bytes else i for i in ob]
        l = [bytes_to_unicode(i) if type(i) in (list, tuple, dict) else i
            for i in l]
        ro = tuple(l) if t is tuple else l
    elif t is dict:
        byte_keys = [i for i in ob if type(i) is bytes]
        for bk in byte_keys:
            v = ob[bk]
            del(ob[bk])
            ob[str(bk, 'utf-8')] = v
        for k in ob:
            if type(ob[k]) is bytes:
                ob[k] = str(ob[k], 'utf-8')
            elif type(ob[k]) in (list, tuple, dict):
                ob[k] = bytes_to_unicode(ob[k])
        ro = ob
    else:
        ro = ob
    return ro
