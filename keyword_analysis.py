import urllib.request
import os
import sys
import json
import encodings
import ssl
import keyword_getter
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
ssl._create_default_https_context = ssl._create_unverified_context

client_id = "PvUZc4rvI25p0PSUWj_J"
client_secret = "ht4yToUsez"
url  = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"

today = datetime.now()

first_day_current_month = today.replace(day=1)
last_day_last_month = first_day_current_month - timedelta(days=1)
first_day_last_month = last_day_last_month.replace(day=1)

last_day_2_months = first_day_last_month - timedelta(days=1)
first_day_2_months = last_day_2_months.replace(day=1)

first_day_last_year = first_day_last_month.replace(year=first_day_last_month.year-1)
last_day_last_year = last_day_last_month.replace(year=last_day_last_month.year-1)


def date_into_string(date):
    return str(date.year) + "-" + str(date.month) + "-" + str(date.day).zfill(2)

def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def make_df_with_different_date(excel):
   
    keyword_df = keyword_getter.keyword_get(excel)

    last_month_df = setting_up_requests(keyword_df, date_into_string(first_day_last_month), date_into_string(last_day_last_month))
    two_months_ago_df = setting_up_requests(keyword_df, date_into_string(first_day_2_months), date_into_string(last_day_2_months))
    last_year_df = setting_up_requests(keyword_df, date_into_string(first_day_last_year), date_into_string(last_day_last_year))
    
    two_months_to_last_month_df = pd.merge(last_month_df, two_months_ago_df, on="keyword", suffixes=('_last_month', '_2months_ago'))
    two_months_to_last_month_df['ratio_change'] = two_months_to_last_month_df['ratio_last_month'] - two_months_to_last_month_df['ratio_2months_ago']
    result_2_vs_last_df = two_months_to_last_month_df[['keyword', 'ratio_2months_ago', 'ratio_last_month', 'ratio_change']]

    last_month_to_last_year_df = pd.merge(last_month_df, last_year_df, on="keyword",  suffixes=('_last_month', '_last_year'))
    last_month_to_last_year_df['ratio_change'] = last_month_to_last_year_df['ratio_last_month'] - last_month_to_last_year_df['ratio_last_year']
    result_last_month_vs_year = last_month_to_last_year_df[['keyword', 'ratio_last_year', 'ratio_last_month', 'ratio_change']]

    result_2_vs_last_df = result_2_vs_last_df[result_2_vs_last_df['keyword'] != keyword_df['campaign'][0]].sort_values(by='ratio_change', ascending=False).reset_index(drop=True)
    result_last_month_vs_year = result_last_month_vs_year[result_last_month_vs_year['keyword'] != keyword_df['campaign'][0]].sort_values(by='ratio_change', ascending=False).reset_index(drop=True)
    return result_2_vs_last_df, result_last_month_vs_year
    
# take in keywords from the keyword_getter and plug in values for the api 

def setting_up_requests(keyword_df, startdate, enddate):
    
    # receive keyword df from the keyword_getter and make the keywords into a list
    
    key_list = list(keyword_df['keyword'])
    split = split_list(key_list, 4)

    param_with_five = [
        {"name": f"가구/{keyword_df['campaign'][0]}", "param": [keyword_df['campaign'][0]]}
    ]
    
    final_df = pd.DataFrame()

    for chunk in split:

        param_with_five.extend(
            {"name": f"가구/{keyword}", "param": [keyword]} for keyword in chunk
        )
        
        final_df = requesting(param_with_five, startdate, enddate, final_df)

        param_with_five = [
            {"name": f"가구/{keyword_df['campaign'][0]}", "param": [keyword_df['campaign'][0]]}
        ]

    return final_df


# requesting is being run in a loop

def requesting(keyword, startdate, enddate, final_df):
    body = {
            "startDate": startdate,
            "endDate": enddate,
            "timeUnit": "month",
            "category": "50000004",
            "keyword" : keyword
            }

    body = json.dumps(body)

    encoded_body = body.encode("utf-8")

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=encoded_body)
    rescode = response.read().decode("utf-8")
    
    json_res = json.loads(rescode)

    normalized = pd.json_normalize(
        json_res['results'], 
        record_path=['data'], 
        meta=['title', 'keyword'],
        sep='_',
        errors='ignore'
    )
    normalized['keyword'] = normalized['keyword']

    final_df = pd.concat([final_df, normalized], ignore_index=True)
    final_df = final_df[['keyword', 'ratio', 'period']]
    return final_df


# def plot_chart(df, title):

#     fig = px.bar(df, x="keyword", y="ratio_change", title=title)
#     fig.show()
    # keyword_list = list(low_df['keyword'])
    # with open('keywords.txt', 'w') as f:
    #     for line in keyword_list:
    #         f.write(line)
    #         f.write('\n')
    # print(keyword_list)
    # return keyword_list

if __name__ == "__main__":
    make_df_with_different_date()
