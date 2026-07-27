import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Rare Disease Intelligence Platform",
    page_icon="🧬",
    layout="wide"
)
st.markdown("""
<div style="
background: linear-gradient(135deg, #0f172a, #1e3a8a, #3b82f6);
padding:30px;
border-radius:18px;
color:white;
box-shadow:0 8px 25px rgba(0,0,0,0.25);
margin-bottom:25px;
">
<h1 style="margin-bottom:12px;">🧬 Rare Disease Intelligence Platform</h1>

<p style="
font-size:20px;
line-height:1.8;
color:#e5e7eb;
margin:0;
">
Analyze rare diseases using the Orphanet dataset. Search diseases, explore
healthcare coding systems (ICD, OMIM, UMLS, MeSH), and gain insights through
interactive analytics.
</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Load CSS
# -----------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/orphanet_cleaned.csv")

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([0.4, 5])

with col1:
    st.image("assets/logo.png", width=90)

with col2:
   st.markdown("""
<h1 style="margin-top:10px;font-size:56px;font-weight:700;">
🧬 Rare Disease Intelligence Platform
</h1>

<p style="margin-top:-10px;font-size:24px;color:gray;">
Healthcare Analytics Dashboard
</p>
""", unsafe_allow_html=True)

st.write("Explore rare diseases using the Orphanet dataset.")

st.markdown("---")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("""
## 🧬 Rare Disease Intelligence Platform

Built using

✅ Streamlit

✅ Python

✅ Plotly

✅ Orphanet Dataset
""")
st.sidebar.divider()
st.sidebar.markdown("## 🚀 Quick Navigation")

st.sidebar.markdown("""
- 📊 Dashboard
- 🔍 Disease Search
- 📈 Analytics
- 🏆 Top Disease Groups
- 📋 Dataset Preview
- ⬇️ Download Data
""")

st.sidebar.divider()
st.sidebar.markdown("## 📊 Dataset Statistics")

st.sidebar.metric(
    "🧬 Total Diseases",
    f"{len(df):,}"
)

st.sidebar.metric(
    "📂 Disease Groups",
    df["group"].nunique()
)

st.sidebar.metric(
    "🧬 Disease Types",
    df["type"].nunique()
)
st.sidebar.divider()
st.sidebar.title("🔍 Filters")

selected_type = st.sidebar.selectbox(
    "Disease Type",
    ["All"] + sorted(df["type"].dropna().unique())
)

selected_group = st.sidebar.selectbox(
    "Disease Group",
    ["All"] + sorted(df["group"].dropna().unique())
)

filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

if selected_group != "All":
    filtered_df = filtered_df[
        filtered_df["group"] == selected_group
    ]

# -----------------------------
# Metrics
# -----------------------------
st.markdown("""
<div class="section-title">
📊 Dashboard Overview
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-icon">🧬</div>
        <div class="metric-value">{len(filtered_df):,}</div>
        <div class="metric-label">Total Diseases</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-icon">🏥</div>
        <div class="metric-value">{filtered_df["icd10"].fillna("").ne("").sum():,}</div>
        <div class="metric-label">ICD-10 Codes</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card orange">
        <div class="metric-icon">📘</div>
        <div class="metric-value">{filtered_df["icd11"].fillna("").ne("").sum():,}</div>
        <div class="metric-label">ICD-11 Codes</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-icon">🧬</div>
        <div class="metric-value">{filtered_df["omim"].fillna("").ne("").sum():,}</div>
        <div class="metric-label">OMIM Records</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Dashboard Statistics
# -----------------------------
st.markdown("""
<div class="section-title">
📈 Dashboard Statistics
</div>
""", unsafe_allow_html=True)

coverage = round(
    (
        filtered_df["icd10"]
        .fillna("")
        .ne("")
        .sum()
        / len(filtered_df)
    ) * 100,
    2
) if len(filtered_df) else 0

k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-icon">🗂️</div>
        <div class="metric-value">{filtered_df["group"].nunique()}</div>
        <div class="metric-label">Disease Groups</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card orange">
        <div class="metric-icon">🧪</div>
        <div class="metric-value">{filtered_df["type"].nunique()}</div>
        <div class="metric-label">Disease Types</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-icon">📈</div>
        <div class="metric-value">{coverage}%</div>
        <div class="metric-label">ICD-10 Coverage</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
# -----------------------------
# Premium Disease Comparison
# -----------------------------
st.markdown("""
<div class="section-title">
⚖️ Disease Comparison
</div>
""", unsafe_allow_html=True)

st.caption("Select two diseases and compare their medical information.")

# ---------------- Search Boxes ---------------- #

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧬 Disease 1")
    disease1 = st.selectbox(
        "Select First Disease",
        sorted(filtered_df["name"].dropna().unique()),
        key="disease1"
    )

with col2:
    st.markdown("### 🧬 Disease 2")
    disease2 = st.selectbox(
        "Select Second Disease",
        sorted(filtered_df["name"].dropna().unique()),
        key="disease2"
    )

# ---------------- VS ---------------- #

st.markdown("""
<div style="
text-align:center;
font-size:50px;
font-weight:bold;
margin:25px 0;
color:#2563eb;">
🆚
</div>
""", unsafe_allow_html=True)

# ---------------- Cards ---------------- #

if disease1 and disease2:

    d1 = filtered_df[filtered_df["name"] == disease1].iloc[0]
    d2 = filtered_df[filtered_df["name"] == disease2].iloc[0]

    card1, card2 = st.columns(2, gap="large")

with card1:
    st.markdown("### 🧬 Disease 1")

    st.markdown(f"""
<div class="compare-card">

<div class="compare-title">
🧬 {d1["name"]}
</div>

<div class="compare-item">
<span>🏷 ORPHA Code</span><br>{d1["orpha_code"]}
</div>

<div class="compare-item">
<span>📂 Group</span><br>{d1["group"]}
</div>

<div class="compare-item">
<span>🧬 Type</span><br>{d1["type"]}
</div>

<div class="compare-item">
<span>🏥 ICD-10</span><br>{d1["icd10"] if pd.notna(d1["icd10"]) else "N/A"}
</div>

<div class="compare-item">
<span>📘 ICD-11</span><br>{d1["icd11"] if pd.notna(d1["icd11"]) else "N/A"}
</div>

<div class="compare-item">
<span>🧬 OMIM</span><br>{d1["omim"] if pd.notna(d1["omim"]) else "N/A"}
</div>

<div class="compare-item">
<span>🔬 UMLS</span><br>{d1["umls"] if pd.notna(d1["umls"]) else "N/A"}
</div>

<div class="compare-item">
<span>📚 MeSH</span><br>{d1["mesh"] if pd.notna(d1["mesh"]) else "N/A"}
</div>

<div class="compare-item">
<span>📚 MeSH</span><br>{d1["mesh"] if pd.notna(d1["mesh"]) else "N/A"}
</div>

<hr>

<div class="compare-item">
<span>📝 Definition</span><br>
{d1["definition"] if pd.notna(d1["definition"]) else "Definition Not Available"}
</div>

</div>
""", unsafe_allow_html=True)

with card2:
    st.markdown("### 🧬 Disease 2")

    st.markdown(f"""
<div class="compare-card">

<div class="compare-title">
🧬 {d2["name"]}
</div>

<div class="compare-item">
<span>🏷 ORPHA Code</span><br>{d2["orpha_code"]}
</div>

<div class="compare-item">
<span>📂 Group</span><br>{d2["group"]}
</div>

<div class="compare-item">
<span>🧬 Type</span><br>{d2["type"]}
</div>

<div class="compare-item">
<span>🏥 ICD-10</span><br>{d2["icd10"] if pd.notna(d2["icd10"]) else "N/A"}
</div>

<div class="compare-item">
<span>📘 ICD-11</span><br>{d2["icd11"] if pd.notna(d2["icd11"]) else "N/A"}
</div>

<div class="compare-item">
<span>🧬 OMIM</span><br>{d2["omim"] if pd.notna(d2["omim"]) else "N/A"}
</div>

<div class="compare-item">
<span>🔬 UMLS</span><br>{d2["umls"] if pd.notna(d2["umls"]) else "N/A"}
</div>

<div class="compare-item">
<span>📚 MeSH</span><br>{d2["mesh"] if pd.notna(d2["mesh"]) else "N/A"}
</div>

<div class="compare-item">
<span>📚 MeSH</span><br>{d2["mesh"] if pd.notna(d2["mesh"]) else "N/A"}
</div>

<hr>

<div class="compare-item">
<span>📝 Definition</span><br>
{d2["definition"] if pd.notna(d2["definition"]) else "Definition Not Available"}
</div>

</div>
""", unsafe_allow_html=True)
    st.markdown("---")

st.markdown("""
<div class="section-title">
📊 Comparison Summary
</div>
""", unsafe_allow_html=True)

comparison_df = pd.DataFrame({
    "Feature": [
        "Disease Name",
        "ORPHA Code",
        "Group",
        "Type",
        "ICD-10",
        "ICD-11",
        "OMIM",
        "UMLS",
        "MeSH"
    ],
    "Disease 1": [
        d1["name"],
        d1["orpha_code"],
        d1["group"],
        d1["type"],
        d1["icd10"] if pd.notna(d1["icd10"]) else "N/A",
        d1["icd11"] if pd.notna(d1["icd11"]) else "N/A",
        d1["omim"] if pd.notna(d1["omim"]) else "N/A",
        d1["umls"] if pd.notna(d1["umls"]) else "N/A",
        d1["mesh"] if pd.notna(d1["mesh"]) else "N/A",
    ],
    "Disease 2": [
        d2["name"],
        d2["orpha_code"],
        d2["group"],
        d2["type"],
        d2["icd10"] if pd.notna(d2["icd10"]) else "N/A",
        d2["icd11"] if pd.notna(d2["icd11"]) else "N/A",
        d2["omim"] if pd.notna(d2["omim"]) else "N/A",
        d2["umls"] if pd.notna(d2["umls"]) else "N/A",
        d2["mesh"] if pd.notna(d2["mesh"]) else "N/A",
    ]
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)
fields = [
    "group",
    "type",
    "icd10",
    "icd11",
    "omim",
    "umls",
    "mesh"
]

same = 0

for field in fields:
    value1 = str(d1[field]).strip().lower()
    value2 = str(d2[field]).strip().lower()

    if value1 == value2:
        same += 1

score = round((same / len(fields)) * 100)

st.markdown("""
<div class="section-title">
🧬 Similarity Score
</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns([2,1,2])

with col2:
    st.metric(
        label="Similarity",
        value=f"{score}%"
    )


    st.markdown("---")

if score == 100:
    st.success("✅ Both diseases have identical coding information.")
elif score >= 70:
    st.info("ℹ️ These diseases share many common characteristics.")
elif score >= 40:
    st.warning("⚠️ These diseases are partially similar.")
else:
    st.error("❌ These diseases are significantly different.")
    st.markdown("---")


csv = comparison_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Comparison Report",
    data=csv,
    file_name="disease_comparison_report.csv",
    mime="text/csv",
    use_container_width=True
)

st.markdown("""
<div style="
padding:15px;
border-radius:12px;
background:#0f172a;
text-align:center;
color:white;
margin-top:20px;
">
🧬 <b>Comparison powered by Orphanet Rare Disease Dataset</b>
</div>
""", unsafe_allow_html=True)
# -----------------------------        
# Disease Search
# -----------------------------

st.divider()
# -----------------------------
# Initialize Session State
# -----------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

st.markdown("""
<div class="section-title">
🔍 Disease Search
</div>
""", unsafe_allow_html=True)

search_type = st.radio(
    "Search By",
    ["Disease Name", "ORPHA Code"],
    horizontal=True
)

if search_type == "Disease Name":
    search = st.selectbox(
        "Search Disease",
        sorted(filtered_df["name"].dropna().unique()),
        index=None,
        placeholder="Type or select a disease..."
    )
else:
    search = st.selectbox(
        "Search ORPHA Code",
        sorted(filtered_df["orpha_code"].dropna().astype(str).unique()),
        index=None,
        placeholder="Type or select an ORPHA Code..."
    )

# -----------------------------
# Search Result
# -----------------------------
if search:

    if search_type == "Disease Name":
        result = filtered_df[
            filtered_df["name"].str.contains(search, case=False, na=False)
        ]
    else:
        result = filtered_df[
            filtered_df["orpha_code"].astype(str).str.contains(
    str(search),
    case=False,
    na=False
)
        ]

    if not result.empty:

        disease = result.iloc[0]
        if search not in st.session_state["history"]:
            st.session_state["history"].append(search)

        st.success("Disease Found Successfully ✅")

        st.markdown(f"""
<div class="disease-profile">

<div class="profile-title">
🧬 {disease["name"]}
</div>

<div class="profile-grid">

<div class="profile-item">
<span>🏷 ORPHA Code</span>
<h4>{disease["orpha_code"]}</h4>
</div>
<div class="profile-item">
<span>🏥 ICD-10</span>
<h4>{disease["icd10"] if pd.notna(disease["icd10"]) else "N/A"}</h4>
</div>

<div class="profile-item">
<span>📘 ICD-11</span>
<h4>{disease["icd11"] if pd.notna(disease["icd11"]) else "N/A"}</h4>
</div>

<div class="profile-item">
<span>🧬 OMIM</span>
<h4>{disease["omim"] if pd.notna(disease["omim"]) else "N/A"}</h4>
</div>

<div class="profile-item">
<span>🔬 UMLS</span>
<h4>{disease["umls"] if pd.notna(disease["umls"]) else "N/A"}</h4>
</div>

<div class="profile-item">
<span>📚 MeSH</span>
<h4>{disease["mesh"] if pd.notna(disease["mesh"]) else "N/A"}</h4>
</div>

<div class="profile-item">
<span>📂 Group</span>
<h4>{disease["group"]}</h4>
</div>

<div class="profile-item">
<span>🧬 Type</span>
<h4>{disease["type"]}</h4>
</div>
<hr>

<div class="definition-box">

<h3>📝 Definition</h3>

<p>
{disease["definition"] if pd.notna(disease["definition"]) else "Definition not available."}
</p>

</div>

</div>

</div>
""", unsafe_allow_html=True)

    else:
        st.error("No Disease Found")
         

# -----------------------------
# Search History
# -----------------------------
st.markdown("""
<div class="section-title">
📜 Recent Searches
</div>
""", unsafe_allow_html=True)

if len(st.session_state["history"]) > 0:

    history = list(dict.fromkeys(st.session_state["history"][::-1]))

    for i, item in enumerate(history[:10], start=1):
        st.write(f"{i}. {item}")

else:
    st.info("No searches yet.")

st.divider()

# -----------------------------
# Analytics Dashboard
# -----------------------------
st.markdown("---")
st.markdown("""
<div class="section-title">
📊 Disease Analytics
</div>
""", unsafe_allow_html=True)

left, right = st.columns(2)

with left:

    type_count = (
        filtered_df["type"]
        .value_counts()
        .reset_index()
    )

    type_count.columns = ["Type", "Count"]

    fig1 = px.bar(
    type_count.head(10),
    x="Count",
    y="Type",
    orientation="h",
    color="Count",
    title="Top 10 Disease Types",
    text="Count"
)

fig1.update_layout(
    yaxis={"categoryorder": "total ascending"},
    title_x=0.5
)

st.plotly_chart(fig1, use_container_width=True)

with right:

    group_count = (
        filtered_df["group"]
        .value_counts()
        .reset_index()
    )

    group_count.columns = ["Group", "Count"]

    fig2 = px.pie(
    group_count.head(10),
    names="Group",
    values="Count",
    hole=0.55,
    title="📊 Disease Group Distribution"
)

    fig2.update_layout(
    height=500,
    width=700,
    title_x=0.5
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class="section-title">
📊 Top 10 Disease Groups
</div>
""", unsafe_allow_html=True)

group_count = (
    df["group"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
    .reset_index()
)

group_count.columns = ["Disease Group", "Count"]

fig = px.bar(
    group_count,
    x="Disease Group",
    y="Count",
    title="Top 10 Disease Groups"
)

st.plotly_chart(fig, use_container_width=True)
fig.update_layout(
    height=500,
    yaxis={'categoryorder':'total ascending'}
)


st.markdown("""
<div class="section-title">
🏥 Medical Database Coverage
</div>
""", unsafe_allow_html=True)

coverage = pd.DataFrame({
    "Database": ["ICD-10", "ICD-11", "OMIM", "UMLS", "MeSH"],
    "Coverage (%)": [
        df["icd10"].notna().mean() * 100,
        df["icd11"].notna().mean() * 100,
        df["omim"].notna().mean() * 100,
        df["umls"].notna().mean() * 100,
        df["mesh"].notna().mean() * 100,
    ]
})

fig = px.bar(
    coverage,
    x="Database",
    y="Coverage (%)",
    title="Coverage of External Medical Databases",
    text="Coverage (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="section-title">
🥧 Disease Group Distribution
</div>
""", unsafe_allow_html=True)

fig = px.pie(
    df,
    names="group",
    title="Disease Distribution by Group"
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.markdown("""
<div class="section-title">


📈 Dataset Insights
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:

    st.markdown(f"""
    <div class="insight-card blue">
        <h3>📌 Total Disease Groups</h3>
        <h1>{filtered_df["group"].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card green">
        <h3>🧬 Total Disease Types</h3>
        <h1>{filtered_df["type"].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card orange">
        <h3>🏥 ICD-10 Coverage</h3>
        <h1>{coverage}%</h1>
    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="insight-card purple">
        <h3>📘 ICD-11 Available</h3>
        <h1>{filtered_df["icd11"].fillna("").ne("").sum()}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card red">
        <h3>🧬 OMIM Available</h3>
        <h1>{filtered_df["omim"].fillna("").ne("").sum()}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card cyan">
        <h3>📚 UMLS Available</h3>
        <h1>{filtered_df["umls"].fillna("").ne("").sum()}</h1>
    </div>
    """, unsafe_allow_html=True)  

    st.markdown("---")
st.markdown("""
<div class="section-title">
🧹 Data Quality Report
</div>
""", unsafe_allow_html=True)

quality = {
    "Column": [
        "Disease Name",
        "ICD-10",
        "ICD-11",
        "OMIM",
        "UMLS",
        "MeSH"
    ],
    "Available": [
        filtered_df["name"].notna().sum(),
        filtered_df["icd10"].fillna("").ne("").sum(),
        filtered_df["icd11"].fillna("").ne("").sum(),
        filtered_df["omim"].fillna("").ne("").sum(),
        filtered_df["umls"].fillna("").ne("").sum(),
        filtered_df["mesh"].fillna("").ne("").sum(),
    ]
}

st.dataframe(
    pd.DataFrame(quality),
    use_container_width=True
)   

    # -----------------------------
# Disease Coding Coverage
# -----------------------------
st.markdown("---")
st.markdown("""
<div class="section-title">
🏥 Medical Database Coverage
</div>
""", unsafe_allow_html=True)

coverage = pd.DataFrame({
    "Database": ["ICD-10", "ICD-11", "OMIM", "UMLS", "MONDO", "MeSH"],
    "Available": [
        filtered_df["icd10"].fillna("").ne("").sum(),
        filtered_df["icd11"].fillna("").ne("").sum(),
        filtered_df["omim"].fillna("").ne("").sum(),
        filtered_df["umls"].fillna("").ne("").sum(),
        filtered_df["mondo"].fillna("").ne("").sum(),
        filtered_df["mesh"].fillna("").ne("").sum()
    ]
})

fig3 = px.bar(
    coverage,
    x="Database",
    y="Available",
    color="Available",
    text="Available",
    title="Medical Database Coverage"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Top Disease Groups
# -----------------------------
st.markdown("---")

st.markdown("""
<div class="section-title">
🏆 Top Disease Groups
</div>
""", unsafe_allow_html=True)

top_group = (
    filtered_df["group"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_group.columns = ["Disease Group", "Count"]

fig = px.bar(
    top_group,
    x="Count",
    y="Disease Group",
    orientation="h",
    text="Count",
    color="Count",
    color_continuous_scale="Blues",
)

fig.update_layout(
    title=None,
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white", size=15),
    height=500,
    margin=dict(l=20, r=20, t=20, b=20),
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending")
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# Dataset Preview
# -----------------------------
st.markdown("---")
st.markdown("""
<div class="section-title">
📋 Dataset Preview
</div>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)

# -----------------------------
# Download Dataset
# -----------------------------
st.markdown("---")
st.markdown("""
<div class="section-title">
📥 Download Filtered Dataset
</div>
""", unsafe_allow_html=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download CSV",
    csv,
    "filtered_rare_disease_data.csv",
    "text/csv"
)

st.divider()

st.markdown("""
<div class="section-title">
ℹ️ About Project
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="definition-box">

<h3>🧬 Rare Disease Intelligence Platform</h3>

<p>
This platform is developed using the Orphanet Rare Disease Dataset to help users
search, compare, and analyze rare diseases. It provides disease classification,
medical coding systems (ICD-10, ICD-11, OMIM, UMLS, MeSH), interactive analytics,
and healthcare insights through an easy-to-use dashboard.
</p>

</div>
""", unsafe_allow_html=True)
# -----------------------------
# Dataset Information
# -----------------------------
st.markdown("---")
st.markdown("""
<div class="section-title">
ℹ️ Dataset Information
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card cyan">
        <div class="metric-icon">📄</div>
        <div class="metric-value">{len(filtered_df):,}</div>
        <div class="metric-label">Rows</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card teal">
        <div class="metric-icon">📊</div>
        <div class="metric-value">{len(filtered_df.columns)}</div>
        <div class="metric-label">Columns</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card red">
        <div class="metric-icon">✅</div>
        <div class="metric-value">{filtered_df.isna().sum().sum()}</div>
        <div class="metric-label">Missing Values</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
    st.divider()

st.markdown("""
<div style="
text-align:center;
padding:25px;
background:linear-gradient(90deg,#0f172a,#1e3a8a);
border-radius:15px;
color:white;
margin-top:20px;
">

<h3>🧬 Rare Disease Intelligence Platform</h3>

<p>
Developed by <b>Rudrakashi Kiledar</b><br>
B.Tech - Artificial Intelligence & Data Science
</p>

<p>
💻 Built with Streamlit | Pandas | Plotly | Python
</p>

<p>
📂 Dataset: Orphanet Rare Disease Dataset
</p>

<p style="font-size:14px;color:#cbd5e1;">
Version 1.0 • 2026
</p>

</div>
""", unsafe_allow_html=True)
