import streamlit as st
import keyword_analysis
import keyword_getter

st.header("This is for Keyword")

uploaded_file = st.file_uploader("Choose a xlsx file", accept_multiple_files=False)

if uploaded_file:
    pruned_df = keyword_getter.keyword_get(uploaded_file)
    key_list = keyword_analysis.taking_keywords(pruned_df)
    my_file = open("keywords.txt", "r") 
    data = my_file.read() 
    data_into_list = data.replace('\n', ', ').split(".") 
    print(data_into_list)
    for d in data_into_list:
        st.write(d)