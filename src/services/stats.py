import time
STATS={"found":0,"sent":0,"start":time.time()}
def inc_found(): STATS["found"]+=1
def inc_sent(): STATS["sent"]+=1
def uptime(): return int(time.time()-STATS["start"])
