from flask import Flask,render_template
from  lx import *
import pandas as pd
import numpy as np
app = Flask(__name__)

df =get_data()

@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/l1',methods=['post'])
def l1():
    data = df[df['quantity']>0].groupby('country').sum()['quantity'].sort_values(ascending=False).head(10)
    text = {}
    text['name'] =data.index.tolist()
    text['price'] = data.values.tolist()
    return text


@app.route('/l2',methods=['post'])
def l2():
    data  = df[df['quantity']>0].groupby('country').sum()['price'].sort_values(ascending=False).head(10)
    text  = {}
    text['name'] = data.index.tolist()
    text['price'] = data.values.tolist()
    return text


@app.route('/c2',methods=['post'])
def c2():
    data = df[['time','quantity','price']]
    data['month'] = pd.to_datetime(data['time']).dt.month
    data = data[data['quantity'] > 0].groupby('month').sum()['quantity']
    text = {}
    text['month'] = data.index.tolist()
    text['sum'] = data.values.tolist()
    return text

@app.route('/c1',methods=['post'])
def c1():
    data = df[['quantity','price','invoice','code','ID']]
    sumPrice = data[data['quantity']>0]['price'].sum()
    count_ID = data[data['quantity']>0]['invoice'].drop_duplicates().count()
    avgPrice = sumPrice/count_ID
    customer = data[data['quantity']>0].groupby('ID').agg({'invoice':'nunique',
                                                           'quantity':np.sum,
                                                           'price':np.sum()})
    customer.describe()




if __name__ == '__main__':
    app.run()
