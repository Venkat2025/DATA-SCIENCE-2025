import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Sample data
df = pd.DataFrame(np.random.randn(100, 4), columns=["A", "B", "C", "D"])
cat_df = pd.DataFrame({
    "Category": ["X", "Y", "Z", "W"],
    "Values": [40, 25, 20, 15]
})

st.title("📊 20 Plotly Graphs in Streamlit")

# ---- 1 & 2 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Line Chart")
    fig = px.line(df, y=["A", "B"])
    st.plotly_chart(fig)

with col2:
    st.subheader("2. Bar Chart")
    fig = px.bar(cat_df, x="Category", y="Values", color="Category")
    st.plotly_chart(fig)

# ---- 3 & 4 ----
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Scatter Plot")
    fig = px.scatter(df, x="A", y="B", color="C", size=df["D"].abs())
    st.plotly_chart(fig)

with col4:
    st.subheader("4. Area Chart")
    fig = px.area(df, y=["A", "B"])
    st.plotly_chart(fig)

# ---- 5 & 6 ----
col5, col6 = st.columns(2)

with col5:
    st.subheader("5. Pie Chart")
    fig = px.pie(cat_df, names="Category", values="Values", hole=0)
    st.plotly_chart(fig)

with col6:
    st.subheader("6. Donut Chart")
    fig = px.pie(cat_df, names="Category", values="Values", hole=0.4)
    st.plotly_chart(fig)

# ---- 7 & 8 ----
col7, col8 = st.columns(2)

with col7:
    st.subheader("7. Box Plot")
    fig = px.box(df, y=["A", "B", "C"])
    st.plotly_chart(fig)

with col8:
    st.subheader("8. Violin Plot")
    fig = px.violin(df, y="A", box=True, points="all")
    st.plotly_chart(fig)

# ---- 9 & 10 ----
col9, col10 = st.columns(2)

with col9:
    st.subheader("9. Histogram")
    fig = px.histogram(df, x="A", nbins=20, color_discrete_sequence=["skyblue"])
    st.plotly_chart(fig)

with col10:
    st.subheader("10. Density Heatmap")
    fig = px.density_heatmap(df, x="A", y="B")
    st.plotly_chart(fig)

# ---- 11 & 12 ----
col11, col12 = st.columns(2)

with col11:
    st.subheader("11. Treemap")
    fig = px.treemap(cat_df, path=["Category"], values="Values")
    st.plotly_chart(fig)

with col12:
    st.subheader("12. Sunburst")
    fig = px.sunburst(cat_df, path=["Category"], values="Values")
    st.plotly_chart(fig)

# ---- 13 & 14 ----
col13, col14 = st.columns(2)

with col13:
    st.subheader("13. Funnel Chart")
    funnel_df = pd.DataFrame({
        "stage": ["Leads", "Prospects", "Opportunities", "Won"],
        "count": [1000, 600, 300, 150]
    })
    fig = px.funnel(funnel_df, x="count", y="stage")
    st.plotly_chart(fig)

with col14:
    st.subheader("14. Waterfall Chart")
    fig = go.Figure(go.Waterfall(
        x=["Sales", "Consulting", "Support", "Licenses"],
        y=[60, 40, -20, 30],
        measure=["relative", "relative", "relative", "total"]
    ))
    st.plotly_chart(fig)

# ---- 15 & 16 ----
col15, col16 = st.columns(2)

with col15:
    st.subheader("15. Gauge Chart")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=70,
        title={"text": "Performance"},
        gauge={"axis": {"range": [0, 100]}}
    ))
    st.plotly_chart(fig)

with col16:
    st.subheader("16. Scatter 3D")
    fig = px.scatter_3d(df, x="A", y="B", z="C", color="D")
    st.plotly_chart(fig)

# ---- 17 & 18 ----
col17, col18 = st.columns(2)

with col17:
    st.subheader("17. Surface Plot")
    X, Y = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    Z = np.sin(X**2 + Y**2)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))
    st.plotly_chart(fig, key="surface_plot")   
with col18:
    st.subheader("18. Bubble Chart")
    fig = px.scatter(df, x="A", y="B", size=df["C"].abs(), color="D", hover_name=df.index)
    st.plotly_chart(fig, key="bubble_chart")   


# ---- 19 & 20 ----
col19, col20 = st.columns(2)

with col19:
    st.subheader("19. Parallel Coordinates")
    fig = px.parallel_coordinates(df, color="A", labels={"A": "A", "B": "B", "C": "C", "D": "D"})
    st.plotly_chart(fig)

with col20:
    st.subheader("20. Radar Chart (Polar)")
    radar_df = pd.DataFrame(dict(
        r=[5, 3, 4, 2, 5],
        theta=["Metric1", "Metric2", "Metric3", "Metric4", "Metric5"]
    ))
    fig = px.line_polar(radar_df, r="r", theta="theta", line_close=True)
    st.plotly_chart(fig)
