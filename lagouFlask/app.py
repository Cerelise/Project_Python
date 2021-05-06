from flask import Flask,render_template,request
from conn import *
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/l1',methods=['post'])
def title():
    sql = """
        select t_job,t_edu,t_money,t_exp
        from lagou
        where t_job like "大数据%";
    """

    data = exp_data(sql)
    a,b,c,d = [],[],[],[]
    text = {}
    for i,j,k,l in data:
        a.append(i)
        b.append(j)
        c.append(k)
        d.append(l)
    max_,min_ = [],[]
    for i in c:
        start = i.split('-')[0]
        end = i.split('-')[1]


        min_.append(int(start.replace('k','000').replace('K','000')))
        max_.append(int(end.replace('k','000').replace('K','000')))

    text["job"] = a
    text["edu"] = b
    text['exp'] = d
    text["min_"] = min_
    text["max_"] = max_


    df = pd.DataFrame(text)
    df.groupby(['exp'])

    return text


@app.route('/bar',methods=['POST',"GET"])
def bar():
    sql = """
        select t_addr,count(t_addr)
        from lagou
        group by t_addr order by count(t_addr) desc limit 10;
    """

    data = exp_data(sql)
    a,b = [],[]
    for j,k in data:
        a.append(j)
        b.append(int(k))

    text = {}
    text['city'] = a
    text['Person'] = b

    return text



@app.route('/line',methods=["POST",'GET'])
def line():
    sql = """
        select t_job,count(t_job)
from lagou
where t_job like '大数据%'
group by t_job
order by count(t_job) desc
limit 30;
    """
    data = exp_data(sql)
    a,b = [],[]

    for i,j in data:
        a.append(i)
        b.append(j)
    text = {}
    text['exp'] = a
    text['per'] = b
    return text

if __name__ == '__main__':
    app.run()
