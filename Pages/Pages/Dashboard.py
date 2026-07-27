import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Rare Disease Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# Load CSS
# ----------------------------------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/orphanet_cleaned.csv")

df = load_data()

# ----------------------------------------------------
# Hero Banner
# ----------------------------------------------------
st.markdown("""
<div style="
background:linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb);
padding:35px;
border-radius:18px;
color:white;
margin-bottom:25px;
box-shadow:0 10px 25px rgba(0,0,0,.25);
">

<h1 style="margin:0;font-size:48px;">
🧬 Rare Disease Intelligence Platform
</h1>

<p style="
font-size:20px;
margin-top:15px;
line-height:1.8;
color:#e2e8f0;
">

Analyze rare diseases using the Orphanet dataset.

Search diseases, compare medical coding systems,
and explore healthcare insights through interactive dashboards.

</p>

</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Header
# ----------------------------------------------------
logo_col, title_col = st.columns([1,6])

with logo_col:
    st.image("assets/logo.png", width=90)

with title_col:

    st.markdown("""
# 🧬 Rare Disease Intelligence Platform

### Healthcare Analytics Dashboard
""")

st.divider()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
with st.sidebar:

    st.title("🧬 Rare Disease Platform")

    st.success("Healthcare Analytics Dashboard")

    st.markdown("### 📌 Navigation")

    st.markdown("""
- 🏠 Dashboard
- 🔍 Disease Search
- ⚖️ Disease Comparison
- 📊 Analytics
- 📈 Dataset Insights
- 📋 Dataset Preview
- 📥 Download Dataset
""")

    st.divider()

    st.markdown("## 📊 Dataset Statistics")

    st.metric(
        "🧬 Total Diseases",
        f"{len(df):,}"
    )

    st.metric(
        "📂 Disease Groups",
        df["group"].nunique()
    )

    st.metric(
        "🧬 Disease Types",
        df["type"].nunique()
    )

    st.metric(
        "🏥 ICD-10 Records",
        df["icd10"].fillna("").ne("").sum()
    )

    st.metric(
        "📘 ICD-11 Records",
        df["icd11"].fillna("").ne("").sum()
    )

    st.divider()

    st.markdown("## 🔍 Filters")

    selected_type = st.selectbox(
        "Disease Type",
        ["All"] + sorted(df["type"].dropna().unique())
    )

    selected_group = st.selectbox(
        "Disease Group",
        ["All"] + sorted(df["group"].dropna().unique())
    )

# ----------------------------------------------------
# Apply Filters
# ----------------------------------------------------
filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

if selected_group != "All":
    filtered_df = filtered_df[
        filtered_df["group"] == selected_group
    ]

# ----------------------------------------------------
# Dashboard Overview
# ----------------------------------------------------
st.markdown("""
<div class="section-title">
📊 Dashboard Overview
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "🧬 Total Diseases",
        len(filtered_df)
    )

with m2:
    st.metric(
        "📂 Disease Groups",
        filtered_df["group"].nunique()
    )

with m3:
    st.metric(
        "🧬 Disease Types",
        filtered_df["type"].nunique()
    )

with m4:

    coverage = round(
        (
            filtered_df["icd10"]
            .fillna("")
            .ne("")
            .sum()
            /
            len(filtered_df)
        ) * 100,
        2
    ) if len(filtered_df) else 0

    st.metric(
        "🏥 ICD-10 Coverage",
        f"{coverage}%"
    )

st.divider()