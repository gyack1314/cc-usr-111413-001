"""食堂湿重和供餐量的已知时点摘要。"""
from common import latest,number
from assignment import registry
from adoption import execution

def prepared(data,asof):
    units=registry(data)['rows'];adopt=execution(data);out=[]
    weights=latest(data['weighings'],'id',asof)
    for r in weights:
        if r['canteen'] not in adopt or r['meals']<=0 or r['waste_kg'] is not None and number(r['waste_kg'])<0:raise ValueError('称重资料非法')
    for unit in units:
        rows=[r for r in weights if r['canteen']==unit['canteen']];obs=[r for r in rows if r['waste_kg'] is not None]
        meals=sum(r['meals'] for r in obs);out.append(dict(unit,execution=adopt[unit['canteen']],observed_meals=meals,missing_weighings=len(rows)-len(obs),wet_kg=sum(r['waste_kg'] for r in obs),weighings=[r['id'] for r in rows]))
    return out
