from flask import Flask,render_template
import pymysql




app = Flask(
    import_name=__name__,
    static_folder='static',
    template_folder='template'
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test',methods=['post'])
def test():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='big_data'
    )
    cur = conn.cursor()
    sql = "select * from test2"
    cur.execute(sql)
    data = cur.fetchall()

    date,sales2017,sales2018,cos2017,cos2018 = [],[],[],[],[]
    for a,b,c,d,e in data:
        date.append(a)
        sales2017.append(b)
        sales2018.append(c)
        cos2017.append(d)
        cos2018.append(e)

    text = {}
    text['date'] = date
    text['sales2017'] = sales2017
    text['sales2018'] = sales2018
    text['cos2017'] = cos2017
    text['cos2018'] = cos2018

    cur.close()
    conn.close()
    return text

if __name__ == '__main__':
    app.run(debug=True)
