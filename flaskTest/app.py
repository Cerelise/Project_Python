from flask import Flask, render_template, redirect, request, jsonify
from conn_sql import *
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/aaa')
def aaa():
    return render_template('test.html')


@app.route('/time', methods=["POST"])
def time():
    return get_time()


@app.route('/bbb', methods=["POST"])
def bbb():
    sql = """
        select sum(confirm) confirm ,sum(confirm_add) confirm_add,sum(heal) heal,sum(dead) dead from details
    """

    data = sql_conn(sql)
    text = []
    text.append(int(data[0][0]))
    text.append(int(data[0][1]))
    text.append(int(data[0][2]))
    text.append(int(data[0][3]))
    a = {}
    a['confirm'] = text[0]
    a['confirm_add'] = text[1]
    a['heal'] = text[2]
    a['dead'] = text[3]
    ret = json.dumps(a)
    return ret


@app.route('/l1', methods=["POST"])
def tt():
    sql = """
        select ds,confirm,suspect,heal,dead from history
    """

    data = sql_conn(sql)
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)

    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


@app.route('/ajax', methods=["POST", "GET"])
def ajax():
    name = request.values.get("name")
    score = request.values.get("score")
    print(f"name:{name},score:{score}")
    return "10000"



@app.route('/l2', methods=["POST"])
def l2():
    sql = """
        select ds,confirm_add,suspect_add from history
    """
    data = sql_conn(sql)
    ds, conf, suspe = [], [], []
    text = {}
    for a, b, c in data:
        ds.append(a.strftime("%Y-%m-%d"))
        conf.append(b)
        suspe.append(c)
    text["ds"] = ds
    text["conf"] = conf
    text["suspe"] = suspe
    return text


@app.route('/r1', methods=["POST"])
def r1():
    sql = """
        select province,sum(confirm),sum(heal),sum(dead)
        from details group by province order by sum(confirm)  limit 7;
    """
    data = sql_conn(sql)
    province, confirm, heal, dead = [], [], [], []
    text = {}
    for a, b, c, d in data:
        province.append(a)
        confirm.append(int(b))
        heal.append(int(c))
        dead.append(int(d))
    text["province"] = province
    text["confirm"] = confirm
    text["heal"] = heal
    text["dead"] = dead
    return text




@app.route('/c2', methods=["POST"])
def c2():
    sql = """
        select province,sum(confirm),sum(heal),sum(dead)
        from details group by province  order by sum(confirm)  limit 10"""
    data = sql_conn(sql)
    province, confirm, heal, dead = [], [], [], []
    text = {}
    for a, b, c, d in data:
        province.append(a)
        confirm.append(int(b))
        heal.append(int(c))
        dead.append(int(d))
    text["province"] = province
    text["confirm"] = confirm
    text["heal"] = heal
    text["dead"] = dead
    return text


@app.route('/r2',methods=["POST"])
def r2():
    sql ="""
        select province,sum(confirm),sum(heal),sum(confirm_add),sum(dead) from details group by province order by  sum(confirm) asc  limit 5
    """

    data = sql_conn(sql)
    province, confirm, heal,con_add,dead = [], [], [],[],[]
    text = {}
    for a, b, c,d,e in data:
        province.append(a)
        confirm.append(int(b))
        heal.append(int(c))
        con_add.append(int(d))

        dead.append(int(e))

    text["province"] = province
    text["confirm"] = confirm
    text["heal"] = heal
    text["con_add"] = con_add
    text["de_add"] = dead
    return text



if __name__ == '__main__':
    app.run()
