import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Overview & Data Quality", page_icon="📊", layout="wide")
st.title("📌 Overview & Data Quality Dashboard")

# ------------------- Load Dataset with Session State -------------------
if "df" not in st.session_state or st.session_state["df"].empty:
    df, outliers_dict, _ = preprocess_data()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

st.subheader("Dataset Overview")

if df.empty:
    st.warning("No data loaded. Ensure 'application_train.csv' exists in the project folder.")
else:
    # ------------------- KPIs -------------------
    Total_Applicants = df['SK_ID_CURR'].count() if 'SK_ID_CURR' in df.columns else "N/A"
    Default_Rate = df['TARGET'].mean() * 100 if 'TARGET' in df.columns else 0
    Repaid_Rate = 100 - Default_Rate
    Total_Features = df.shape[1]
    Avg_Missing_per_Feature = df.isnull().mean().mean() * 100
    Numerical_Features = df.select_dtypes(include='number').shape[1]
    Categorical_Features = df.select_dtypes(include='object').shape[1]
    Median_Age = int(df['AGE_YEARS'].median()) if 'AGE_YEARS' in df.columns else "N/A"
    Median_Income = df['AMT_INCOME_TOTAL'].median() if 'AMT_INCOME_TOTAL' in df.columns else "N/A"
    Avg_Credit = df['AMT_CREDIT'].mean() if 'AMT_CREDIT' in df.columns else "N/A"

     # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Applicants", f"{Total_Applicants:,}" if isinstance(Total_Applicants,int) else Total_Applicants)
    col2.metric("Default Rate (%)", f"{Default_Rate:.2f}%")
    col3.metric("Repaid Rate (%)", f"{Repaid_Rate:.2f}%")
    col4.metric("Total Features", f"{Total_Features}")
    col5.metric("Avg Missing per Feature (%)", f"{Avg_Missing_per_Feature:.2f}%")

    col6, col7, col8, col9, col10 = st.columns(5)
    col6.metric("Numerical Features", Numerical_Features)
    col7.metric("Categorical Features", Categorical_Features)
    col8.metric("Median Age", f"{Median_Age}")
    col9.metric("Median Annual Income", f"{Median_Income:,.0f}")
    col10.metric("Average Credit Amount", f"{Avg_Credit:,.0f}")

    st.markdown("---")

    #=================GRAPHS============================
    st.subheader("Dataset Overview & Graphs")

    # 1. Pie / Donut — Target distribution
    if 'TARGET' in df.columns:
        st.subheader("Target Distribution (0 vs 1)")
        plt.figure()
        df['TARGET'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'])
        plt.ylabel('')
        st.pyplot(plt)

    # 2. Bar — Top 20 features by missing %
    st.subheader("Top 20 Features by Missing %")
    missing_pct = df.isnull().mean().sort_values(ascending=False).head(20) * 100
    plt.figure(figsize=(10,4))
    sns.barplot(x=missing_pct.index, y=missing_pct.values, palette='viridis')
    plt.ylabel("Missing %")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # ------------------- Histograms -------------------
    if 'AGE_YEARS' in df.columns:
        st.subheader("Age Distribution")
        plt.figure()
        sns.histplot(df['AGE_YEARS'], bins=30, kde=True, color='skyblue')
        st.pyplot(plt)

    if 'AMT_INCOME_TOTAL' in df.columns:
        st.subheader("Income Distribution")
        plt.figure()
        sns.histplot(df['AMT_INCOME_TOTAL'], bins=30, kde=True, color='lightgreen')
        st.pyplot(plt)

    if 'AMT_CREDIT' in df.columns:
        st.subheader("Credit Amount Distribution")
        plt.figure()
        sns.histplot(df['AMT_CREDIT'], bins=30, kde=True, color='salmon')
        st.pyplot(plt)

    # ------------------- Boxplots -------------------
    st.subheader("Boxplots")
    box1, box2 = st.columns(2)

    if 'AMT_INCOME_TOTAL' in df.columns:
        with box1:
            st.subheader("Income Boxplot")
            plt.figure()
            sns.boxplot(x=df['AMT_INCOME_TOTAL'], color='lightgreen')
            st.pyplot(plt)

    if 'AMT_CREDIT' in df.columns:
        with box2:
            st.subheader("Credit Amount Boxplot")
            plt.figure()
            sns.boxplot(x=df['AMT_CREDIT'], color='salmon')
            st.pyplot(plt)

    # ------------------- Countplots -------------------
    st.subheader("Categorical Distributions")
    cat1, cat2 = st.columns(2)

    if 'CODE_GENDER' in df.columns:
        with cat1:
            st.subheader("Gender")
            plt.figure()
            sns.countplot(df['CODE_GENDER'], palette='pastel')
            st.pyplot(plt)

    if 'NAME_FAMILY_STATUS' in df.columns:
        with cat2:
            st.subheader("Family Status")
            plt.figure(figsize=(6,4))
            sns.countplot(df['NAME_FAMILY_STATUS'], palette='pastel')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(plt)

    if 'NAME_EDUCATION_TYPE' in df.columns:
        st.subheader("Education Type Distribution")
        plt.figure(figsize=(6,4))
        sns.countplot(df['NAME_EDUCATION_TYPE'], palette='pastel')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)
