import requests
import json
import refreshToken
import postfortoken
import pandas as pd

def get_categories(category):

    url = f"https://sofsystem.cafe24api.com/api/v2/admin/categories/{category}/products?display_group=1"

    try:
        with open('access_data.json', 'r') as file:
            data = json.load(file)
            access_token = data.get('access_token')
            print(access_token)
    except FileNotFoundError:
        print("there is no json file")
        postfortoken.get_token()

    headers = {
        'Authorization': "Bearer " + access_token,
        'X-Cafe24-Api-Version': "2023-09-01",
        'Content-Type': "application/json"
    }

    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    product_nos = [product["product_no"] for product in response_json["products"]]
    print(product_nos)
    # getproducts.get_products(product_nos)

    # all the categories: 52, 198, 157, 42, 43, 44, 45, 46
    return product_nos

if __name__ == "__main__":
    get_categories()