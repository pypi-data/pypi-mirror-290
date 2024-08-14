# dbcfg本身

dbcfg的python包。包含python的库以及dbcfg本身。

有关dbcfg的文档请参考

https://gitee.com/chenc224/dbcfg/blob/master/README.md

# 安装

使用

```
pip install dbcfg
```
即可下载安装

# 使用方法

```
import dbcfg
dbc=dbcfg.use("xxx")
print(dbc.dbtype)       #输出数据库类型，如mysql
db=dbc.connect()        #返回数据库连接
```

