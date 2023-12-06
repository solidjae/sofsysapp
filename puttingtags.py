import requests
import getproductsfromcats

def putting_tags(tags, product_list):

    list = tags.split(",")
    tag_list = []
    print(list)
    for i in list: 
        str(i).replace(' ', '')
        tag_list.append(i)
    
    print("taglist:")
    print(tag_list)
    print("prod:")
    print(product_list)
    
    # for p in product_list:
    #     url = "https://sofsystem.cafe24api.com/api/v2/admin/products/" + p
    #     payload = {
    #         "shop_no": 1,
    #         "request": {
    #         "product_tag": tag_list
    #         }
    #     }

    #     headers = {
    #         'Authorization': "Bearer H9RzcycUH1xnNzJzRdeOOF",
    #         'Content-Type': "application/json",
    #     }

    #     response = requests.put(url, json=payload, headers=headers)
    #     print(response)
        

if __name__ == "__main__":
    putting_tags()