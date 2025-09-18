import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample dataset
df = pd.DataFrame(np.random.randn(100, 4), columns=["A", "B", "C", "D"])

st.title("📊 20 Seaborn Graphs in Streamlit")

# ---- 1 & 2 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Line Plot")
    plt.figure()
    sns.lineplot(data=df[["A", "B"]])
    st.pyplot(plt.gcf())

with col2:
    st.subheader("2. Scatter Plot")
    plt.figure()
    sns.scatterplot(x="A", y="B", hue="C", size="D", data=df)
    st.pyplot(plt.gcf())

# ---- 3 & 4 ----
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Histogram")
    plt.figure()
    sns.histplot(df["A"], bins=20, kde=True, color="skyblue")
    st.pyplot(plt.gcf())

with col4:
    st.subheader("4. KDE Plot")
    plt.figure()
    sns.kdeplot(df["A"], shade=True, color="red")
    st.pyplot(plt.gcf())

# ---- 5 & 6 ----
col5, col6 = st.columns(2)

with col5:
    st.subheader("5. Box Plot")
    plt.figure()
    sns.boxplot(data=df)
    st.pyplot(plt.gcf())

with col6:
    st.subheader("6. Violin Plot")
    plt.figure()
    sns.violinplot(data=df)
    st.pyplot(plt.gcf())

# ---- 7 & 8 ----
col7, col8 = st.columns(2)

with col7:
    st.subheader("7. Strip Plot")
    plt.figure()
    sns.stripplot(data=df, jitter=True)
    st.pyplot(plt.gcf())

with col8:
    st.subheader("8. Swarm Plot")
    plt.figure()
    sns.swarmplot(data=df)
    st.pyplot(plt.gcf())

# ---- 9 & 10 ----
col9, col10 = st.columns(2)

with col9:
    st.subheader("9. Heatmap")
    plt.figure()
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    st.pyplot(plt.gcf())

with col10:
    st.subheader("10. Pairplot")
    plt.figure()
    sns.pairplot(df)
    st.pyplot(plt.gcf())

# ---- 11 & 12 ----
col11, col12 = st.columns(2)

with col11:
    st.subheader("11. Joint Plot (Scatter + KDE)")
    plt.figure()
    sns.jointplot(x="A", y="B", data=df, kind="kde")
    st.pyplot(plt.gcf())

with col12:
    st.subheader("12. Regression Plot")
    plt.figure()
    sns.regplot(x="A", y="B", data=df)
    st.pyplot(plt.gcf())

# ---- 13 & 14 ----
col13, col14 = st.columns(2)

with col13:
    st.subheader("13. Residual Plot")
    plt.figure()
    sns.residplot(x="A", y="B", data=df)
    st.pyplot(plt.gcf())

with col14:
    st.subheader("14. Rug Plot")
    plt.figure()
    sns.rugplot(df["A"])
    st.pyplot(plt.gcf())

# ---- 15 & 16 ----
col15, col16 = st.columns(2)

with col15:
    st.subheader("15. Count Plot")
    plt.figure()
    sns.countplot(x=pd.cut(df["A"], bins=5))
    st.pyplot(plt.gcf())

with col16:
    st.subheader("16. ECDF Plot")
    plt.figure()
    sns.ecdfplot(df["A"])
    st.pyplot(plt.gcf())

# ---- 17 & 18 ----
col17, col18 = st.columns(2)

with col17:
    st.subheader("17. Hexbin (via JointPlot)")
    plt.figure()
    sns.jointplot(x="A", y="B", data=df, kind="hex")
    st.pyplot(plt.gcf())

with col18:
    st.subheader("18. Hist with Hue")
    plt.figure()
    sns.histplot(df, x="A", hue=pd.cut(df["B"], bins=3), multiple="stack")
    st.pyplot(plt.gcf())

# ---- 19 & 20 ----
col19, col20 = st.columns(2)

with col19:
    st.subheader("19. KDE with Multiple Columns")
    plt.figure()
    sns.kdeplot(df["A"], shade=True, color="blue")
    sns.kdeplot(df["B"], shade=True, color="green")
    st.pyplot(plt.gcf())

with col20:
    st.subheader("20. FacetGrid Example")
    g = sns.FacetGrid(df, col="C", col_wrap=3)
    g.map_dataframe(sns.scatterplot, x="A", y="B")
    st.pyplot(g.fig)
