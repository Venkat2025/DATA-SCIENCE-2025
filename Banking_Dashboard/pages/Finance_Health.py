import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Financial Profile Dashboard", page_icon="💰", layout="wide")
st.title("💳 Financial Profile")

# ------------------- Load Dataset with Session State -------------------
if "df" not in st.session_state or st.session_state["df"].empty:
    df, outliers_dict, _ = preprocess_data()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

if df.empty:
    st.warning("No data loaded. Ensure 'application_train.csv' exists in the project folder.")
else:
    st.subheader("Key Financial KPIs")
    
    # ------------------- KPIs -------------------
    Avg_Income = df['AMT_INCOME_TOTAL'].mean()
    Median_Income = df['AMT_INCOME_TOTAL'].median()
    Avg_Credit = df['AMT_CREDIT'].mean()
    Avg_Annuity = df['AMT_ANNUITY'].mean()
    Avg_Goods_Price = df['AMT_GOODS_PRICE'].mean() if 'AMT_GOODS_PRICE' in df.columns else 0
    Avg_DTI = df['DTI'].mean()
    Avg_LTI = df['LTI'].mean()
    Income_Gap = df[df['TARGET']==0]['AMT_INCOME_TOTAL'].mean() - df[df['TARGET']==1]['AMT_INCOME_TOTAL'].mean()
    Credit_Gap = df[df['TARGET']==0]['AMT_CREDIT'].mean() - df[df['TARGET']==1]['AMT_CREDIT'].mean()
    High_Credit_pct = (df['AMT_CREDIT'] > 1_000_000).mean() * 100
    # ------------------- Display KPIs -------------------
    col1, col2, col3,col4,col5 = st.columns(5)
    col1.metric("Avg Annual Income", f"{Avg_Income:,.0f}")
    col2.metric("Median Annual Income", f"{Median_Income:,.0f}")
    col3.metric("Avg Credit Amount", f"{Avg_Credit:,.0f}")
    col4.metric("Avg Annuity", f"{Avg_Annuity:,.0f}")
    col5.metric("Avg Goods Price", f"{Avg_Goods_Price:,.0f}")

    col6, col7, col8,col9,col10 = st.columns(5)
    col6.metric("Avg DTI", f"{Avg_DTI:.2f}")
    col7.metric("Avg Loan-to-Income (LTI)", f"{Avg_LTI:.2f}")
    col8.metric("Income Gap (Non-def − Def)", f"{Income_Gap:,.0f}")
    col9.metric("Credit Gap (Non-def − Def)", f"{Credit_Gap:,.0f}")
    col10.metric("% High Credit (>1M)", f"{High_Credit_pct:.2f}%")

    st.markdown("---")
    st.subheader("Graphs")

    # ------------------- Graphs -------------------
    # Hist -Plot
    graph_cols = ['AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY']
    for col in graph_cols:
        if col in df.columns:
            st.subheader(f"{col} Distribution")
            plt.figure(figsize=(6,4))
            plt.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black')
            plt.xlabel(col)
            plt.ylabel("Count")
            st.pyplot(plt)

    # scatter -Income vs Credit scatter
    if all(c in df.columns for c in ['AMT_INCOME_TOTAL','AMT_CREDIT']):
        st.subheader("Income vs Credit")
        plt.figure(figsize=(6,4))
        plt.scatter(df['AMT_INCOME_TOTAL'], df['AMT_CREDIT'], alpha=0.3, color='green')
        plt.xlabel("Income")
        plt.ylabel("Credit")
        st.pyplot(plt)

    # scatter - Income vs Annuity scatter
    if all(c in df.columns for c in ['AMT_INCOME_TOTAL','AMT_ANNUITY']):
        st.subheader("Income vs Annuity")
        plt.figure(figsize=(6,4))
        plt.scatter(df['AMT_INCOME_TOTAL'], df['AMT_ANNUITY'], alpha=0.3, color='purple')
        plt.xlabel("Income")
        plt.ylabel("Annuity")
        st.pyplot(plt)

    # Boxplots by Target
    for col in ['AMT_CREDIT','AMT_INCOME_TOTAL']:
        if col in df.columns and 'TARGET' in df.columns:
            st.subheader(f"{col} by Target")
            plt.figure(figsize=(6,4))
            plt.boxplot([df[df['TARGET']==0][col], df[df['TARGET']==1][col]],
                        labels=['Repaid','Default'], patch_artist=True,
                        boxprops=dict(facecolor='lightblue'))
            plt.ylabel(col)
            st.pyplot(plt)

    # ------------------- Income-Credit KDE PLOT Using Hexbin Plot -------------------
    if 'AMT_INCOME_TOTAL' in df.columns and 'AMT_CREDIT' in df.columns:
        st.subheader("Income–Credit Hexbin Plot")
        plt.figure(figsize=(6,4))
        x = df['AMT_INCOME_TOTAL']
        y = df['AMT_CREDIT']
        plt.hexbin(x, y, gridsize=50, cmap='Reds', mincnt=1)
        plt.colorbar(label='Count in bin')
        plt.xlabel("Income")
        plt.ylabel("Credit")
        plt.title("Income vs Credit Density (Hexbin)")
        st.pyplot(plt)

    # ------------------- Income Brackets vs Default Rate -------------------
    if 'AMT_INCOME_TOTAL' in df.columns and 'TARGET' in df.columns:
        st.subheader("Income Brackets vs Default Rate")
        bins = [0, 50000, 100000, 150000, 200000, 500000, 1_000_000, np.inf]
        labels = ['<50k','50-100k','100-150k','150-200k','200-500k','500k-1M','>1M']
        df['Income_Bracket'] = pd.cut(df['AMT_INCOME_TOTAL'], bins=bins, labels=labels)
        default_rate = df.groupby('Income_Bracket')['TARGET'].mean() * 100
        plt.figure(figsize=(8,4))
        default_rate.plot(kind='bar', color='orange')
        plt.ylabel("Default Rate (%)")
        plt.xlabel("Income Bracket")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Heatmap — Financial correlations
    corr_cols = ['AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY','DTI','LTI','TARGET']
    available_cols = [c for c in corr_cols if c in df.columns]
    if len(available_cols) >= 2:
        st.subheader("Financial Correlation Matrix")
        corr_matrix = df[available_cols].corr()
        plt.figure(figsize=(6,4))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        st.pyplot(plt)
