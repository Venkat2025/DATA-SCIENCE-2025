import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Target & Risk Segmentation", page_icon="🎯", layout="wide")
st.title("🎯 Target & Risk Segmentation Dashboard")

# ------------------- Load Dataset with Session State -------------------
if "df" not in st.session_state or st.session_state["df"].empty:
    df, outliers_dict, _ = preprocess_data()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

if df.empty or 'TARGET' not in df.columns:
    st.warning("No TARGET column found or dataset not loaded. Ensure 'application_train.csv' exists.")
else:
    st.subheader("Key KPIs")

    # ------------------- KPIs -------------------
    Total_Defaults = int(df['TARGET'].sum())
    Default_Rate = df['TARGET'].mean() * 100
    Repaid_Rate = 100 - Default_Rate

    Avg_Income_Defaulters = df[df['TARGET'] == 1]['AMT_INCOME_TOTAL'].mean()
    Avg_Credit_Defaulters = df[df['TARGET'] == 1]['AMT_CREDIT'].mean()
    Avg_Annuity_Defaulters = df[df['TARGET'] == 1]['AMT_ANNUITY'].mean() if 'AMT_ANNUITY' in df.columns else 0
    Avg_Employment_Years_Defaulters = df[df['TARGET'] == 1]['EMPLOYMENT_YEARS'].mean() if 'EMPLOYMENT_YEARS' in df.columns else 0

    # Default rate by categorical columns
    Default_Rate_by_Gender = df.groupby('CODE_GENDER')['TARGET'].mean() * 100 if 'CODE_GENDER' in df.columns else pd.Series()
    Default_Rate_by_Education = df.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean() * 100 if 'NAME_EDUCATION_TYPE' in df.columns else pd.Series()
    Default_Rate_by_Family_Status = df.groupby('NAME_FAMILY_STATUS')['TARGET'].mean() * 100 if 'NAME_FAMILY_STATUS' in df.columns else pd.Series()
    Default_Rate_by_Housing_Type = df.groupby('NAME_HOUSING_TYPE')['TARGET'].mean() * 100 if 'NAME_HOUSING_TYPE' in df.columns else pd.Series()

    # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Defaults", f"{Total_Defaults:,}")
    col2.metric("Default Rate (%)", f"{Default_Rate:.2f}%")
    col3.metric("Repaid Rate (%)", f"{Repaid_Rate:.2f}%")
    col4.metric("Avg Income - Defaulters", f"${Avg_Income_Defaulters:,.0f}")
    col5.metric("Avg Credit - Defaulters", f"${Avg_Credit_Defaulters:,.0f}")

    col6, col7, col8, col9, col10 = st.columns(5)
    col6.metric("Avg Annuity - Defaulters", f"${Avg_Annuity_Defaulters:,.0f}")
    col7.metric("Avg Employment Years - Defaulters", f"{Avg_Employment_Years_Defaulters:.1f}")
    col8.metric("Default Rate by Gender (%)", f"{Default_Rate_by_Gender.mean():.2f}" if not Default_Rate_by_Gender.empty else "N/A")
    col9.metric("Default Rate by Education (%)", f"{Default_Rate_by_Education.mean():.2f}" if not Default_Rate_by_Education.empty else "N/A")
    col10.metric("Default Rate by Family Status (%)", f"{Default_Rate_by_Family_Status.mean():.2f}" if not Default_Rate_by_Family_Status.empty else "N/A")

    st.markdown("---")
    st.subheader("Graphs")

    # Rest of the graphs remain unchanged, using df from session_state


    # ------------------- 1. Bar: Default vs Repaid -------------------
    target_counts = df['TARGET'].value_counts().reindex([0,1])
    plt.figure()
    plt.bar(['Repaid','Default'], target_counts.values, color=['#66b3ff','#ff9999'])
    plt.ylabel("Counts")
    plt.title("Default vs Repaid")
    st.pyplot(plt)

    # ------------------- 2-5. Default % by categorical -------------------
    cat_cols = ['CODE_GENDER', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE']
    for col in cat_cols:
        if col in df.columns:
            st.subheader(f"Default % by {col.replace('_',' ')}")
            default_pct = df.groupby(col)['TARGET'].mean() * 100  # Series
            plt.figure()
            plt.bar(default_pct.index, default_pct.values, color='skyblue')
            plt.ylabel("Default %")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(plt)

    # ------------------- 6-7. Boxplots: Income & Credit by Target -------------------
    st.subheader("Boxplots by Target")
    box1, box2 = st.columns(2)

    # Income by Target
    if 'AMT_INCOME_TOTAL' in df.columns:
        with box1:
            st.subheader("Income by Target")
            plot_df = df[['TARGET', 'AMT_INCOME_TOTAL']].dropna()
            income_repaid = plot_df[plot_df['TARGET']==0]['AMT_INCOME_TOTAL']
            income_default = plot_df[plot_df['TARGET']==1]['AMT_INCOME_TOTAL']
            plt.figure(figsize=(6,4))
            plt.boxplot([income_repaid, income_default], labels=['Repaid','Default'], patch_artist=True,
                        boxprops=dict(facecolor='lightgreen'))
            plt.ylabel("AMT_INCOME_TOTAL")
            st.pyplot(plt)

    # Credit by Target
    if 'AMT_CREDIT' in df.columns:
        with box2:
            st.subheader("Credit by Target")
            plot_df = df[['TARGET', 'AMT_CREDIT']].dropna()
            credit_repaid = plot_df[plot_df['TARGET']==0]['AMT_CREDIT']
            credit_default = plot_df[plot_df['TARGET']==1]['AMT_CREDIT']
            plt.figure(figsize=(6,4))
            plt.boxplot([credit_repaid, credit_default], labels=['Repaid','Default'], patch_artist=True,
                        boxprops=dict(facecolor='salmon'))
            plt.ylabel("AMT_CREDIT")
            st.pyplot(plt)

    # ------------------- 8. Violin — Age vs Target -------------------
    violin_col, hist_col = st.columns(2)
    if 'AGE_YEARS' in df.columns:
        with violin_col:
            st.subheader("Age Distribution by Target")
            plot_df = df[['TARGET', 'AGE_YEARS']].dropna()
            age_repaid = plot_df[plot_df['TARGET']==0]['AGE_YEARS']
            age_default = plot_df[plot_df['TARGET']==1]['AGE_YEARS']
            plt.figure(figsize=(6,4))
            plt.violinplot([age_repaid, age_default])
            plt.xticks([1,2], ['Repaid','Default'])
            plt.ylabel('AGE_YEARS')
            st.pyplot(plt)

    # ------------------- 9. Histogram (stacked) — EMPLOYMENT_YEARS by Target -------------------
    if 'EMPLOYMENT_YEARS' in df.columns:
        with hist_col:
            st.subheader("Employment Years by Target (Stacked)")
            plot_df = df[['TARGET', 'EMPLOYMENT_YEARS']].dropna()
            target0 = plot_df[plot_df['TARGET']==0]['EMPLOYMENT_YEARS']
            target1 = plot_df[plot_df['TARGET']==1]['EMPLOYMENT_YEARS']
            plt.figure(figsize=(6,4))
            plt.hist([target0, target1], bins=20, stacked=True, color=['skyblue','lightcoral'], label=['Repaid','Default'])
            plt.xlabel("EMPLOYMENT_YEARS")
            plt.ylabel("Count")
            plt.legend()
            st.pyplot(plt)

    # ------------------- 10. Stacked Bar — NAME_CONTRACT_TYPE vs Target -------------------
    if 'NAME_CONTRACT_TYPE' in df.columns:
        st.subheader("Contract Type vs Target (Stacked Bar)")

        # Prepare data
        contract_counts = df.groupby(['NAME_CONTRACT_TYPE','TARGET']).size().unstack(fill_value=0)
        categories = contract_counts.index.tolist()
        repaid = contract_counts[0].values
        default = contract_counts[1].values

        # Plot
        plt.figure(figsize=(6,4))
        plt.bar(categories, repaid, label='Repaid', color='#66b3ff')
        plt.bar(categories, default, bottom=repaid, label='Default', color='#ff9999')
        plt.ylabel("Counts")
        plt.xlabel("Contract Type")
        plt.xticks(rotation=45, ha='right')
        plt.title("Contract Type vs Target")
        plt.legend()
        plt.tight_layout()
        st.pyplot(plt)
