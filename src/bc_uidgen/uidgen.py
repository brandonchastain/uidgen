import time
import socket

class UidGen:
    def __init__(self):
        self.ids = dict()

    def makeUid(self) -> int:
        ts = time.time_ns() // 1_000_000
        systemname = socket.gethostname()
        h = hash(systemname)

        ts_embed = int(ts) & (0xFFFFFFFF)
        name_embed = h & 0xFFFFFF
        
        if not ts_embed in self.ids:
            self.ids[ts_embed] = 0
        seqno = self.ids[ts_embed]

        res = 0
        res |= ts_embed << 48
        res |= (name_embed << 20)
        res |= (seqno & (0xFFFFFF))

        self.ids[ts_embed] = seqno + 1

        return res

gen = UidGen()

ids = set()
starttime = time.time()
count = 0
error = False
while not error:
    uid = gen.makeUid()
    if uid in ids:
        error = True
        print("Error: generated duplicate id %s" % (bin(uid)))
    ids.add(uid)
    #print(bin(uid))
    count += 1
    #time.sleep(0.00000006)
    endtime = time.time()
    if endtime - starttime >= 10:
        break

print("%s items" % (count))
    