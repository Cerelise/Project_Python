from flask import Flask,render_template
import pandas as pd
import numpy as np
from tools import *

app = Flask(import_name=__name__,
            static_folder='static',
            template_folder='template')


data = get_data()

@app.route('/')
def main():

    return render_template('main.html')



@app.route('/time',methods=['post'])
def time_data():
    return get_time()


@app.route('/text',methods=['post'])
def text():
    pv_daily = data.groupby('date').count()['user'].rename('pv')
    uv_daily = data.groupby('date')['user'].apply(lambda x:x.drop_duplicates().count())
    pv_uv_daily = pd.concat([pv_daily,uv_daily],axis=1)


if __name__ == '__main__':
    app.run(debug=True)