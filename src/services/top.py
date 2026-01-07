TOP=[]
def add_deal(p):
    TOP.append(p)
    if len(TOP)>10: TOP.pop(0)
def get_top(): return TOP
