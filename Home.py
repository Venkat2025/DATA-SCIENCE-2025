from utils.preprocessing import load_data, preprocessing
import streamlit as st

st.set_page_config(page_title="Home Credit Default Risk – Analytics Dashboard", page_icon="🏦", layout="wide")


st.title("Home Credit Default Risk – Analytics Dashboard")

st.markdown("""
# 🏦 Home Credit Default Risk Dashboard  

Welcome to the **Home Credit Default Risk Dashboard**, built with *Streamlit*.  
This dashboard explores the **Home Credit Application dataset** (`application_train.csv`) to surface insights on borrower profiles, repayment behaviors, and risk drivers.  

Use the sidebar to navigate between modules:  
* 📌 **Overview & Data Quality** – dataset structure, missing values, portfolio risk  
* 🎯 **Target & Risk Segmentation** – default patterns across demographics & segments  
* 👨‍👩‍👧 **Demographics & Household Profile** – age, family, housing, and education effects  
* 💳 **Financial Health & Affordability** – income, credit, DTI, and affordability thresholds  
* 🔍 **Correlations & Risk Drivers** – feature correlations and interactive risk slicing  

---
""")

st.markdown("---")
st.subheader("Upload / Use Default Dataset")

uploaded_file=st.file_uploader("Upload he Dataset in csv format :",type=['csv'])
if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data()    
processed_df= preprocessing(df)    
st.dataframe(processed_df.head(20))   
