import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Sample dataset
df = pd.DataFrame(np.random.randn(100, 3), columns=["A", "B", "C"])
df["Category"] = np.random.choice(["X", "Y", "Z"], size=100)

st.title("📊 Altair Charts in Streamlit")

# 1. Line Chart
st.subheader("1. Line Chart")
line = alt.Chart(df.reset_index()).mark_line().encode(
    x="index",
    y="A"
)
st.altair_chart(line, use_container_width=True)

# 2. Bar Chart
st.subheader("2. Bar Chart")
bar = alt.Chart(df).mark_bar().encode(
    x="Category",
    y="mean(A)",
    color="Category"
)
st.altair_chart(bar, use_container_width=True)

# 3. Scatter Plot
st.subheader("3. Scatter Plot")
scatter = alt.Chart(df).mark_circle(size=60).encode(
    x="A",
    y="B",
    color="Category",
    tooltip=["A", "B", "C", "Category"]
)
st.altair_chart(scatter, use_container_width=True)

# 4. Area Chart
st.subheader("4. Area Chart")
area = alt.Chart(df.reset_index()).mark_area(opacity=0.5).encode(
    x="index",
    y="A"
)
st.altair_chart(area, use_container_width=True)

# 5. Histogram
st.subheader("5. Histogram")
hist = alt.Chart(df).mark_bar().encode(
    alt.X("A", bin=True),
    y="count()"
)
st.altair_chart(hist, use_container_width=True)

# 6. Box Plot
st.subheader("6. Box Plot")
box = alt.Chart(df).mark_boxplot().encode(
    x="Category",
    y="A"
)
st.altair_chart(box, use_container_width=True)

# 7. Heatmap
st.subheader("7. Heatmap")
heatmap = alt.Chart(df).mark_rect().encode(
    x=alt.X("A", bin=alt.Bin(maxbins=20)),
    y=alt.Y("B", bin=alt.Bin(maxbins=20)),
    color="count()"
)
st.altair_chart(heatmap, use_container_width=True)


# 8. Stacked Bar
st.subheader("8. Stacked Bar")
stacked = alt.Chart(df).mark_bar().encode(
    x="Category",
    y="count()",
    color="Category"
)
st.altair_chart(stacked, use_container_width=True)

# 9. Density Line (KDE-like)
st.subheader("9. Density Estimate")
density = alt.Chart(df).transform_density(
    "A", as_=["A", "density"]
).mark_area().encode(
    x=("A:Q"),
    y=("density:Q")
)
st.altair_chart(density, use_container_width=True)

# 10. Faceted Scatter
st.subheader("10. Faceted Scatter")
facet = alt.Chart(df).mark_circle().encode(
    x="A", y="B", color="Category"
).facet(
    column="Category"
)
st.altair_chart(facet, use_container_width=True)
