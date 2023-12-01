from flask import Flask, render_template, jsonify, request
from getproductsfromcats import get_categories
from templates import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/execute_function', methods=['POST'])
def execute_function():
    data = request.json.get('selectedOption')  # Access JSON data instead of form data
    get_categories(data)
    return jsonify(message='Categories processed successfully')

@app.route('/tags')
def tags():
    return render_template("tags.html")

if __name__ == '__main__':
    app.run(debug=True)



# https://developers.cafe24.com/docs/api/admin/#create-a-product-category for category api 

