import streamlit as st
import keyword_analysis
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

st.header("This is for Keyword")


def query_db(sql):
    engine = create_engine('postgresql+psycopg2://sofsys:withus4u!@sofsys.postgres.database.azure.com/postgres',connect_args={'sslmode': 'require'})

    df = pd.read_sql(sql, engine)
    print(df['campaign'].unique())
    st.session_state.campaign_list = df['campaign'].unique()

query_db('select * from coupang_marketing')

with st.form("Pick Campaign"):
    if "picked_campaign" not in st.session_state:
            st.session_state.campaign = ''
    campaign = st.selectbox("Pick Campaign ", st.session_state.campaign_list)
    submit = st.form_submit_button("Submit")

# if uploaded_file:
#     two_months_df, last_year_df = keyword_analysis.make_df_with_different_date(uploaded_file)
#     fig1 = px.bar(two_months_df, x = 'keyword', y = 'ratio_change')
#     fig2 = px.bar(last_year_df, x = 'keyword', y = 'ratio_change')

#     st.subheader("Comparing ratio between last 2 months")
#     st.plotly_chart(fig1, use_container_width=True)

#     st.write("Top 10 gainers for last month: ", ", ".join(two_months_df.nlargest(10, 'ratio_change')['keyword']))

#     st.subheader("Comparing ratio between between last month and last year")
#     st.plotly_chart(fig2, use_container_width=True)

#     st.write("Top 10 gainers for last month vs last year: ", ", ".join(last_year_df.nlargest(10, 'ratio_change')['keyword']))