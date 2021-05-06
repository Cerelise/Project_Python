from flask import Flask,render_template
from  tools import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')

#
# @app.route('/le',methods=['POST'])
# def le():
#     sql = """
#         select t_money,t_exp from lagou
#     """
#     data = sql_ex(sql)
#     a,b =[],[]
#     for i,j in data:
#         if j == "经验应届毕业生" or j == "经验不限":
#             continue
#         b.append(j)
#         a.append(i)
#     max_,min_ = [],[]
#
#     for i in a:
#         if '-' in i:
#             x = str(i).split('-')
#             start = x[0]
#             end = x[1]
#             max_.append(start.replace('k','000').replace('K','000'))
#             min_.append(end.replace('k','000').replace('K','000'))
#         else:
#             continue
#
#     maxYears,minYears = [],[]
#     for z in b:
#         start = z.split('-')[0]
#         end = z.split('-')[1]
#         minYears.append(int(start.replace('经验','')))
#         maxYears.append(int(end.replace('经验','').replac('年以下','1').replace('年以上','13')))
#
#     min_Y,max_Y = [],[]
#
#     for i,j in zip(min_,minYears):
#         min_Y.append([i,j])
#
#     for i,j in zip(max_,maxYears):
#         max_Y.append([i,j])
#     lis = {}
#     lis['maxY'] = max_Y
#     lis['minY'] = min_Y
#
#
#     return lis
#
#
#
# @app.route('/test',methods=["POST","GET"])
# def cen():
#     sql = """SELECT vpd.水表名,GROUP_CONCAT(vpd.采集时间), GROUP_CONCAT(vpd.上次读数),GROUP_CONCAT(vpd.当前读数)
#     FROM 一季度 AS vpd
#
#     where 采集时间  like "2019%00:30:00"
#     GROUP BY vpd.水表名
#     ;
#     """
#     data = sql_ex(sql)
#     test = {}
#     for i in range(len(data)):
#
#         if list(data[i][1].split(','))[0] == "2019-01-01 00:30:00":
#             test['name{}'.format(i)] = data[i][0]
#             test['date{}'.format(i)] = list(data[i][1].split(','))
#             test['last{}'.format(1)] = list(data[i][2].split(','))
#             test['this{}'.format(i)] = list(data[i][3].split(','))
#         else:
#             continue
#
#     return test


@app.route('/cen')
def cen():
    sql = """
        select 水表名,采集时间,当前读数
        from 四季度
        where 采集时间  like "2019%00:00:00"  and 水表名 = "司法鉴定中心";
    """
    data = sql_ex(sql)
    nameSf,timeSf,thisSf =[],[],[]
    for a,b,c in data:
        nameSf.append(a)
        timeSf.append(b.strftime('%m-%d'))
        thisSf.append(c)
    text = {}
    text['nameSf'] = nameSf
    text['timeSf'] = timeSf
    text['thisSf'] = thisSf
    return text



if __name__ == '__main__':
    app.run()
