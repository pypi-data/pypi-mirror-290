import sys

import dbcfg

def main():
    if len(sys.argv)<2:
        print("需要附加一个参数指定配置文件名")
        return
    dbc=dbcfg.use(sys.argv[1])    #读取xxx.cfg里的配置信息
    if dbc.code!=0:
        print(dbc.info)
    cfg=dbc.cfg()           #返回指定名称的配置，不指定使用name为""的那一个
    if dbc.code!=0:
        print(dbc.info)
    db=dbc.connect()        #根据配置信息直接连接数据库，并返回相应连接，可以指定
    if dbc.code!=0:
        print(dbc.info)
    c=db.cursor()           #获取cursor
