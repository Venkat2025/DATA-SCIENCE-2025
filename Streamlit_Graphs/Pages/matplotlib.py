import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
df = pd.DataFrame(np.random.randint(0, 10, (10, 2)), columns=['a', 'b'])

st.title("📊 Matplotlib and Seaborn in Streamlit")

# ---- KPI Row ----
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="KPI 1", value=123, delta=-23)
with kpi2:
    st.metric(label="KPI 2", value=456, delta=-45)
with kpi3:
    st.metric(label="KPI 3", value=789, delta=67)
with kpi4:
    st.metric(label="KPI 4", value=1011, delta=-89)

# ---- Charts Row 1 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("Line Plot")
    plt.figure()
    plt.plot(df['a'], label="a")
    plt.plot(df['b'], label="b")
    plt.legend()
    st.pyplot(plt.gcf())

with col2:
    st.subheader("Scatter Plot")
    plt.figure()
    plt.scatter(df['a'], df['b'], c='red', marker='o')
    st.pyplot(plt.gcf())

# ---- Charts Row 2 ----
col3, col4 = st.columns(2)

with col3:
    st.subheader("Histogram")
    plt.figure()
    plt.hist(df['a'], bins=5, color='skyblue', edgecolor='black')
    st.pyplot(plt.gcf())

with col4:
    st.subheader("Box Plot")
    plt.figure()
    plt.boxplot([df['a'], df['b']], labels=['a', 'b'])
    st.pyplot(plt.gcf())

# ---- Charts Row 3 ----
col5, col6 = st.columns(2)

with col5:
    st.subheader("Pie Chart")
    plt.figure()
    plt.pie([df['a'].sum(), df['b'].sum()], labels=['a', 'b'], autopct='%1.1f%%')
    st.pyplot(plt.gcf())

with col6:
    st.subheader("Seaborn Heatmap")
    plt.figure()
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    st.pyplot(plt.gcf())
