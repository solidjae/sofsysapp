import urllib.request
import os
import sys
import json
import encodings
import ssl
import keyword_getter
import pandas as pd
import plotly.express as px

ssl._create_default_https_context = ssl._create_unverified_context

client_id = "ay5oiiPc3FQUI6itxMct"
client_secret = "Rp32vUs6i_"
url  = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"

final_df = pd.DataFrame()
keyword_dict = keyword_getter.keyword_get()
def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def taking_keywords():
    key_list = list(keyword_dict.keys())
    split = split_list(key_list, 5)

    param_with_five = []
    
    for i in range(0, 1):
        for j in split[i]:
            param_with_five.append({"name": "가구/" + j, "param": [ j ]})
        requesting(param_with_five)
        param_with_five = []
    plot_chart()
    # plot_historgram()
            
def requesting(keyword):
    body = {
            "startDate": "2023-08-01",
            "endDate": "2023-09-30",
            "timeUnit": "date",
            "category": "50000004",
            "keyword" : keyword
            }
    print("inserted body: ")
    print(body)
    body = json.dumps(body)
    encoded_body = body.encode("utf-8")

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=encoded_body)
    rescode = response.read().decode("utf-8")
    print("response : ")
    
    json_res = json.loads(rescode)
    formatted = json.dumps(json_res, indent=2)
    print(formatted)
    df = create_dataframe(rescode)
    global final_df 
    final_df = pd.concat([final_df, df])
    

def create_dataframe(api_response):
    data = json.loads(api_response)
    results = data.get("results", [])
    
    rows = []

    for result in results:
        keyword = result.get("keyword", [])[0]
        
        for entry in result.get("data", []):
            row = {
                "keyword": keyword,
                "period": entry.get("period"),
                "ratio": entry.get("ratio"),
                "roas": keyword_dict[keyword]
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv('file_name.csv', index=False)
    return df

def plot_chart():
    
    fig = px.line_3d(final_df, x="period", y="ratio", z = "roas", color="keyword")

    fig.show()

# def plot_histogram():
    
#     fig = px.histogram(final_df, x="")
    
taking_keywords()