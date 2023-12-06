import authCodegetter
import requests
import json


def get_token():

    url = "https://sofsystem.cafe24api.com/api/v2/oauth/token"
    code = authCodegetter.getting_auth_code()
    header = {
        "Authorization": "Basic aUNOTTFQOFZPQklrd1VmaHZ5WkFkQzpjZkY2V0xQb2NTcFhwYnQ4Z3libDhE",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://www.sofsys.co.kr/"
    }

    response = requests.post(url, headers=header, data=body).json()
    print(response)
    print("Access token: " + response.get('access_token'))

    with open('access_data.json', 'w') as file:
        json.dump(response, file)


if __name__ == "__main__":
    get_token()