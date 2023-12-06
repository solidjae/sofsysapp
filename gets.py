import requests
import json
import refreshToken
import postfortoken


def get_categories():

    url = "https://sofsystem.cafe24api.com/api/v2/admin/categories/381"

    try:
        with open('access_data.json', 'r') as file:
            data = json.load(file)
            access_token = data.get('access_token')
            print(access_token)
    except FileNotFoundError:
        print("there is no json file")
        postfortoken.get_token()

    if access_token is None:

        refreshToken.refresh()

        with open('access_data.json', 'r') as file:
            data = json.load(file)
            access_token = data.get('access_token')

    headers = {
        'Authorization': "Bearer " + access_token,
        'Content-Type': "application/json"
    }

    response = requests.request("GET", url, headers=headers)

    response_json = response.json()

    print(json.dumps(response_json, indent=2))

    return response


if __name__ == "__main__":
    get_categories()