import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -30%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 80%);
        transform: rotate(30deg);
        pointer-events: none;
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Glassmorphic Metric Cards */
    .kpi-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.6);
    }
    
    .dark .kpi-card {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 0.25rem;
        background: linear-gradient(135deg, #1E1B4B 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .dark .kpi-value {
        background: linear-gradient(135deg, #F3F4F6 0%, #A5B4FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Badge styling */
    .trend-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .badge-positive {
        background-color: #DEF7EC;
        color: #03543F;
    }
    
    /* Table style */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Clean and stylish tab bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        background-color: rgba(243, 244, 246, 0.8);
        border-radius: 10px;
        font-weight: 600;
        color: #4B5563;
        border: none;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(229, 231, 235, 1);
        color: #1F2937;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4F46E5 !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    /* Sections headers */
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #111827;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #4F46E5;
        padding-left: 10px;
    }
    
    .dark .section-title {
        color: #F9FAFB;
    }
    
    .feature-card {
        padding: 1.5rem;
        background-color: #F8FAFC;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    
    .dark .feature-card {
        background-color: #1E293B;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 1. LOAD & CACHE DATA PIPELINE
# ----------------------------------------------------
@st.cache_data
def get_raw_data():
    return pd.read_csv("googleplaystore_v2.csv")

@st.cache_data
def get_clean_data(df):
    df_clean = df.copy()
    
    # 1. Null Rating Treatment: Drop rows with null ratings
    df_clean = df_clean[~df_clean['Rating'].isnull()]
    
    # 2. Drop specific shifted row (index 10472 where Android Ver is null and Category is '1.9')
    if 10472 in df_clean.index:
        df_clean = df_clean.drop(10472)
    
    # 3. Fill missing Android Ver with mode
    if not df_clean['Android Ver'].isnull().all():
        android_mode = df_clean['Android Ver'].mode()[0]
        df_clean['Android Ver'] = df_clean['Android Ver'].fillna(android_mode)
    
    # 4. Fill missing Current Ver with mode
    if not df_clean['Current Ver'].isnull().all():
        current_mode = df_clean['Current Ver'].mode()[0]
        df_clean['Current Ver'] = df_clean['Current Ver'].fillna(current_mode)
        
    # 5. Clean Price column (remove '$' and convert to float)
    def clean_price_val(x):
        if pd.isna(x):
            return 0.0
        x_str = str(x).strip()
        if x_str == "0" or x_str == "0.0":
            return 0.0
        if x_str.startswith("$"):
            x_str = x_str[1:]
        try:
            return float(x_str)
        except ValueError:
            return 0.0
            
    df_clean['Price'] = df_clean['Price'].apply(clean_price_val)
    
    # 6. Reviews to int32
    df_clean['Reviews'] = pd.to_numeric(df_clean['Reviews'], errors='coerce').fillna(0).astype('int32')
    
    # 7. Clean Installs column (remove commas & plus, convert to int)
    def clean_installs_val(x):
        if pd.isna(x):
            return 0
        x_str = str(x).replace(",", "").replace("+", "").strip()
        try:
            return int(x_str)
        except ValueError:
            try:
                return int(float(x_str))
            except ValueError:
                return 0
                
    df_clean['Installs'] = df_clean['Installs'].apply(clean_installs_val)
    
    # 8. Sanity check: Reviews <= Installs
    df_clean = df_clean[df_clean['Reviews'] <= df_clean['Installs']]
    
    # 9. Outliers: Price <= 30
    df_clean = df_clean[df_clean['Price'] <= 30.0]
    
    # 10. Outliers: Reviews <= 1,000,000 (1 million)
    df_clean = df_clean[df_clean['Reviews'] <= 1000000]
    
    # 11. Outliers: Installs <= 100,000,000 (100 million)
    df_clean = df_clean[df_clean['Installs'] <= 100000000]
    
    # 12. Clean Content Rating: drop 'Adults only 18+' and 'Unrated'
    df_clean = df_clean[~df_clean['Content Rating'].isin(["Adults only 18+", "Unrated"])]
    
    # 13. Create Size Bucket using pd.qcut
    try:
        df_clean['Size_Bucket'] = pd.qcut(df_clean['Size'], [0, 0.2, 0.4, 0.6, 0.8, 1], labels=["VL", "L", "M", "H", "VH"])
    except ValueError:
        # Fallback if duplicate boundaries
        df_clean['Size_Bucket'] = pd.qcut(df_clean['Size'], [0, 0.2, 0.4, 0.6, 0.8, 1], labels=["VL", "L", "M", "H", "VH"], duplicates='drop')
        
    # 14. Extract Month updated
    df_clean['updated_month'] = pd.to_datetime(df_clean['Last Updated'], errors='coerce').dt.month
    df_clean['updated_month'] = df_clean['updated_month'].fillna(1).astype(int)
    
    df_clean.reset_index(inplace=True, drop=True)
    return df_clean

# Load dataframes
df_raw = get_raw_data()
df_clean_all = get_clean_data(df_raw)

# ----------------------------------------------------
# 2. HERO HEADER SECTION
# ----------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1 class="header-title">Google Play Store Insights Dashboard</h1>
    <p class="header-subtitle">Interactive analytics, data cleaning pipeline & exploratory analysis based on the Python Data Visualisation Case Study.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. SIDEBAR CONTROLS & DYNAMIC FILTERING
# ----------------------------------------------------
st.sidebar.markdown("### 📊 Global Filters")
st.sidebar.write("Filters apply across the analysis tabs.")

# Categories multiselect
categories = sorted(df_clean_all['Category'].unique())
selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories[:8])

# Type selection
app_types = ["All", "Free", "Paid"]
selected_type = st.sidebar.selectbox("App Type", app_types)

# Rating slider
min_rating, max_rating = float(df_clean_all['Rating'].min()), float(df_clean_all['Rating'].max())
selected_rating_range = st.sidebar.slider("Rating Range", min_rating, max_rating, (1.0, 5.0), step=0.1)

# Price slider
max_price_limit = float(df_clean_all['Price'].max())
selected_price_range = st.sidebar.slider("Price Range ($)", 0.0, max_price_limit if max_price_limit > 0 else 30.0, (0.0, 30.0), step=0.5)

# Apply filters
df_filtered = df_clean_all.copy()

if selected_categories:
    df_filtered = df_filtered[df_filtered['Category'].isin(selected_categories)]

if selected_type != "All":
    df_filtered = df_filtered[df_filtered['Type'] == selected_type]

df_filtered = df_filtered[
    (df_filtered['Rating'] >= selected_rating_range[0]) & 
    (df_filtered['Rating'] <= selected_rating_range[1]) & 
    (df_filtered['Price'] >= selected_price_range[0]) & 
    (df_filtered['Price'] <= selected_price_range[1])
]

# ----------------------------------------------------
# 4. TABBED LAYOUT CREATION
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 App Overview",
    "🧹 Data Cleaning Pipeline",
    "📈 Univariate Analysis",
    "🔗 Bivariate Analysis",
    "🗺️ Multivariate Heatmaps",
    "📅 Temporal & Stacked Trends"
])

# ----------------------------------------------------
# TAB 1: OVERVIEW & KEY KPI METRICS
# ----------------------------------------------------
with tab1:
    st.markdown("<div class='section-title'>Overview & Key Performance Indicators</div>", unsafe_allow_html=True)
    
    # Calculate KPIs on filtered data
    total_apps = len(df_filtered)
    avg_rating = df_filtered['Rating'].mean() if total_apps > 0 else 0.0
    total_installs = df_filtered['Installs'].sum() if total_apps > 0 else 0
    avg_price = df_filtered['Price'].mean() if total_apps > 0 else 0.0
    free_ratio = (df_filtered['Type'] == 'Free').sum() / total_apps * 100 if total_apps > 0 else 0.0
    
    # Render premium HTML metrics
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Total Apps Selected</div>
            <div class="kpi-value">{total_apps:,}</div>
            <span class="trend-badge badge-positive">Active Range</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Average App Rating</div>
            <div class="kpi-value">{avg_rating:.2f} ★</div>
            <span class="trend-badge badge-positive">Out of 5.0</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total App Installs</div>
            <div class="kpi-value">{total_installs:,}</div>
            <span class="trend-badge badge-positive">Downloads</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Average Price</div>
            <div class="kpi-value">${avg_price:.2f}</div>
            <span class="trend-badge badge-positive">Paid apps only</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Free Apps Portion</div>
            <div class="kpi-value">{free_ratio:.1f}%</div>
            <span class="trend-badge badge-positive">Distribution Ratio</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Search & Data Explorer
    st.subheader("🔍 Interactive Dataset Explorer")
    search_query = st.text_input("Search apps by name...", "")
    
    display_df = df_filtered.copy()
    if search_query:
        display_df = display_df[display_df['App'].str.contains(search_query, case=False, na=False)]
        
    st.dataframe(
        display_df[['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price', 'Content Rating', 'Genres', 'Last Updated']],
        use_container_width=True
    )
    st.caption(f"Showing {len(display_df)} apps of {len(df_filtered)} filtered results.")

# ----------------------------------------------------
# TAB 2: INTERACTIVE DATA CLEANING WALKTHROUGH
# ----------------------------------------------------
with tab2:
    st.markdown("<div class='section-title'>Interactive Data Cleaning Pipeline</div>", unsafe_allow_html=True)
    
    st.write(
        "A critical phase in the Google Play Store Case Study was standardizing the data types and handling outliers. "
        "Here is the interactive pipeline showing how raw data was refined step by step:"
    )
    
    # Showcase stats comparison
    col_raw, col_cleaned = st.columns(2)
    with col_raw:
        st.markdown("""
        <div class="feature-card" style="border-left: 5px solid #EF4444;">
            <h3>🚨 Raw Input Data</h3>
            <p><strong>Initial Shape:</strong> 10,841 Rows x 13 Columns</p>
            <ul>
                <li><code>Rating</code> had 1,474 missing values.</li>
                <li><code>Price</code> contained character strings like "$" and "0".</li>
                <li><code>Reviews</code> and <code>Installs</code> were classified as text/object datatypes.</li>
                <li>Shifted rows existed (e.g. index 10472 category shifted).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_cleaned:
        st.markdown(f"""
        <div class="feature-card" style="border-left: 5px solid #10B981;">
            <h3>✅ Cleaned & Sanitized Data</h3>
            <p><strong>Final Shape:</strong> {len(df_clean_all):,} Rows x 15 Columns</p>
            <ul>
                <li>Missing values resolved / modes imputed.</li>
                <li>Corrected data types (Reviews: int32, Price: float64, Installs: int).</li>
                <li>Outliers removed (Price <= $30, Reviews <= 1M, Installs <= 100M).</li>
                <li>Additional buckets (Size_Bucket) and features (updated_month) calculated.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    # Interactive Step-by-Step logs
    with st.expander("🕵️ View Step-by-Step Data Reductions"):
        
        # We can construct intermediate steps counts
        # Step 0: Raw
        step0_cnt = len(df_raw)
        
        # Step 1: Drop null ratings
        df_s1 = df_raw[~df_raw['Rating'].isnull()]
        step1_cnt = len(df_s1)
        
        # Step 2: Drop shifted
        df_s2 = df_s1.copy()
        if 10472 in df_s2.index:
            df_s2 = df_s2.drop(10472)
        step2_cnt = len(df_s2)
        
        # Step 3: Type Cleanings
        # We can just apply the cleaning to Price, Reviews, Installs
        df_s3 = df_s2.copy()
        df_s3['Price'] = df_s3['Price'].apply(clean_price_val)
        df_s3['Reviews'] = pd.to_numeric(df_s3['Reviews'], errors='coerce').fillna(0).astype('int32')
        df_s3['Installs'] = df_s3['Installs'].apply(clean_installs_val)
        step3_cnt = len(df_s3)
        
        # Step 4: Sanity: Reviews <= Installs
        df_s4 = df_s3[df_s3['Reviews'] <= df_s3['Installs']]
        step4_cnt = len(df_s4)
        
        # Step 5: Price Outliers <= 30
        df_s5 = df_s4[df_s4['Price'] <= 30.0]
        step5_cnt = len(df_s5)
        
        # Step 6: Review Outliers <= 1M
        df_s6 = df_s5[df_s5['Reviews'] <= 1000000]
        step6_cnt = len(df_s6)
        
        # Step 7: Installs Outliers <= 100M
        df_s7 = df_s6[df_s6['Installs'] <= 100000000]
        step7_cnt = len(df_s7)
        
        # Step 8: Content Rating exclusions
        df_s8 = df_s7[~df_s7['Content Rating'].isin(["Adults only 18+", "Unrated"])]
        step8_cnt = len(df_s8)
        
        step_names = [
            "Raw Dataset",
            "1. Dropping Null Ratings",
            "2. Removing Shifted Rows",
            "3. Datatype Conversion",
            "4. Sanity Check (Reviews <= Installs)",
            "5. Price Outlier Cap (<= $30)",
            "6. Reviews Outlier Cap (<= 1M)",
            "7. Installs Outlier Cap (<= 100M)",
            "8. Removing Rare Content Ratings"
        ]
        
        counts = [step0_cnt, step1_cnt, step2_cnt, step3_cnt, step4_cnt, step5_cnt, step6_cnt, step7_cnt, step8_cnt]
        reductions = [0] + [counts[i-1] - counts[i] for i in range(1, len(counts))]
        
        pipeline_df = pd.DataFrame({
            "Cleaning Step": step_names,
            "Remaining Rows": counts,
            "Rows Dropped in Step": reductions
        })
        
        st.table(pipeline_df)
        
        # Waterfall style visualization of data retention
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Data Cleaning Retention", 
            orientation = "v",
            measure = ["relative"] * len(step_names),
            x = step_names,
            textposition = "outside",
            text = [f"{c:,}" for c in counts],
            y = [step0_cnt] + [-r for r in reductions[1:]],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color": "#EF4444"}},
            increasing = {"marker":{"color": "#10B981"}},
            totals = {"marker":{"color": "#4F46E5"}}
        ))
        
        fig_waterfall.update_layout(
            title = "Waterfall: Row Count Reduction After Cleaning",
            showlegend = False,
            height = 500,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

# ----------------------------------------------------
# TAB 3: UNIVARIATE ANALYSES
# ----------------------------------------------------
with tab3:
    st.markdown("<div class='section-title'>Univariate Analysis & Distributions</div>", unsafe_allow_html=True)
    st.write("Understand the individual distribution profile of key metric attributes.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ App Ratings Distribution")
        # Plot rating distribution histogram
        bins_sel = st.slider("Rating Histogram Bins", 5, 50, 20)
        fig_rating = px.histogram(
            df_filtered, 
            x="Rating", 
            nbins=bins_sel,
            title="Distribution of App Ratings",
            labels={"Rating": "App Rating"},
            color_discrete_sequence=["#10B981"],
            opacity=0.85
        )
        fig_rating.update_layout(
            xaxis_title="Rating (1.0 to 5.0)",
            yaxis_title="Count of Apps",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_rating, use_container_width=True)
        st.markdown(
            "> **Insight:** Ratings are heavily left-skewed, showing that the majority of apps "
            "maintained on the Play Store receive feedback scores between 4.0 and 4.7."
        )

    with col2:
        st.subheader("💬 Reviews Distribution")
        fig_reviews = px.histogram(
            df_filtered, 
            x="Reviews", 
            nbins=25,
            title="Distribution of User Reviews",
            labels={"Reviews": "Number of Reviews"},
            color_discrete_sequence=["#3B82F6"],
            opacity=0.85
        )
        fig_reviews.update_layout(
            xaxis_title="Reviews (Cap: 1M)",
            yaxis_title="Count of Apps",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_reviews, use_container_width=True)
        st.markdown(
            "> **Insight:** User reviews follow a highly skewed power-law distribution. Most apps "
            "receive relatively few reviews, while only a small set crosses 100,000+ review counts."
        )

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("📐 App Size Distribution")
        fig_size = px.histogram(
            df_filtered, 
            x="Size", 
            nbins=25,
            title="Distribution of App Sizes",
            labels={"Size": "Size (MBs / relative)"},
            color_discrete_sequence=["#EC4899"],
            opacity=0.85
        )
        fig_size.update_layout(
            xaxis_title="Size (MBs)",
            yaxis_title="Count of Apps",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_size, use_container_width=True)
        st.markdown(
            "> **Insight:** A high concentration of apps are lightweight (under 20MBs), suggesting "
            "developers target smaller file footprints for faster install rates."
        )

    with col4:
        st.subheader("👪 Content Rating Share")
        # Content rating distribution
        content_counts = df_filtered['Content Rating'].value_counts().reset_index()
        content_counts.columns = ['Content Rating', 'Count']
        
        # Dual visualization selector
        viz_type = st.radio("Chart Type", ["Pie Chart", "Bar Chart"], horizontal=True, key="univariate_content_rating")
        
        if viz_type == "Pie Chart":
            fig_content = px.pie(
                content_counts, 
                values="Count", 
                names="Content Rating",
                title="Content Rating Distribution Proportions",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_content.update_traces(textposition='inside', textinfo='percent+label')
        else:
            fig_content = px.bar(
                content_counts, 
                x="Content Rating", 
                y="Count",
                title="App Count by Content Rating Class",
                color="Content Rating",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            
        fig_content.update_layout(height=370, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_content, use_container_width=True)

# ----------------------------------------------------
# TAB 4: BIVARIATE & CORRELATION ANALYSES
# ----------------------------------------------------
with tab4:
    st.markdown("<div class='section-title'>Bivariate Analysis & Correlations</div>", unsafe_allow_html=True)
    st.write("Examine potential correlations between app metrics (e.g., how sizing or pricing affects rating).")
    
    col_biv1, col_biv2 = st.columns(2)
    
    with col_biv1:
        st.subheader("📐 Size vs Rating (Joint Scatter)")
        fig_scat_size = px.scatter(
            df_filtered, 
            x="Size", 
            y="Rating",
            trendline=None,
            marginal_x="histogram",
            marginal_y="box",
            opacity=0.4,
            title="App Size vs. App Rating",
            color_discrete_sequence=["#8B5CF6"]
        )
        fig_scat_size.update_layout(
            xaxis_title="Size (MBs)",
            yaxis_title="Rating (1-5)",
            height=450,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_scat_size, use_container_width=True)
        st.markdown(
            "> **Observation:** Heavy app sizing doesn't guarantee premium scores, though "
            "top-tier ratings (4.5+) are distributed across all size brackets."
        )

    with col_biv2:
        st.subheader("💵 Price vs Rating (Paid Apps Trend)")
        
        # Interactive selector: Paid apps vs all
        show_only_paid = st.checkbox("Only show paid apps", value=True)
        plot_df = df_filtered[df_filtered['Price'] > 0] if show_only_paid else df_filtered
        
        fig_scat_price = px.scatter(
            plot_df, 
            x="Price", 
            y="Rating",
            trendline="ols",  # ordinary least squares linear regression
            opacity=0.6,
            title="App Price vs. App Rating",
            color_discrete_sequence=["#F59E0B"]
        )
        fig_scat_price.update_layout(
            xaxis_title="Price ($)",
            yaxis_title="Rating (1-5)",
            height=450,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_scat_price, use_container_width=True)
        st.markdown(
            "> **Observation:** The linear regression trendline shows whether premium priced apps "
            "receive better or worse user ratings compared to budget alternatives."
        )

    st.write("---")
    
    # Box plots comparison
    col_box1, col_box2 = st.columns(2)
    
    with col_box1:
        st.subheader("👪 Rating Distribution across Content Ratings")
        fig_box_content = px.box(
            df_filtered, 
            x="Content Rating", 
            y="Rating",
            color="Content Rating",
            title="App Rating Spread by Content Rating Target Group",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_box_content.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_box_content, use_container_width=True)
        st.markdown(
            "> **Observation:** The box spreads are reasonably consistent. 'Teen' content ratings "
            "have slightly more compact interquartile ranges (IQR)."
        )

    with col_box2:
        st.subheader("🎭 Rating Distribution across Top 4 Genres")
        
        # Filter for top 4 genres matching notebook
        c_genres = ['Tools', 'Entertainment', 'Medical', 'Education']
        df_top_genres = df_filtered[df_filtered['Genres'].isin(c_genres)]
        
        if len(df_top_genres) > 0:
            fig_box_genres = px.box(
                df_top_genres, 
                x="Genres", 
                y="Rating",
                color="Genres",
                title="App Rating Spread across Top 4 Popular Genres",
                color_discrete_sequence=["#10B981", "#3B82F6", "#EC4899", "#8B5CF6"]
            )
            fig_box_genres.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_box_genres, use_container_width=True)
        else:
            st.warning("Please adjust filters. No records found containing Genres: Tools, Entertainment, Medical, or Education.")
            
        st.markdown(
            "> **Observation:** Medical and Education apps tend to exhibit higher median ratings, "
            "whereas Entertainment apps feature wider overall ratings variance."
        )

# ----------------------------------------------------
# TAB 5: MULTIVARIATE HEATMAPS
# ----------------------------------------------------
with tab5:
    st.markdown("<div class='section-title'>Multivariate Pivot Tables & Heatmaps</div>", unsafe_allow_html=True)
    st.write("Analyze how ratings interact with multiple dimensions (e.g. Content Ratings vs Size Buckets or Review Buckets).")
    
    col_heat_settings, col_heat_plot = st.columns([1, 2])
    
    with col_heat_settings:
        st.markdown("### ⚙️ Heatmap Configurator")
        
        # Option to toggle between Content Rating vs Size Buckets AND Content Rating vs Review Buckets
        analysis_axis = st.selectbox(
            "X-Axis Attribute",
            ["Size Buckets (VL, L, M, H, VH)", "Review Count Buckets"]
        )
        
        # Choose Aggregation function matching notebook instructions
        agg_option = st.selectbox(
            "Aggregate Metric (Rating)",
            ["Median", "Mean", "Minimum", "20th Percentile"]
        )
        
        # Choose color scale
        color_scale_sel = st.selectbox(
            "Color Palette Theme",
            ["Greens", "Viridis", "YlGnBu", "Thermal", "Cividis"]
        )
        
        # Add dynamic bucketing on reviews if chosen
        if analysis_axis == "Review Count Buckets":
            # Let's dynamically construct Review Buckets matching size buckets Q-cut
            df_filtered['Review_Bucket'] = pd.qcut(
                df_filtered['Reviews'], 
                [0, 0.2, 0.4, 0.6, 0.8, 1], 
                labels=["Very Low", "Low", "Medium", "High", "Very High"],
                duplicates='drop'
            )
            index_attr = "Content Rating"
            column_attr = "Review_Bucket"
        else:
            index_attr = "Content Rating"
            column_attr = "Size_Bucket"
            
        # Determine aggregate function
        if agg_option == "Median":
            agg_func = np.median
        elif agg_option == "Mean":
            agg_func = np.mean
        elif agg_option == "Minimum":
            agg_func = np.min
        else: # 20th Percentile
            agg_func = lambda x: np.quantile(x, 0.2)
            
    with col_heat_plot:
        # Generate pivot table
        if len(df_filtered) > 0 and column_attr in df_filtered.columns:
            pivot_table = pd.pivot_table(
                data=df_filtered,
                index=index_attr,
                columns=column_attr,
                values="Rating",
                aggfunc=agg_func
            )
            
            # Format pivot table for plotting (melt or draw matrix)
            # Reorder rows/cols for readability
            pivot_table = pivot_table.fillna(0.0) # Fill NaN cells with 0
            
            # Draw interactive annotated Heatmap with Plotly
            fig_heat = px.imshow(
                pivot_table,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale=color_scale_sel,
                title=f"Heatmap: Ratings ({agg_option}) by {index_attr} & {column_attr}",
                labels=dict(x=column_attr, y=index_attr, color="Rating Value")
            )
            
            fig_heat.update_layout(
                height=450,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.warning("No data matches current filter settings to display heatmap.")
            
    st.markdown(
        "> **Key Case Study Takeaway:** Heatmaps are invaluable for comparing numerical performance "
        "across two categorical variables simultaneously, highlighting sub-segment opportunities "
        "(e.g., highly rated light apps for specific content target audiences)."
    )

# ----------------------------------------------------
# TAB 6: TEMPORAL & MONTHLY INSTAL TRENDS
# ----------------------------------------------------
with tab6:
    st.markdown("<div class='section-title'>Temporal Patterns & Installs Distribution</div>", unsafe_allow_html=True)
    st.write("Understand performance fluctuations over time (months) and proportional volume releases.")
    
    col_temp1, col_temp2 = st.columns(2)
    
    with col_temp1:
        st.subheader("📅 Monthly Average App Ratings")
        
        # Calculate monthly average rating
        monthly_avg_rating = df_filtered.groupby("updated_month")[['Rating']].mean().reset_index()
        # Map month integers to names
        month_names = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        monthly_avg_rating['Month_Name'] = monthly_avg_rating['updated_month'].map(month_names)
        
        # Sort by month order
        monthly_avg_rating = monthly_avg_rating.sort_values('updated_month')
        
        fig_temp_line = px.line(
            monthly_avg_rating,
            x="Month_Name",
            y="Rating",
            markers=True,
            title="Monthly Average Ratings Trend",
            color_discrete_sequence=["#636EFA"]
        )
        
        fig_temp_line.update_layout(
            xaxis_title="Month Updated",
            yaxis_title="Average Rating",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_temp_line, use_container_width=True)
        st.markdown(
            "> **Insight:** Shows ratings stability based on release months. Allows "
            "diagnosing if seasonal releases perform differently."
        )

    with col_temp2:
        st.subheader("📊 Stacked Monthly Installs Proportion")
        
        # Toggle between Absolute installs vs Percentage distribution proportions
        stacked_mode = st.radio("Stacking Unit Mode", ["Percentage Proportions", "Absolute Installs Sum"], horizontal=True)
        
        # Create Pivot table for Content Rating and updated Month with values set to Installs sum
        monthly_installs = pd.pivot_table(
            data=df_filtered, 
            values="Installs", 
            index="updated_month", 
            columns="Content Rating", 
            aggfunc=sum
        ).fillna(0.0)
        
        # Map indices to names
        monthly_installs.index = monthly_installs.index.map(month_names)
        
        # Reorder months logically
        ordered_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        existing_months = [m for m in ordered_months if m in monthly_installs.index]
        monthly_installs = monthly_installs.reindex(existing_months)
        
        if stacked_mode == "Percentage Proportions":
            # Normalise rows to proportions
            monthly_installs_perc = monthly_installs.apply(lambda x: x / x.sum() if x.sum() > 0 else 0, axis=1) * 100
            
            fig_stacked = px.bar(
                monthly_installs_perc,
                title="Monthly Installs Share by Content Rating (%)",
                labels={"value": "Install Share (%)", "index": "Month"},
                color_discrete_sequence=px.colors.qualitative.Bold
            )
        else:
            fig_stacked = px.bar(
                monthly_installs,
                title="Monthly Total Installs Sum",
                labels={"value": "Total Installs Count", "index": "Month"},
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
        fig_stacked.update_layout(
            barmode="stack",
            xaxis_title="Month Updated",
            height=370,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
    st.write("---")
    st.info(
        "💡 **Pair Programming Tip:** This Streamlit dashboard is fully interactive. Use the sidebar on the "
        "left to restrict app analysis to specific categories, ratings, or app types, and observe how all "
        "metrics and visualizations update dynamically in real-time."
    )
