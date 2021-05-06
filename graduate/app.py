import pandas as pd
from flask import Flask,render_template
from tools import *

app = Flask(import_name=__name__,
            static_folder='static',
            template_folder='template')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/gettime',methods=['post'])
def time_now():
    return get_time()

data = get_data()

@app.route('/text',methods=['post'])
def text():
    data_2020 = data[data['年份'] == 2020]
    data_1 = data_2020.groupby('专业名称')['总分'].agg([np.mean,np.max,np.min])
    data_1['mean'] = data_1['mean'].astype('int')
    data_1 = data_1.sort_values(by=['mean'], ascending=False)[:50]
    text = {}
    text['amean'] = data_1['mean'].tolist()
    text['amax'] = data_1['amax'].tolist()
    text['amin'] = data_1['amin'].tolist()
    text['name'] = data_1.index.tolist()
    data_2 = data_2020['专业名称'].value_counts()[:15]
    text['sname'] = data_2.index.tolist()
    text['number'] = data_2.values.tolist()
    return text




if __name__ == '__main__':
    app.run(debug=True)