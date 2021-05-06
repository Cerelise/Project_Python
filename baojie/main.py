import re

from flask import Flask ,render_template
import pandas as pd
import numpy as np
from tools import *
import json

app = Flask(
    import_name=__name__,
    static_folder='static',
    template_folder='template'
)


data = get_data_price()

data_taitan = get_data_taitan()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/titan')
def titan():
    return render_template('titan.html')

@app.route('/typhoon')
def typhoon():
    return render_template('typhon.html')


@app.route('/typhoontest',methods=['post'])
def typhoontest():
    sql = "select * from typhoon"
    data = pd.DataFrame(exe_sql(sql),columns=['id','name','ename','city','time','max_strength','min_strength'])
    data_1 = data[['time','min_strength','max_strength','city']].dropna()
    data_1['登录强度'] = data_1['min_strength'].apply(lambda x:int(x.split('级')[0].split('+')[0]))
    data_1['巅峰强度'] = data_1['max_strength'].apply(lambda x:int(x.split('级')[0].split('+')[0]))
    data_1['登录年份'] = pd.to_datetime(data_1['time'],format='%Y年%m月%d日').dt.year
    data_1['登录月份'] = pd.to_datetime(data_1['time'],format='%Y年%m月%d日').dt.month
    data_1['city'] = data_1['city'].apply(lambda x:x.split('省')[0].split('市')[0].split('特')[0].split('新')[0].split('温')[0])
    city_data = data_1.groupby(data_1['city']).size()

    text = {}

    year_counts = data_1['登录年份'].value_counts().sort_index()

    text['time_num'] = year_counts.values.tolist()
    text['time_date'] = [str(x) for x in year_counts.index.tolist()]

    data_3 = data_1.groupby(['登录月份', '登录强度'], as_index=False)['time'].size()
    data_3 = data_3.rename(columns={'size': '登录次数'})
    data_3_pivot = data_3.pivot('登录强度','登录月份','登录次数')
    li = []
    for i in range(len(data_3_pivot.values)):
        for j in range(len(data_3_pivot.values[0])):
            t = list([i, j, data_3_pivot.values[i][j]])
            li.append(t)

    text['diagram'] = li
    text['hours'] = data_3_pivot.index.tolist()
    text['month'] = data_3_pivot.columns.tolist()

    return json.dumps(text)


@app.route('/test',methods=['post'])
def test():

    data.drop(data[data['rent_area'] < 5].index,inplace=True)
    price_data = data.groupby('dist').count()['city'].sort_values(ascending=False).head(20)
    text = {}

    text['city'] = price_data.index.tolist()
    text['number'] = price_data.values.tolist()

    mean_data = round(data.groupby('city').mean()['rent_price_listing'],2)
    text['mean_city'] = mean_data.index.tolist()
    text['price_city'] = mean_data.values.tolist()
    dist_mean = round(data.groupby('dist').mean()['rent_price_listing'],2)
    text['dist_name'] = dist_mean.index.tolist()
    text['dist_mean'] = dist_mean.values.tolist()
    type_con = data.groupby('frame_orientation').count()['type'].sort_values(ascending=False).head(10)
    text['type_name'] = type_con.index.tolist()
    text['type_num'] = type_con.values.tolist()

    layout = data[data['type'] == '合租'].groupby('layout').count()['type'].sort_values(ascending=False).head(10)
    text['la_name'] = layout.index.tolist()
    text['la_num'] = layout.values.tolist()

    city_dist = round(data[(data['type'] == '整租') & (data['city'] == '广州')].groupby('dist').mean()['rent_price_listing'],2)
    text['city_dist'] = city_dist.index.tolist()
    text['dist_num'] = city_dist.values.tolist()
    return text


@app.route('/taitan',methods=['post'])
def taitan():
    survived = data_taitan['survived'].value_counts()
    text = {}
    text['sur_num'] = survived.values.tolist()

    sex_male = data_taitan[data_taitan['sex'] == 'male'].groupby('survived').count()['sex']
    sex_female = data_taitan[data_taitan['sex'] == 'female'].groupby('survived').count()['sex']

    text['sex_male'] = sex_male.tolist()
    text['sex_female'] = sex_female.tolist()

    age_df = data_taitan.loc[:,['survived','age']]
    age_df['age'] = age_df['age'].replace('NA',np.nan)
    age_df.dropna(inplace=True)
    age_df['age'] = age_df['age'].astype(float)
    age_df['age']=  age_df['age'].astype(int)
    age_df['levels'] = pd.cut(age_df['age'],bins=[0,20,40,60,100],labels=['20岁及以下','21-40岁','41-60岁','60岁以上'])
    age_mean = round(age_df.groupby('survived')['age'].mean(),2)
    age_level = age_df.groupby(['survived','levels']).size()
    age_level = age_level.unstack()
    age_level.rename(index={0:'遇难',1:'存活'},inplace=True)

    text['death'] = age_level.loc['遇难'].values.tolist()
    text['index_'] = age_level.loc['遇难'].index.tolist()
    text['survival'] = age_level.loc['存活'].values.tolist()

    pclass_df = data_taitan.loc[:,['survived','pclass']]
    pclass_df= pclass_df.groupby(['survived','pclass']).size()
    pclass_df = pclass_df.unstack()
    pclass_df = pclass_df.rename(index={0:'遇难',1:'存活'},columns={'1st':'一等舱','2nd':'二等舱','3rd':'三等舱'})
    text['ticket'] = pclass_df.loc['遇难'].index.tolist()
    text['ticket_yu'] = pclass_df.loc['遇难'].values.tolist()
    text['ticket_cun'] = pclass_df.loc['存活'].values.tolist()

    embarked_df = data_taitan.loc[:,['survived','embarked']]
    embarked_df = embarked_df.groupby(['survived','embarked']).size()
    embarked_df =  embarked_df.unstack()
    embarked_df.rename(index={0:'遇难',1:'存活'},inplace=True)
    text['cherbourg'] = embarked_df['Cherbourg'].tolist()
    text['queenstown'] = embarked_df['Queenstown'].tolist()
    text['southampton'] = embarked_df['Southampton'].tolist()


    return text







if __name__ == '__main__':
    app.run(debug=True)