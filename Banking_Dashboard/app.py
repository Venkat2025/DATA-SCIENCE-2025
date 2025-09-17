import streamlit as st
from utils.preprocessing import preprocess_data

st.set_page_config(
    page_title="Home Credit Default Risk Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Home Credit Default Risk Dashboard")
st.markdown("""

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

# ------------------- File Upload ( -------------------
uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])

# ------------------- Load Dataset -------------------
if "df" not in st.session_state:
    source = uploaded_file if uploaded_file else "application_train_10000.csv"
    try:
        df, outliers_dict, _ = preprocess_data(source)
        st.session_state["df"] = df
        st.session_state["outliers_dict"] = outliers_dict
        st.success("Dataset loaded successfully.")
    except FileNotFoundError:
        st.error("Dataset not found. Please upload a CSV file.")

# ------------------- Display Dataset -------------------
if "df" in st.session_state:
    df = st.session_state["df"]

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())
    st.write(f"**Shape:** {df.shape[0]:,} rows × {df.shape[1]:,} columns")

    if st.session_state.get("outliers_dict"):
        st.subheader("📈 Outlier Summary")
        total_outliers = 0
        for col, outliers in st.session_state["outliers_dict"].items():
            st.write(f"**{col}:** {len(outliers)} outliers detected")
        st.write(f"**Total Outliers:** {total_outliers}")
    st.subheader("💾 Download Processed Dataset")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label="📥 Download CSV",data=csv,file_name="processed_dataset.csv",mime="text/csv")
