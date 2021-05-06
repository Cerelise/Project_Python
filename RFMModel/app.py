from flask import Flask, render_template
import pandas as pd
import numpy as np
from uiilt import *

app = Flask(import_name=__name__,
            static_folder='static',
            template_folder='templates')

data = get_data()


@app.route('/')
def hello_world():
    return render_template('main.html')



@app.route('/time', methods=['post'])
def time_data():
    return get_time()



@app.route('/test', methods=['post'])
def test():
    df = data.loc[data['Quantity'] <= 0]
    tt = pd.pivot_table(df, index='year', columns='month', values='amount', aggfunc={'amount': np.sum},margins=False)
    df2 = data[(data['Quantity']>0)&(data['Price']>0)]
    pp = pd.pivot_table(df2, index='year', columns='month', values='amount', aggfunc={'amount': np.sum},margins=False)
    test  = np.abs(tt/pp)
    test = test.T.reset_index()[['month','2011']]
    test['2011'] = test['2011'].round(2)
    test['month'] = test['month'].astype(int)
    test = test.sort_values('month')


    R_value=df2.groupby('Customer ID')['date'].max()
    R_value = (df2['date'].max() - R_value).dt.days
    F_value = df2.groupby('Customer ID')['invoice'].nunique()

    M_value = df2.groupby('Customer ID')['amount'].sum()

    text = {}
    text['R_index'] = R_value.head(30).index.tolist()
    text['R_values'] = R_value.head(30).values.tolist()
    text['F_index'] = F_value.head(30).index.tolist()
    text['F_values'] =F_value.head(30).values.tolist()
    text['M_index'] = M_value[2:32].index.tolist()
    text['M_values'] = M_value[2:32].values.tolist()
    text['month'] = test['month'].to_list()
    text['sum'] = test['2011'].to_list()

    R_bins = [0,30,90,180,360,720]
    F_bins = [1,2,5,10,20,5000]
    M_bins = [0,500,2000,5000,10000,200000]
    R_score = pd.cut(R_value,R_bins,labels=[5,4,3,2,1],right=False)
    F_score = pd.cut(F_value,F_bins,labels=[1,2,3,4,5],right=False)
    M_score = pd.cut(M_value,M_bins,labels=[1,2,3,4,5],right=False)
    rmf = pd.concat([R_score,F_score,M_score],axis=1)
    rmf.rename(columns={'date':'R_score','invoice':'F_score','amount':'M_score'},inplace=True)
    for i in ['R_score','F_score','M_score']:
        rmf[i] = rmf[i].astype(float)
    rmf['R'] = np.where(rmf['R_score']>3.82,'高','低')
    rmf['F'] = np.where(rmf['F_score'] > 2.03, '高', '低')
    rmf['M'] = np.where(rmf['M_score'] > 1.89, '高', '低')
    rmf['value']=rmf['R'].str[:] + rmf['F'].str[:]+rmf['M'].str[:]
    rmf['value'] = rmf['value'].str.strip()
    def trans_value(x):
        if x =='高高高':
            return '重要价值客户'
        elif x =='底高高':
            return '重要保值客户'
        elif x =='底低高':
            return '重要挽留客户'
        elif x =='高高低':
            return '一般价值客户'
        elif x =='高低低':
            return '一般发展客户'
        elif x =='低高低':
            return '一般保持客户'
        else:
            return '一般挽留客户'
    rmf['用户等级'] = rmf['value'].apply(trans_value)

    F_value.quantile([0.1,0.2,0.3,0.4,0.5,0.9,1])
    text['用户等级'] = rmf['用户等级'].value_counts().index.tolist()
    text['人数'] = rmf['用户等级'].value_counts().values.tolist()
    return text


if __name__ == '__main__':
    app.run(debug=True)
