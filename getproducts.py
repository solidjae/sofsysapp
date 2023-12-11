import json
import requests
import pandas as pd

def get_products(product_nos):
    all_products = []

    for p in product_nos: 
        url = "https://sofsystem.cafe24api.com/api/v2/admin/products/" + str(p)
        with open('access_data.json', 'r') as file:
            data = json.load(file)
            access_token = data.get('access_token')
        headers = {
        'Authorization': "Bearer " + access_token,
        'X-Cafe24-Api-Version': "2023-09-01",
        'Content-Type': "application/json"
        }
        response = requests.request("GET", url, headers=headers)

        product_data = response.json()
        all_products.append(product_data["product"])

    df = pd.DataFrame(all_products)

    df.to_excel("products_data.xlsx", index=False)

if __name__ == "__main__":
    get_products()