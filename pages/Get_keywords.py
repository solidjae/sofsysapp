import streamlit as st

import keyword_analysis
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

st.header("This is for Keyword")

engine = create_engine('postgresql+psycopg2://sofsys:withus4u!@sofsys.postgres.database.azure.com/postgres',connect_args={'sslmode': 'require'})
sql = 'select * from coupang_marketing where spending > 100'
df = pd.read_sql(sql, engine)


def draw_chart(df):

    two_months_df, last_year_df = keyword_analysis.make_df_with_different_date(df)
    two_months_df.drop_duplicates(subset='keyword')
    last_year_df.drop_duplicates(subset='keyword')
    fig1 = px.bar(two_months_df, x = 'keyword', y = 'ratio_change')
    two_months_df.to_csv('2months.csv')
    fig2 = px.bar(last_year_df, x = 'keyword', y = 'ratio_change')

    st.subheader("Comparing ratio between last 2 months")
    st.plotly_chart(fig1, use_container_width=True)

    st.write("Top 10 gainers for last month: ", ", ".join(two_months_df.nlargest(10, 'ratio_change')['keyword']))

    st.subheader("Comparing ratio between between last month and last year")
    st.plotly_chart(fig2, use_container_width=True)

    st.write("Top 10 gainers for last month vs last year: ", ", ".join(last_year_df.nlargest(10, 'ratio_change')['keyword']))

def query_db(chosen_campaign):
    filtered_df = df[df['campaign'] == chosen_campaign]
    df_cleaned = filtered_df[~filtered_df.isna().any(axis=1)].copy()
    df_cleaned['normalized_keyword'] = df_cleaned['keyword'].str.replace(' ', '').replace(to_replace=r'\d{3,}', value='', regex=True)


    columns_to_merge = ['normalized_keyword', 'campaign']
    columns_to_sum = ['normalized_keyword', 'impression', 'clicks', 'spending', 'ccnt', 'convamt']

    df_cleaned = df_cleaned[df_cleaned['normalized_keyword'].str.strip() != '']

    merge_df = df_cleaned[columns_to_merge]
    sum_df = df_cleaned[columns_to_sum]

    cleaned = sum_df.groupby('normalized_keyword').sum()
    cleaned['ROAS'] = cleaned['convamt'] / cleaned['spending'].replace(0, 1) # Handling division by zero

    merge_df_unique = merge_df.drop_duplicates(subset='normalized_keyword')
    merge_df_unique['normalized_keyword'] = merge_df_unique['normalized_keyword'].replace(to_replace=r'\d{'+str(3)+r',}', value='', regex=True)

    cleaned_merged = cleaned.merge(merge_df_unique, on='normalized_keyword', how='left')
    cleaned_merged = cleaned_merged[cleaned_merged['ROAS'] > 3].reset_index(drop=True)
    cleaned_merged.rename(columns={'normalized_keyword': 'keyword'}, inplace=True)
    cleaned_merged.to_csv('dasdf.csv')
    draw_chart(cleaned_merged)



with st.form("Pick Campaign"):
    sql = "select distinct campaign from coupang_marketing"
    camp_df = pd.read_sql(sql, engine)
    print(camp_df['campaign'])
    arr = []
    for c in camp_df['campaign']:
        arr.append(c)
    st.session_state.campaign = st.selectbox("Pick Campaign ", arr)
    submit = st.form_submit_button("Submit")
    
if submit:
    query_db(st.session_state.campaign)


