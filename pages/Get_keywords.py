import streamlit as st
import keyword_analysis
import plotly.express as px

st.header("This is for Keyword")

uploaded_file = st.file_uploader("Choose a xlsx file", accept_multiple_files=False)

if uploaded_file:
    two_months_df, last_year_df = keyword_analysis.make_df_with_different_date(uploaded_file)
    fig1 = px.bar(two_months_df, x = 'keyword', y = 'ratio_change')
    fig2 = px.bar(last_year_df, x = 'keyword', y = 'ratio_change')

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
