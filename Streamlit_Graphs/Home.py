# import streamlit as st
# import pandas as pd
# import altair as alt

# # ---------------- Load Data ----------------
# @st.cache_data
# def load_data():
#     df = pd.read_excel("C:/Users/ADMIN/Stremalit/Sample - Superstore (2).xls")
#     df["Order Date"] = pd.to_datetime(df["Order Date"])
#     return df

# df = load_data()

# st.title("📊 Superstore Sales Dashboard with Global Filters")

# # ---------------- Sidebar Filters ----------------
# st.sidebar.header("Global Filters")

# # Region filter
# region_filter = st.sidebar.multiselect(
#     "Select Region",
#     options=df["Region"].unique(),
#     default=df["Region"].unique()
# )

# # Category filter
# category_filter = st.sidebar.multiselect(
#     "Select Category",
#     options=df["Category"].unique(),
#     default=df["Category"].unique()
# )

# # Date filter
# date_range = st.sidebar.date_input(
#     "Select Date Range",
#     value=(df["Order Date"].min().date(), df["Order Date"].max().date())
# )

# # ---------------- Apply Filters ----------------
# start_date = pd.to_datetime(date_range[0])
# end_date = pd.to_datetime(date_range[1])

# df_filtered = df[
#     (df["Region"].isin(region_filter)) &
#     (df["Category"].isin(category_filter)) &
#     (df["Order Date"].between(start_date, end_date))
# ]

# st.write(f"### Filtered Data ({len(df_filtered)} rows)")
# st.dataframe(df_filtered.head())

# # ---------------- KPIs ----------------
# kpi1, kpi2, kpi3 = st.columns(3)

# with kpi1:
#     st.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")

# with kpi2:
#     st.metric("Total Profit", f"${df_filtered['Profit'].sum():,.0f}")

# with kpi3:
#     st.metric("Total Orders", f"{df_filtered['Order ID'].nunique():,}")

# # ---------------- Charts ----------------

# # Sales by Category
# st.subheader("Sales by Category")
# cat_chart = alt.Chart(df_filtered).mark_bar().encode(
#     x="Category",
#     y="sum(Sales)",
#     color="Category"
# ).properties(width=600)
# st.altair_chart(cat_chart, use_container_width=True)

# # Sales by Region
# st.subheader("Sales by Region")
# region_chart = alt.Chart(df_filtered).mark_bar().encode(
#     x="Region",
#     y="sum(Sales)",
#     color="Region"
# ).properties(width=600)
# st.altair_chart(region_chart, use_container_width=True)

# # Profit vs Sales Scatter
# st.subheader("Profit vs Sales (by Sub-Category)")
# scatter = alt.Chart(df_filtered).mark_circle(size=60).encode(
#     x="Sales",
#     y="Profit",
#     color="Sub-Category",
#     tooltip=["Sub-Category", "Sales", "Profit"]
# ).interactive()
# st.altair_chart(scatter, use_container_width=True)

# # Sales Over Time
# st.subheader("Sales Over Time")
# time_chart = alt.Chart(df_filtered).mark_line().encode(
#     x="yearmonth(Order Date)",
#     y="sum(Sales)",
#     color="Region"
# ).properties(width=700)
# st.altair_chart(time_chart, use_container_width=True)


import streamlit as st
import pandas as pd
import altair as alt

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("Sample - Superstore (2).xls")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

st.title("📊 Superstore Sales Dashboard with Inline Filters")

# ---------------- Inline Filters ----------------
st.markdown("### 🔍 Global Filters")

fcol1, fcol2, fcol3 = st.columns([1, 1, 2])

with fcol1:
    region_filter = st.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

with fcol2:
    category_filter = st.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

with fcol3:
    date_range = st.date_input(
        "Select Date Range",
        value=(df["Order Date"].min().date(), df["Order Date"].max().date())
    )

# ---------------- Apply Filters ----------------
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

df_filtered = df[
    (df["Region"].isin(region_filter)) &
    (df["Category"].isin(category_filter)) &
    (df["Order Date"].between(start_date, end_date))
]

st.write(f"### 📑 Filtered Data ({len(df_filtered)} rows)")
st.dataframe(df_filtered.head())

# ---------------- KPIs ----------------
st.markdown("### 📈 Key Metrics")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")

with kpi2:
    st.metric("Total Profit", f"${df_filtered['Profit'].sum():,.0f}")

with kpi3:
    st.metric("Total Orders", f"{df_filtered['Order ID'].nunique():,}")

# ---------------- Charts ----------------

st.markdown("### 📊 Visualizations")

# Sales by Category
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    cat_chart = alt.Chart(df_filtered).mark_bar().encode(
        x="Category",
        y="sum(Sales)",
        color="Category"
    )
    st.altair_chart(cat_chart, use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    region_chart = alt.Chart(df_filtered).mark_bar().encode(
        x="Region",
        y="sum(Sales)",
        color="Region"
    )
    st.altair_chart(region_chart, use_container_width=True)

# Profit vs Sales Scatter
st.subheader("Profit vs Sales (by Sub-Category)")
scatter = alt.Chart(df_filtered).mark_circle(size=60).encode(
    x="Sales",
    y="Profit",
    color="Sub-Category",
    tooltip=["Sub-Category", "Sales", "Profit"]
).interactive()
st.altair_chart(scatter, use_container_width=True)

# Sales Over Time
st.subheader("Sales Over Time")
time_chart = alt.Chart(df_filtered).mark_line().encode(
    x="yearmonth(Order Date)",
    y="sum(Sales)",
    color="Region"
)
st.altair_chart(time_chart, use_container_width=True)
