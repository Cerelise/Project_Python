from flask import Flask,render_template
from parts import *
import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/time',methods=['POST'])
def get_time():
    now = get_date()
    return now


@app.route('/l1',methods=['POST'])
def l1():
    sql = """
        select user_id,birthday from sam_tianchi_mum_baby
    """
    data = ex_sql(sql)
    data = pd.DataFrame(data,columns=['id','date'])
    data['year'] = pd.to_datetime(data['date'],format='%Y%m%d')
    df = data.groupby(data['year'].dt.year).count()
    df1= df[8:]
    a = []
    b = df1['year'].mean()
    for i in df1['year']:
        k = i / b * 10
        a.append(round(k, 2))
    text = {}
    c= []
    for i in df1.index:
        c.append(i)
    text['year'] = c
    text['lv'] = a
    return text

@app.route('/l2',methods=['POST'])
def l2():
    sql = """
        select buy_mount,day from sam_tianchi_mum_baby_trade_history
    """
    data = ex_sql(sql)
    df = pd.DataFrame(data, columns=['sum', 'day'])
    df['year'] = pd.to_datetime(df['day'], format="%Y%m%d")
    data = df.groupby(df['year'].dt.year).sum()
    day,sumT =[],[]
    for i in data.index:
        day.append(i)
    for i in data['sum']:
        sumT.append(i)
    text = {}
    text['day'] = day
    text['sumT'] = sumT
    return text


@app.route('/r1',methods=['POST'])
def r1():
    sql = """
            select user_id,birthday from sam_tianchi_mum_baby
        """
    data = ex_sql(sql)
    data = pd.DataFrame(data, columns=['id', 'date'])
    data['year'] = pd.to_datetime(data['date'], format='%Y%m%d')
    df = data.groupby(data['year'].dt.year).count()
    df = df[1:]
    a = []
    for i in df['year']:
        a.append(i)
    text = {}
    c = []
    for i in df.index:
        c.append(i)
    text['year'] = c
    text['lv'] = a

    return text




@app.route('/r2',methods=['POST'])
def r2():
    sql = """
            select user_id,birthday from sam_tianchi_mum_baby
        """
    data = ex_sql(sql)
    data = pd.DataFrame(data, columns=['id', 'date'])
    data['year'] = pd.to_datetime(data['date'], format='%Y%m%d')
    df = data.groupby(data['year'].dt.year).count()
    a = []
    su = 0
    for i in df['year']:
        a.append(i)
        su += i
    text = {}
    c = []
    for i in df.index:
        c.append(i)

    a.insert(0,su)
    c.insert(0,'全年')

    sum = []
    x = a[0]
    for i in range(1, len(a)):
        sum.append(x - a[i])
        x = x - a[i]
    sum.insert(0,0)
    text['year'] = c
    text['lv'] = a
    text['lvM'] = sum
    return text


@app.route('/c1',methods=['post'])
def c1():
    sql = """
        select cat_id,count(cat_id) from sam_tianchi_mum_baby_trade_history group by cat_id order by count(cat_id) desc limit 10
    """
    data = ex_sql(sql)
    catId,sumCat = [],[]
    for a,b in data:
       catId.append(a)
       sumCat.append(b)
    text = {}
    text['cat'] = catId
    text['sum'] = sumCat

    return text


@app.route('/c2',methods=['post'])
def c2():
    sql = """
        select day,auction_id from sam_tianchi_mum_baby_trade_history
    """
    data = ex_sql(sql)
    data = pd.DataFrame(data)
    data['day'] =pd.to_datetime(data[0],format="%Y%m%d")
    df = data.groupby(data['day'].dt.year).sum()
    a = []
    for i in df[1]:
        a.append(round((i / 1000000000000),2))
    date = []
    for i in df.index:
        date.append(i)
    text = {}
    text['sal'] = a
    text['year'] = date
    return text





if __name__ == '__main__':
    app.run()
