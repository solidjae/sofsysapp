from flask import Flask, render_template, jsonify, request
import getproductsfromcats
from templates import *
from refreshToken import refresh
import puttingtags
import getsubcats
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    refresh()
    return render_template("index.html")

@app.route('/execute_function', methods=['POST'])
def execute_function():
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
    getsubcats.get_sub_categories(cat_no)
    product_nos = getproductsfromcats.get_categories()
    global temp_product_nos
    temp_product_nos = product_nos
    return jsonify(message='Categories processed successfully')

@app.route('/loading')
def loading():
    return render_template("loading_screen.html")

@app.route('/tags')
def tags():
    return render_template("tags.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/products')
def products():
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
