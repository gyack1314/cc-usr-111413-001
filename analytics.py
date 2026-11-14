"""当前来源准备入口。"""
import json
from common import read
from weighing import prepared
def prepare_sources():
    data=read()
    return prepared(data,data['asof'])
if __name__=="__main__":print(json.dumps(prepare_sources(),ensure_ascii=False,indent=2))
