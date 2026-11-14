"""食堂整群固定数量抽签的登记。"""
from common import digest
import random

def registry(data):
    rows=data['assignment'];ids=[r['canteen'] for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('食堂重复登记')
    blocks={}
    for r in rows:
        if type(r['encouraged']) is not int or r['encouraged'] not in (0,1):raise ValueError('鼓励标记非法')
        blocks.setdefault(r['block'],[]).append(r)
    for block,units in blocks.items():
        if not 0<sum(r['encouraged'] for r in units)<len(units):raise ValueError('区组没有分配变化')
    return {'rows':rows,'blocks':blocks,'digest':digest(rows)}

def draw(data,seed):
    rng=random.Random(seed);out={}
    for block,rows in sorted(registry(data)['blocks'].items()):
        treated=set(rng.sample(sorted(r['canteen'] for r in rows),sum(r['encouraged'] for r in rows)))
        out.update({r['canteen']:int(r['canteen'] in treated) for r in rows})
    return out
