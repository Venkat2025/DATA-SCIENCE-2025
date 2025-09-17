import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.preprocessing import preprocess_data

st.set_page_config(page_title=" Demographics & Household Profile", page_icon="🎯", layout="wide")
st.title("👨‍👩‍👧 Demographics & Household Profile")

# ------------------- Load Dataset with Session State -------------------
if "df" not in st.session_state or st.session_state["df"].empty:
    df, outliers_dict, _ = preprocess_data()
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

if df.empty:
    st.warning("No data loaded. Ensure 'application_train.csv' exists in the project folder.")
else:
    st.subheader("Key KPIs")
    Male_vs_Female = df['CODE_GENDER'].value_counts(normalize=True).mean()*100
    Avg_Age_Defaulters = df[df['TARGET']==1]['AGE_YEARS'].mean() if 'AGE_YEARS' in df.columns else 0
    Avg_Age_Non_Defaulters = df[df['TARGET']==0]['AGE_YEARS'].mean() if 'AGE_YEARS' in df.columns else 0
    with_children = (df['HAS_CHILDREN'].mean() * 100) if 'HAS_CHILDREN' in df.columns else 0
    Avg_Family_Size = df['FAMILY_SIZE'].mean() if 'FAMILY_SIZE' in df.columns else 0
    Married_vs_Single = df['IS_MARRIED'].value_counts(normalize=True) * 100 if 'IS_MARRIED' in df.columns else 0
    Higher_Education = (df['NAME_EDUCATION_TYPE'].isin(['Higher education','Academic degree']).mean())*100
    Living_With_Parents = (df['NAME_HOUSING_TYPE'].eq('With parents').mean()) * 100
    Currently_Working = (df['DAYS_EMPLOYED'] != 365243).mean() * 100
    Average_Employment_Years = (-df['DAYS_EMPLOYED'][df['DAYS_EMPLOYED'] != 365243].mean()) / 365

    # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Male_vs_Female (%)", f"{Male_vs_Female:.2f} %")
    col2.metric("Avg_Age_Defaulters", f"{Avg_Age_Defaulters:.2f}")
    col3.metric(" Avg_Age_Non_Defaulters ", f"{ Avg_Age_Non_Defaulters:.2f}")
    col4.metric("with_children (%)", f"{with_children:.2f}%")
    col5.metric("Avg_Family_Size ", f"{Avg_Family_Size:.2f}")

    col6, col7, col8, col9, col10= st.columns(5)
    col6.metric("Married_vs_Single(Married)", f"{Married_vs_Single.get(1,0):.2f}%")
    col7.metric("Married_vs_Single (Single)", f"{Married_vs_Single.get(0,0):.2f}%")
    col8.metric("Higher_Education", f"{Higher_Education:.2f}%")
    col9.metric("Living_With_Parents", f"{Living_With_Parents:.2f}%")
    col10.metric("Currently_Working", f"{Currently_Working:,.2f}%")
 
    col11 = st.columns(1)[0]
    col11.metric("Average_Employment_Years", f"{Average_Employment_Years:.2f}")

    st.markdown("---")
    st.subheader("Graphs")

    # ------------------- 1. Histograms — Age by all -------------------
    if 'AGE_YEARS' in df.columns:
        st.subheader("Age Distribution (All)")
        plt.figure(figsize=(6,4))
        plt.hist(df['AGE_YEARS'].dropna(), bins=20, color='skyblue', edgecolor='black')
        plt.xlabel("Age (Years)")
        plt.ylabel("Count")
        plt.title("Age Distribution (All)")
        st.pyplot(plt)

    # ------------------- 2. Histogram — Age by Target (overlay) -------------------
    if 'AGE_YEARS' in df.columns and 'TARGET' in df.columns:
        st.subheader("Age Distribution by Target")
        age_repaid = df[df['TARGET']==0]['AGE_YEARS'].dropna()
        age_default = df[df['TARGET']==1]['AGE_YEARS'].dropna()
        plt.figure(figsize=(6,4))
        plt.hist(age_repaid, bins=20, alpha=0.7, label='Repaid', color='green', edgecolor='black')
        plt.hist(age_default, bins=20, alpha=0.7, label='Default', color='red', edgecolor='black')
        plt.xlabel("Age (Years)")
        plt.ylabel("Count")
        plt.title("Age Distribution by Target")
        plt.legend()
        st.pyplot(plt)

    # ------------------- 3-6. Bar charts  -------------------
    bar_cols = st.columns(2)

    # Gender Distribution (left)
    if 'CODE_GENDER' in df.columns:
        with bar_cols[0]:
            gender_counts = df['CODE_GENDER'].value_counts()
            plt.figure(figsize=(4,4))
            plt.bar(gender_counts.index, gender_counts.values, color=['#66b3ff','#ff9999'])
            plt.ylabel("Count")
            plt.title("Gender Distribution")
            plt.tight_layout()
            st.pyplot(plt)

    # Family Status Distribution (right)
    if 'NAME_FAMILY_STATUS' in df.columns:
        with bar_cols[1]:
            family_counts = df['NAME_FAMILY_STATUS'].value_counts()
            plt.figure(figsize=(5,4))
            plt.bar(family_counts.index, family_counts.values, color='lightgreen')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Count")
            plt.title("Family Status Distribution")
            plt.tight_layout()
            st.pyplot(plt)

    # Education Distribution (left)
    if 'NAME_EDUCATION_TYPE' in df.columns:
        with bar_cols[0]:
            edu_counts = df['NAME_EDUCATION_TYPE'].value_counts()
            plt.figure(figsize=(5,4))
            plt.bar(edu_counts.index, edu_counts.values, color='orange')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Count")
            plt.title("Education Distribution")
            plt.tight_layout()
            st.pyplot(plt)

    # Occupation Distribution (Top 10) (right)
    if 'OCCUPATION_TYPE' in df.columns:
        with bar_cols[1]:
            occ_counts = df['OCCUPATION_TYPE'].value_counts().head(10)
            plt.figure(figsize=(6,4))
            plt.bar(occ_counts.index, occ_counts.values, color='purple')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("Count")
            plt.title("Top 10 Occupations")
            plt.tight_layout()
            st.pyplot(plt)

    # Pie — Housing Type
    if 'NAME_HOUSING_TYPE' in df.columns:
        st.subheader("Housing Type Distribution")  
        housing_counts = df['NAME_HOUSING_TYPE'].value_counts()
        explode = [0.1 if (count / housing_counts.sum() * 100) > 5 else 0 for count in housing_counts]
        plt.figure(figsize=(5,5))
        plt.pie(
            housing_counts.values,labels=housing_counts.index,autopct='%1.1f%%',startangle=90,colors=sns.color_palette('pastel'),
            explode=explode)
        plt.title("Housing Type Distribution")
        st.pyplot(plt.gcf())
        
    # Countplot — CNT_CHILDREN
    if 'CNT_CHILDREN' in df.columns:
        st.subheader("Children Count Distribution")
        children_counts = df['CNT_CHILDREN'].value_counts().sort_index()
        plt.figure(figsize=(6,4))
        plt.bar(children_counts.index.astype(str), children_counts.values, color='teal')
        plt.xlabel("Number of Children")
        plt.ylabel("Count")
        plt.title("Children Count Distribution")
        st.pyplot(plt)

    # Boxplot — Age vs Target
    if 'AGE_YEARS' in df.columns and 'TARGET' in df.columns:
        st.subheader("Age vs Target")
        age_repaid = df[df['TARGET']==0]['AGE_YEARS']
        age_default = df[df['TARGET']==1]['AGE_YEARS']
        plt.figure(figsize=(6,4))
        plt.boxplot([age_repaid, age_default], labels=['Repaid','Default'], patch_artist=True,
                        boxprops=dict(facecolor='lightblue'))
        plt.ylabel("Age (Years)")
        st.pyplot(plt)

    # Heatmap — Corr(Age, Children, Family Size, TARGET)
    corr_cols = ['AGE_YEARS','CNT_CHILDREN','CNT_FAM_MEMBERS','TARGET']
    available_cols = [c for c in corr_cols if c in df.columns]
    if len(available_cols) >= 2:
        st.subheader("Correlation Matrix")
        corr_matrix = df[available_cols].corr()
        plt.figure(figsize=(5,4))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        st.pyplot(plt)
    


