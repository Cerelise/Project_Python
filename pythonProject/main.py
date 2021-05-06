from   flask import Flask,render_template
from parts import *
import pandas as pd

app = Flask(import_name=__name__,
            static_folder='static',
            template_folder='templates')


@app.route('/')
def test():
    return render_template('main.html')


@app.route('/l1',methods=[''])
def l2():
    sql = """
        select * from online_data
    """
    data = exe_sql(sql)
    df = pd.DataFrame(sql,columns=[''])


if __name__ == '__main__':
    app.run(debug=True)