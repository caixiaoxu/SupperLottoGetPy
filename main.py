import requests
from lxml import etree
import sqlite3

# 获取期数列表
r = requests.get("http://kaijiang.500.com/dlt.shtml")
r.encoding = 'utf-8'
html = etree.HTML(r.text)
npers = html.xpath('//div[@class="iSelectList"]/a/text()')
print(npers)

# 打开数据库连接
db = sqlite3.connect("PreloadLotto.db")
cursor = db.cursor()
# 创建表
sql = "CREATE TABLE if not exists Lottery ( nper TEXT PRIMARY KEY , num1 TEXT ,num2 TEXT,num3 TEXT,num4 TEXT,num5 TEXT,num6 TEXT,num7 TEXT )"
cursor.execute(sql)

# 获取最新一条
sql = "SELECT * FROM Lottery LIMIT 1"
cursor.execute(sql)
last = cursor.fetchone()
print("之前最新一条：", last)

# 循环取网页数据
count = 0
for nper in npers:
    if (last is not None) and (last[0] == nper):
        break

    print(nper)
    # 网页请示
    r = requests.get("http://kaijiang.500.com/shtml/dlt/%s.shtml" % (nper))
    r.encoding = 'utf-8'
    # print('网页' + r.text)
    # 解析
    html = etree.HTML(r.text)
    # 取值
    result = html.xpath('//div[@class="ball_box01"]/ul/li/text()')
    print('网页值:', result)
    if 7 == len(result):
        # 写入
        sql = "INSERT OR IGNORE INTO Lottery (nper,num1,num2,num3,num4,num5,num6,num7) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            nper, result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        print("sql语句:" + sql)
        cursor.execute(sql)
    count += 1
    if 30 == count:
        db.commit()
        count = 0
# 关闭
cursor.close()
db.commit()
db.close()
