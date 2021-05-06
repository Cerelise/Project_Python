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

    return text




if __name__ == '__main__':
    app.run(debug=True)