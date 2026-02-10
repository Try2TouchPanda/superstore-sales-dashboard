# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df['sales_clean'] = df['sales'].astype(str).str.replace(',', '').astype(float)
    df['profit_clean'] = df['profit'].astype(str).str.replace(',', '').astype(float)
    df = df[df['sales_clean'] > 0]
    df['profit_margin'] = (df['profit_clean'] / df['sales_clean']) * 100
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True)
    
    # Clean discount if exists
    if 'discount' in df.columns:
        df['discount_clean'] = df['discount'].astype(str).str.replace(',', '').astype(float)
    
    return df

df = load_data()

# ============================================
# HEADER
# ============================================

st.title("📊 Superstore Sales Dashboard")
st.markdown("Interactive analysis of sales, profit, and margins (2011-2014)")

# ============================================
# SIDEBAR FILTERS
# ============================================

st.sidebar.header("🔍 Filters")

# Date range
min_date = df['order_date'].min().date()
max_date = df['order_date'].max().date()
start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Category
selected_category = st.sidebar.selectbox("Select Category", ["All"] + list(df['category'].unique()))
selected_segment = st.sidebar.selectbox("Select Segment", ["All"] + list(df['segment'].unique()))

# Region
selected_regions = st.sidebar.multiselect("Select Regions", list(df['region'].unique()), default=[])

# Sales range
min_sales_val = float(df['sales_clean'].min())
max_sales_val = float(df['sales_clean'].max())
min_sales, max_sales = st.sidebar.slider("Sales Range ($)", min_sales_val, max_sales_val, 
                                         (min_sales_val, max_sales_val), step=100.0)

# ============================================
# APPLY FILTERS
# ============================================

filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df['order_date'].dt.date >= start_date) & 
                          (filtered_df['order_date'].dt.date <= end_date)]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if selected_segment != "All":
    filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
if selected_regions:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
filtered_df = filtered_df[(filtered_df['sales_clean'] >= min_sales) & 
                          (filtered_df['sales_clean'] <= max_sales)]

st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")

# ============================================
# KPI CARDS
# ============================================

st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df['sales_clean'].sum()
    st.metric("💰 Total Sales", f"${total_sales/1e6:.2f}M", f"{len(filtered_df):,} orders")

with col2:
    total_profit = filtered_df['profit_clean'].sum()
    margin = (total_profit/total_sales*100) if total_sales > 0 else 0
    st.metric("📈 Total Profit", f"${total_profit/1e6:.2f}M", f"{margin:.1f}% margin")

with col3:
    aov = filtered_df['sales_clean'].mean()
    st.metric("🛒 Avg Order Value", f"${aov:,.0f}")

with col4:
    losses = len(filtered_df[filtered_df['profit_clean'] < 0])
    loss_pct = (losses/len(filtered_df)*100) if len(filtered_df) > 0 else 0
    st.metric("⚠️ Loss Orders", f"{losses:,}", f"{loss_pct:.1f}%", delta_color="inverse")

# ============================================
# MAIN CHARTS
# ============================================

st.subheader("📊 Overview")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    if len(filtered_df) > 0:
        cat_sales = filtered_df.groupby('category')['sales_clean'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = {'Technology': '#2E86AB', 'Furniture': '#A23B72', 'Office Supplies': '#F18F01'}
        bars = ax.bar(cat_sales.index, cat_sales.values, color=[colors.get(c, 'gray') for c in cat_sales.index])
        ax.set_ylabel("Sales ($)")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h, f'${h/1e6:.1f}M', ha='center', va='bottom', fontsize=9)
        st.pyplot(fig)
    else:
        st.warning("No data")

with col_chart2:
    if len(filtered_df) > 0:
        cat_margin = filtered_df.groupby('category')['profit_margin'].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = {'Technology': '#2E86AB', 'Furniture': '#A23B72', 'Office Supplies': '#F18F01'}
        bars = ax.bar(cat_margin.index, cat_margin.values, color=[colors.get(c, 'gray') for c in cat_margin.index])
        ax.set_ylabel("Profit Margin (%)")
        ax.axhline(y=0, color='red', linestyle='--')
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h, f'{h:.1f}%', ha='center', va='bottom', fontsize=9)
        st.pyplot(fig)
    else:
        st.warning("No data")

# ============================================
# ADVANCED ANALYSIS
# ============================================

st.markdown("---")
st.subheader("🔍 Advanced Analysis")

col_adv1, col_adv2 = st.columns(2)

with col_adv1:
    st.markdown("**💸 Sales vs Profit Scatter**")
    if len(filtered_df) > 0:
        plot_df = filtered_df.sample(min(500, len(filtered_df)))
        fig, ax = plt.subplots(figsize=(8, 6))
        for cat in plot_df['category'].unique():
            d = plot_df[plot_df['category'] == cat]
            ax.scatter(d['sales_clean'], d['profit_clean'], label=cat, alpha=0.6, s=40)
        ax.axhline(y=0, color='red', linestyle='--')
        ax.set_xlabel('Sales ($)')
        ax.set_ylabel('Profit ($)')
        ax.legend(fontsize=8)
        st.pyplot(fig)
        
        disasters = len(filtered_df[(filtered_df['sales_clean'] > 1000) & (filtered_df['profit_clean'] < 0)])
        if disasters > 0:
            st.error(f"⚠️ {disasters} discount disasters")

with col_adv2:
    st.markdown("**📊 Profit Margin Distribution**")
    if len(filtered_df) > 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        n, bins, patches = ax.hist(filtered_df['profit_margin'], bins=25, alpha=0.7, color='steelblue', edgecolor='black')
        for patch, left in zip(patches, bins[:-1]):
            if left < 0:
                patch.set_facecolor('#e74c3c')
        ax.axvline(x=0, color='red', linestyle='--')
        ax.axvline(x=filtered_df['profit_margin'].mean(), color='green', linestyle='--')
        ax.set_xlabel('Profit Margin (%)')
        ax.set_ylabel('Orders')
        st.pyplot(fig)
        
        neg_pct = (filtered_df['profit_margin'] < 0).mean() * 100
        st.info(f"{neg_pct:.1f}% orders are unprofitable")

# ============================================
# TOP/BOTTOM PRODUCTS
# ============================================

st.markdown("---")
st.subheader("🏆 Product Performance")

col_top, col_bottom = st.columns(2)

with col_top:
    st.markdown("**⭐ Top 10 Most Profitable**")
    if len(filtered_df) > 0:
        top10 = filtered_df.nlargest(10, 'profit_clean')[['product_name', 'profit_clean', 'profit_margin']]
        top10['profit_clean'] = top10['profit_clean'].apply(lambda x: f"${x:,.0f}")
        top10['profit_margin'] = top10['profit_margin'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(top10, hide_index=True, use_container_width=True)

with col_bottom:
    st.markdown("**⚠️ Top 10 Biggest Losses**")
    if len(filtered_df) > 0:
        bottom10 = filtered_df.nsmallest(10, 'profit_clean')[['product_name', 'profit_clean', 'profit_margin']]
        bottom10['profit_clean'] = bottom10['profit_clean'].apply(lambda x: f"${x:,.0f}")
        bottom10['profit_margin'] = bottom10['profit_margin'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(bottom10, hide_index=True, use_container_width=True)

# ============================================
# DISCOUNT ANALYSIS (if data available)
# ============================================

if 'discount_clean' in filtered_df.columns:
    st.markdown("---")
    st.subheader("💰 Discount Impact")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("**Discount vs Margin**")
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(filtered_df['discount_clean'], filtered_df['profit_margin'], 
                           alpha=0.5, c=filtered_df['sales_clean'], cmap='viridis', s=30)
        ax.set_xlabel('Discount Rate')
        ax.set_ylabel('Profit Margin (%)')
        ax.axhline(y=0, color='red', linestyle='--')
        plt.colorbar(scatter, label='Sales ($)')
        st.pyplot(fig)
    
    with col_d2:
        st.markdown("**Margin by Discount Range**")
        filtered_df['disc_range'] = pd.cut(filtered_df['discount_clean'], 
                                          bins=[0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                          labels=['0-10%', '10-20%', '20-30%', '30-50%', '50%+'])
        disc_margin = filtered_df.groupby('disc_range')['profit_margin'].mean()
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#8e44ad']
        bars = ax.bar(disc_margin.index, disc_margin.values, color=colors[:len(disc_margin)])
        ax.set_ylabel('Avg Margin (%)')
        ax.axhline(y=0, color='red', linestyle='--')
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h, f'{h:.1f}%', ha='center', va='bottom')
        st.pyplot(fig)

# ============================================
# DATA EXPORT
# ============================================

st.markdown("---")
st.subheader("💾 Export Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered CSV", csv, 
                   f"sales_filtered_{start_date}_{end_date}.csv", "text/csv")

st.dataframe(filtered_df[['order_date', 'category', 'segment', 'region', 'sales_clean', 
                         'profit_clean', 'profit_margin']].head(50), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Superstore Sales Analysis 2011-2014")