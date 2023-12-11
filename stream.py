import streamlit as st
import pandas as pd
import numpy as np
import time
import refreshToken
import getsubcats
import getproductsfromcats
import puttingtags
import getproducts
import openpyxl

st.title('Sofsys Tag Update Application')
st.header("")

with st.spinner("Refreshing Access Token"):
    if refreshToken.refresh() == "Token Refreshed":
        success = st.toast('Ready to use!')
    else:
        time.sleep(5)

segments = {
    "Event": 52,
    "New": 198,
    "Best": 157,
    "책상": 368,
    "테이블식탁": 381,
    "모듈책장": 387,
    "책장선반": 392,
    "행거드레스룸": 397,
    "의자": 400
}
# st.session_state.picked_category = list(segments.keys())[0]
st.header("1 Pick Category", divider="red")
option = st.selectbox("", segments.keys())

if option: 
    if "picked_category" not in st.session_state:
        st.session_state.picked_category = option
    if "cat_no" not in st.session_state:
        st.session_state.cat_no = segments[st.session_state.picked_category]
    st.session_state.picked_category = option
    st.session_state.cat_no = segments[st.session_state.picked_category]
    
    selection = st.button("Use " + st.session_state.picked_category + " (" + str(st.session_state.cat_no) + ") to get subcategories", type="primary")
   

st.header("2 Pick Sub-Category", divider="violet")
if selection: 
    with st.spinner("Getting Subcategories"):
        sub_cat_dict = getsubcats.get_sub_categories(st.session_state.cat_no)
        if "sub_cat_dict" not in st.session_state:
            st.session_state.sub_cat_dict = sub_cat_dict
        st.session_state.sub_cat_dict = sub_cat_dict    
        
with st.form("Pick Subcategory"):
    if "sub_cat_dict" not in st.session_state:
            st.session_state.sub_cat_dict = {}
    subcat = st.selectbox("Pick Subcategory ", st.session_state.sub_cat_dict.keys())
    submit = st.form_submit_button("Submit")
    
    if submit:
        if 'picked_subcat' not in st.session_state:
            st.session_state.picked_subcat = subcat
        st.session_state.picked_subcat = subcat
        if 'pro_no' not in st.session_state:
            st.session_state.pro_no = getproductsfromcats.get_categories(st.session_state.sub_cat_dict[st.session_state.picked_subcat])
        st.session_state.pro_no = getproductsfromcats.get_categories(st.session_state.sub_cat_dict[st.session_state.picked_subcat])
        


st.header("3 Input Tags", divider="green")

with st.form("Tags"):
    if "picked_subcat" not in st.session_state:
        st.session_state.picked_subcat = ""
    st.write("Insert Tags into: " + str(st.session_state.picked_subcat))
    text = st.text_input("Tags input")
    submit = st.form_submit_button("Submit")
    
    if submit: 
        puttingtags.putting_tags(text, st.session_state.pro_no)
        getproducts.get_products(st.session_state.pro_no)
        st.toast("Submitted")
st.download_button(
    label="Download data as Excel",
    data="file",
    file_name='products_data.xlsx',
)
    
        
st.divider()