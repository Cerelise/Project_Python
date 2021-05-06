from flask import Flask, render_template
import pandas as pd
from tools import *
app = Flask(
    import_name=__name__,
    static_folder='static',
    template_folder='template'
)

data = get_data()


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/text',methods=['post'])
def text():
    year_sales1 = round(data.loc[:,['name','year','global_sales']].groupby('year').sum()['global_sales'],2)
    text = {}

    text['year'] = year_sales1.index.tolist()

    text['number'] = year_sales1.values.tolist()

    year_sales2 = round(data.loc[:, ['name', 'year', 'na_sales', 'eu_sales', 'jp_sales', 'other_sales']].groupby('year').sum(),2)
    text['na_sales'] = year_sales2['na_sales'].tolist()
    text['jp_sales'] = year_sales2['jp_sales'].tolist()
    text['eu_sales'] = year_sales2['eu_sales'].tolist()
    text['other_sales'] = year_sales2['other_sales'].tolist()

    plat_count = round(data.groupby('platform').agg({
        'na_sales':np.sum,
        'jp_sales':np.sum,
        'eu_sales':np.sum,
        'other_sales':np.sum
    }).reset_index().sort_values(['na_sales','jp_sales','eu_sales','other_sales'],ascending=False),2)
    plat_count['total'] = round(plat_count['na_sales']+plat_count['eu_sales']+plat_count['jp_sales']+plat_count['other_sales'],2)
    plat_count = plat_count.sort_values('total',ascending=False).head(10)
    text['platform'] = plat_count['platform'].tolist()
    text['na_sales_plat'] = plat_count['na_sales'].tolist()
    text['jp_sales_plat'] = plat_count['jp_sales'].tolist()
    text['eu_sales_plat'] = plat_count['eu_sales'].tolist()
    text['other_sales_plat'] = plat_count['other_sales'].tolist()
    text['total_plat'] = plat_count['total'].tolist()

    pub_count = round(data.groupby('publisher').agg({'na_sales': np.sum,
                                             'jp_sales': np.sum,
                                             'eu_sales': np.sum,
                                             'other_sales': np.sum}).reset_index().sort_values(
        by=['na_sales', 'jp_sales', 'eu_sales', 'other_sales'], ascending=False),2)

    pub_count['total_pub'] = round(pub_count['na_sales']+pub_count['jp_sales']+pub_count['eu_sales']+pub_count['other_sales'],2)
    pub_count = pub_count.sort_values('total_pub', ascending=False).head(10)
    text['publisher'] = pub_count['publisher'].tolist()
    text['na_sales_pub'] = pub_count['na_sales'].tolist()
    text['jp_sales_pub'] = pub_count['jp_sales'].tolist()
    text['eu_sales_pub'] = pub_count['eu_sales'].tolist()
    text['other_sales_pub'] = pub_count['other_sales'].tolist()
    text['total_pub'] = pub_count['total_pub'].tolist()
    games_top5 = data.sort_values(by=['na_sales', 'eu_sales', 'jp_sales', 'other_sales'], ascending=False).head(5)
    text['gamename'] = games_top5['name'].tolist()
    text['na_sales_gen'] = games_top5['na_sales'].tolist()
    text['eu_sales_gen'] = games_top5['eu_sales'].tolist()
    text['jp_sales_gen'] = games_top5['jp_sales'].tolist()
    text['other_sales_gen'] = games_top5['other_sales'].tolist()

    year_sales_glo_count = data.loc[:, ['name', 'year', 'global_sales']].groupby(by='year').count()
    text['global_sales'] = year_sales_glo_count['global_sales'].tolist()

    return text



if __name__ == '__main__':
    app.run(debug=True)
