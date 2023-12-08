from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import getproductsfromcats
from templates import *
from refreshToken import refresh
import puttingtags
import getsubcats
import getproducts
import pandas as pd
import time
import asyncio


app = FastAPI()
app.secret_key = 'j1'

@app.get('/')
def index():
    refresh()
    return render_template("index.html")

@app.route('/execute_function', methods=['POST'])
def execute_function():
    global temp_cat_no

    segments = {
            "Event": 52,
            "New": 198,
            "Best": 157,
            "책상": 368,
            "테이블식탁": 381,
            "모듈책장": 387,
            "책장선반": 392,
            "행거드레스룸": 397,
            "의자": 400
    }
    option = request.json.get('selectedOption')  # Access JSON data instead of form data
    cat_no = segments[option]

    temp_cat_no = cat_no
    return redirect('/processing')


@app.route('/processing', methods=['GET'])
def processing():
    global temp_product_nos
    global temp_cat_no

    temp_product_nos = getproductsfromcats.get_categories(temp_cat_no)
    sub_cat_dict = getsubcats.get_sub_categories(temp_cat_no)

    session['sub_cat_dict'] = sub_cat_dict
    return redirect(url_for('subcats'))

@app.route('/subcats')
def subcats():
    sub_cat_dict = session.get('sub_cat_dict', {})
    return render_template("subcats.html", sub_cat_dict=sub_cat_dict)

@app.route('/processsubcats', methods=['POST'])
def process_sub_cats():
    global temp_product_nos

    cat = request.json.get('catNumber')
    temp_product_nos = getproductsfromcats.get_categories(cat)

    return redirect('/tags')

@app.route('/tags', methods=['GET'])
def tags():
    return render_template("tags.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/products')
def products():
    global temp_product_nos

    getproducts.get_products(temp_product_nos)
    
    excel_file_path = 'products_data.xlsx'

    df = pd.read_excel(excel_file_path, usecols="B,G,M,AG")
    numpy_array = df.to_numpy()

    html_table = pd.DataFrame(numpy_array, columns=df.columns).to_html(index=False)

    return render_template("products.html", html_table=html_table)

@app.route('/process_tags', methods=['POST'])
def insert_tags():
    global temp_product_nos
    data = request.json.get('selectedTags')
    puttingtags.putting_tags(data, temp_product_nos)
    temp_product_nos = []
    return jsonify(message = 'tags added')


if __name__ == '__main__':
    app.run(port= 5555, debug=True)



# https://developers.cafe24.com/docs/api/admin/#create-a-product-category for category api 

