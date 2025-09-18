import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
df=pd.DataFrame(np.random.randint(0,10,(10,2)),columns=['a','b'])
print(df.head())
kpi1,kpi2,kpi3,kpi4=st.columns(4)
with kpi1:
    st.metric(label="KPI 1",value=123,delta=-23)
with kpi2:  
    st.metric(label="KPI 2",value=456,delta=-45)
with kpi3:
    st.metric(label="KPI 3",value=789,delta=67)
with kpi4:
    st.metric(label="KPI 4",value=1011,delta=-89)
col1,col2=st.columns(2)
with col1:
    st.title("First Column")
    st.line_chart(df)
with col2:
    st.title("Second Column")
    st.area_chart(df)

st.bar_chart(df)