import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from utils.preprocessing import preprocess_data

st.set_page_config(page_title="Correlations, Drivers & Interactive Slice-and-Dice Dashboard", page_icon="🔍", layout="wide")
st.title("🔍 Correlations, Drivers & Interactive Slice-and-Dice Profile")

# ------------------- Load Dataset -------------------
df, Outliers_Dict, _ = preprocess_data()

if df.empty:
    st.warning("No data loaded. Ensure 'application_train.csv' exists in the project folder.")
else:
    # ------------------- Sidebar Filters -------------------
    st.sidebar.header("Filters")
    Gender_Filter = st.sidebar.multiselect(
        "Select Gender", options=df['CODE_GENDER'].unique(), default=df['CODE_GENDER'].unique()
    )
    Education_Filter = st.sidebar.multiselect(
        "Select Education", options=df['NAME_EDUCATION_TYPE'].unique(), 
        default=df['NAME_EDUCATION_TYPE'].unique()
    )

    # Filter dataset based on sidebar selections
    df_filtered = df[df['CODE_GENDER'].isin(Gender_Filter) & df['NAME_EDUCATION_TYPE'].isin(Education_Filter)]

    # ------------------- KPIs -------------------
    st.subheader("Key Correlation KPIs")

    # Select numeric columns relevant for correlations
    Numeric_Cols = [
        'AGE_YEARS','AMT_CREDIT','AMT_INCOME_TOTAL','AMT_ANNUITY',
        'EMPLOYMENT_YEARS','CNT_FAM_MEMBERS','DTI','LTI','TARGET'
    ]
    Numeric_Cols = [c for c in Numeric_Cols if c in df_filtered.columns]

    # Compute correlation matrix if we have at least 2 numeric columns
    Corr_Matrix = df_filtered[Numeric_Cols].corr() if len(Numeric_Cols) >= 2 else pd.DataFrame()
    
    if not Corr_Matrix.empty:
        # Correlation with TARGET column
        Target_Corr = Corr_Matrix['TARGET'].drop('TARGET', errors='ignore').sort_values()
        
        # ------------------- KPI Calculations -------------------
        Top5_Pos_Corr = Target_Corr[Target_Corr > 0].tail(5)
        Top5_Neg_Corr = Target_Corr[Target_Corr < 0].head(5)
        Most_Corr_Income = Corr_Matrix['AMT_INCOME_TOTAL'].drop('AMT_INCOME_TOTAL', errors='ignore').idxmax()
        Most_Corr_Credit = Corr_Matrix['AMT_CREDIT'].drop('AMT_CREDIT', errors='ignore').idxmax()
        Corr_Income_Credit = Corr_Matrix.loc['AMT_INCOME_TOTAL','AMT_CREDIT']
        Corr_Age_Target = Corr_Matrix.loc['AGE_YEARS','TARGET'] if 'AGE_YEARS' in Corr_Matrix else None
        Corr_Employment_Target = Corr_Matrix.loc['EMPLOYMENT_YEARS','TARGET'] if 'EMPLOYMENT_YEARS' in Corr_Matrix else None
        Corr_Family_Target = Corr_Matrix.loc['CNT_FAM_MEMBERS','TARGET'] if 'CNT_FAM_MEMBERS' in Corr_Matrix else None
        Var_Explained = (Target_Corr.abs().sort_values(ascending=False).head(5)**2).sum()
        High_Corr_Features = Target_Corr[abs(Target_Corr) > 0.5]

        # ------------------- Display KPIs -------------------
        C1, C2, C3, C4, C5 = st.columns(5)
        C1.metric("Top 5 +Corr (TARGET)", ", ".join(Top5_Pos_Corr.index))
        C2.metric("Top 5 −Corr (TARGET)", ", ".join(Top5_Neg_Corr.index))
        C3.metric("Most Corr w/ Income", Most_Corr_Income)
        C4.metric("Most Corr w/ Credit", Most_Corr_Credit)
        C5.metric("Corr(Income, Credit)", f"{Corr_Income_Credit:.2f}")

        C6, C7, C8, C9, C10 = st.columns(5)
        C6.metric("Corr(Age, TARGET)", f"{Corr_Age_Target:.2f}" if Corr_Age_Target is not None else "N/A")
        C7.metric("Corr(Employment, TARGET)", f"{Corr_Employment_Target:.2f}" if Corr_Employment_Target is not None else "N/A")
        C8.metric("Corr(Family Size, TARGET)", f"{Corr_Family_Target:.2f}" if Corr_Family_Target is not None else "N/A")
        C9.metric("Variance Explained (Top 5)", f"{Var_Explained:.2f}")
        C10.metric("# Features |corr| > 0.5", str(len(High_Corr_Features)))

    st.markdown("---")
    st.subheader("Graphs")

    # ------------------- 1. Correlation Heatmap -------------------
    if not Corr_Matrix.empty:
        st.subheader("Correlation Heatmap")
        plt.figure(figsize=(8,5))
        sns.heatmap(Corr_Matrix, annot=True, cmap='coolwarm', fmt=".2f")
        st.pyplot(plt)

    # ------------------- 2. Bar |Correlation| vs TARGET -------------------
    if not Target_Corr.empty:
        st.subheader("Top |Correlation| with TARGET")
        plt.figure(figsize=(7,4))
        sns.barplot(x=Target_Corr.abs().sort_values(ascending=False).index,
                    y=Target_Corr.abs().sort_values(ascending=False).values, palette='viridis')
        plt.ylabel("|Correlation|")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # ------------------- 3. Scatter: Age vs Credit -------------------
    if all(c in df_filtered.columns for c in ['AGE_YEARS','AMT_CREDIT','TARGET']):
        st.subheader("Age vs Credit by TARGET")
        plt.figure(figsize=(6,4))
        sns.scatterplot(x='AGE_YEARS', y='AMT_CREDIT', hue='TARGET', data=df_filtered, alpha=0.6, palette='Set1')
        plt.xlabel("Age")
        plt.ylabel("Credit")
        st.pyplot(plt)

    # ------------------- 4. Scatter: Age vs Income -------------------
    if all(c in df_filtered.columns for c in ['AGE_YEARS','AMT_INCOME_TOTAL','TARGET']):
        st.subheader("Age vs Income by TARGET")
        plt.figure(figsize=(6,4))
        sns.scatterplot(x='AGE_YEARS', y='AMT_INCOME_TOTAL', hue='TARGET', data=df_filtered, alpha=0.6, palette='Set2')
        plt.xlabel("Age")
        plt.ylabel("Income")
        st.pyplot(plt)

    # ------------------- 5. Scatter: Employment Years vs TARGET -------------------
    if all(c in df_filtered.columns for c in ['EMPLOYMENT_YEARS','TARGET']):
        st.subheader("Employment Years vs TARGET")
        plt.figure(figsize=(6,4))
        sns.stripplot(x='TARGET', y='EMPLOYMENT_YEARS', data=df_filtered, jitter=0.2, palette='Set3')
        plt.xlabel("TARGET")
        plt.ylabel("Employment Years")
        st.pyplot(plt)

    # ------------------- 6. Boxplot: Credit by Education -------------------
    if all(c in df_filtered.columns for c in ['AMT_CREDIT','NAME_EDUCATION_TYPE']):
        st.subheader("Credit by Education")
        plt.figure(figsize=(6,4))
        sns.boxplot(x='NAME_EDUCATION_TYPE', y='AMT_CREDIT', data=df_filtered, palette='Pastel1')
        plt.xticks(rotation=45)
        plt.ylabel("Credit")
        st.pyplot(plt)

    # ------------------- 7. Boxplot: Income by Family Status -------------------
    if all(c in df_filtered.columns for c in ['AMT_INCOME_TOTAL','NAME_FAMILY_STATUS']):
        st.subheader("Income by Family Status")
        plt.figure(figsize=(6,4))
        sns.boxplot(x='NAME_FAMILY_STATUS', y='AMT_INCOME_TOTAL', data=df_filtered, palette='Pastel2')
        plt.xticks(rotation=45)
        plt.ylabel("Income")
        st.pyplot(plt)

    #-----------------------Pair Plot ncome, Credit, Annuity, TARGET----------------
    Pair_Cols = ['AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY','TARGET']
    Pair_Cols = [c for c in Pair_Cols if c in df_filtered.columns]
    if len(Pair_Cols) >= 2:
        st.subheader("Pair Plot")
        sns.pairplot(df_filtered[Pair_Cols], hue='TARGET' if 'TARGET' in Pair_Cols else None, palette='Set1')
        st.pyplot(plt)


    # ------------------- 9. Filtered Bar: Default Rate by Gender -------------------
    if all(c in df_filtered.columns for c in ['CODE_GENDER','TARGET']):
        st.subheader("Default Rate by Gender")
        Gender_Default = df_filtered.groupby('CODE_GENDER')['TARGET'].mean()*100
        plt.figure(figsize=(5,4))
        sns.barplot(x=Gender_Default.index, y=Gender_Default.values, palette='cool')
        plt.ylabel("Default Rate (%)")
        st.pyplot(plt)

    # ------------------- 10. Filtered Bar: Default Rate by Education -------------------
    if all(c in df_filtered.columns for c in ['NAME_EDUCATION_TYPE','TARGET']):
        st.subheader("Default Rate by Education")
        Edu_Default = df_filtered.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean()*100
        plt.figure(figsize=(6,4))
        sns.barplot(x=Edu_Default.index, y=Edu_Default.values, palette='magma')
        plt.xticks(rotation=45)
        plt.ylabel("Default Rate (%)")
        st.pyplot(plt)

