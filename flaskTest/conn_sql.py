import pymysql
import datetime

def get_time():
    time_str = datetime.datetime.now().strftime("%Y{}%m{}%d{}, %H:%M:%S")
    return time_str.format("年","月","日")


def get_conn():
    conn = pymysql.connect(
        host='10.178.98.32',
        user='ytj',
        password='123456',
        db='big_data'
    )

    cur = conn.cursor()

    return conn,cur


def close_conn(conn,cur):

    if cur:
        cur.close()
    if conn:
        conn.close()


def sql_conn(sql,*args):

    conn,cur = get_conn()
    cur.execute(sql,args)
    ret = cur.fetchall()

    close_conn(conn,cur)

    return ret




