import time
import socket

class UidGen:
    def __init__(self):
        self.ids = dict()

    def makeUid(self) -> int:
        ts = time.time()
        systemname = socket.gethostname()

        ts_embed = int(ts) & (0xFFFFFFFF)
        name_embed = (hash(systemname) & (0xFF00)) >> 8
        
        if not ts_embed in self.ids:
            self.ids[ts_embed] = 0
        seqno = self.ids[ts_embed]

        res = ts_embed << 32
        res |= (name_embed << 8)
        res |= (seqno & (0xFF))

        self.ids[ts_embed] = seqno + 1

        return res

gen = UidGen()

ids = set()

error = False
while not error:
    uid = gen.makeUid()
    if uid in ids:
        error = True
        print("Error: generated duplicate id %s" % (uid))
    ids.add(uid)
    print(uid)
    time.sleep(0.01)
    