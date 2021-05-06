from flask import Flask, render_template
import pandas as pd
import numpy as np
from tools import *

app = Flask(import_name=__name__,
            static_folder='static',
            template_folder='template')


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/time', methods=['post'])
def time_data():
    return get_time()


data = get_data()


@app.route('/text', methods=['post'])
def text():
    new_group(data)
    s_group = data.groupby('newgroup').shopname.nunique().reset_index(name='counts')
    s_group.sort_values(by='counts', ascending=False, inplace=True)

    text = {}
    text['group'] = s_group['newgroup'].to_list()
    text['counts'] = s_group['counts'].to_list()
    text['number'] = data['newgroup'].value_counts().values.tolist()
    text['bType'] = data['newgroup'].value_counts().index.tolist()

    return text


@app.route('/price', methods=['post'])
def price():
    result = data
    result['price_cut'] = pd.cut(x=result['price'],
                                 bins=[0, 100, 200, 300, 400, 500, 600, 800, 1000, 30000],
                                 labels=['100以下', '100-200', '200-300', '300-400', '400-500', '500-600', '600-800',
                                         '800-1k', '1K以上'])
    result2 = data[data['price'] >= 1000]
    result2 = pd.cut(x=result2['price'], bins=[1000, 2000, 5000, 10000, 30000],
                                  labels=['1K-2K', '2K-5K', '5K-1W', '1W以上'])
    result3 = pd.DataFrame((result2.value_counts()/result.shape[0]).round(3))
    text = {}
    text['price'] = result.groupby('price_cut').count()['price'].index.tolist()
    text['number'] = result.groupby('price_cut').count()['price'].values.tolist()
    text['Bprice'] = result3.index.tolist()
    text['Bnumber'] = result3.values.tolist()
    return text

if __name__ == '__main__':
    app.run(debug=True)
