import requests
import json
import postfortoken



def refresh():

    
    with open('access_data.json', 'r') as file:
        data = json.load(file)
        if "refresh_token" in data:
            refresh_token = data.get('refresh_token')
            url = "https://sofsystem.cafe24api.com/api/v2/oauth/token"
            header = {
                "Authorization": "Basic aUNOTTFQOFZPQklrd1VmaHZ5WkFkQzpjZkY2V0xQb2NTcFhwYnQ4Z3libDhE",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            body = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            response = requests.post(url, headers=header, data=body).json()
            with open('access_data.json', 'w') as file:
                json.dump(response, file)
            print(response)
            print("token refreshed")
            return "Token Refreshed"
        else:
            print("refresh token error, getting new token")
            postfortoken.get_token()
            return "Error, regenerating token"


if __name__ == "__main__":
    refresh()