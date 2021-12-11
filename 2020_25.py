from itertools import count

SAMPLE = False
pks = (8184785, 5293040) if not SAMPLE else (17807724, 5764801)

def loop_size(pk: int) -> int:
    v = 1
    sn = 7
    for i in count():
        v *= sn
        v = v % 20201227
        if v == pk:
            return i + 1
    return -1

def comp(sn: int, ls: int) -> int:
    v = 1
    for i in range(ls):
        v *= sn
        v = v % 20201227
    return v


lss = list(map(loop_size, pks))

for i in range(2):
    print(comp(pks[i], lss[(i + 1) % 2]))