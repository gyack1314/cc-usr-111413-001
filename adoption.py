"""按窗口营业暴露聚合实际执行；不把分配当执行。"""
from assignment import registry

def execution(data):
    ids={r['canteen'] for r in registry(data)['rows']};seen=set();out={c:[0,0] for c in ids}
    for r in data['adoption']:
        key=(r['canteen'],r['window'])
        if r['canteen'] not in ids or key in seen or type(r['adopted']) is not int or r['adopted'] not in (0,1):raise ValueError('执行身份或标记非法')
        if r['meals']<=0:raise ValueError('供餐暴露非法')
        seen.add(key);out[r['canteen']][0]+=r['adopted']*r['meals'];out[r['canteen']][1]+=r['meals']
    threshold=data['adoption_threshold']
    if not 0<threshold<=1:raise ValueError('事前执行门槛非法')
    return {c:{'adoption_share':a/b if b else None,'adopted':int(a/b>=threshold) if b else None,'meals':b} for c,(a,b) in out.items()}
