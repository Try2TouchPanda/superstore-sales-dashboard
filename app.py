import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("sales_data.csv")

print("Shape of Dataset:", df.shape)
print("\nDataset Information")
print(df.info())
print("\nStatistical Summary")
print(df.describe())
print("\nMissing values in each column")
print(df.isnull().sum())
print("\nColumn names:")
print(df.columns)
print("\nSample order_date values:")
print(df['order_date'].head())
print("\nData type of order_date:")
print(df['order_date'].dtype)

# Define your brand colors (use these everywhere)
COLORS = {
    'primary': '#2E86AB',      # Blue - main brand
    'secondary': '#A23B72',    # Magenta - accent
    'tertiary': '#F18F01',     # Orange - highlight
    'success': '#2ecc71',      # Green - positive
    'danger': '#e74c3c',       # Red - negative/warning
    'warning': '#f1c40f',      # Yellow - caution
    'neutral': '#95a5a6'       # Gray - neutral
}

# Category colors (consistent across all charts)
CATEGORY_COLORS = {
    'Technology': '#2E86AB',      # Blue
    'Furniture': '#A23B72',       # Magenta  
    'Office Supplies': '#F18F01'  # Orange
}

# Segment colors (consistent across all charts)
SEGMENT_COLORS = {
    'Consumer': '#e74c3c',      # Red - emotional
    'Corporate': '#3498db',     # Blue - professional
    'Home Office': '#2ecc71'    # Green - growth
}

# Set global matplotlib style
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 100

print("Style guide loaded!")
print("Category colors:", CATEGORY_COLORS)
print("Segment colors:", SEGMENT_COLORS)

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    dayfirst=True
)

print("\nConverted order_date:")
print(df["order_date"].head())

# Convert ship_date to datetime
df["ship_date"] = pd.to_datetime(
    df["ship_date"],
    format="mixed",
    dayfirst=True
)

print("\nConverted ship_date:")
print(df["ship_date"].head())

# Create time features
df['month'] = df['order_date'].dt.month
df['month_name'] = df['order_date'].dt.month_name()

print("\nTime features:")
print(df[['order_date', 'year', 'month', 'month_name']].head())

# Clean sales data (remove commas and convert to number)
df['sales_clean'] = df['sales'].astype(str).str.replace(',', '').astype(float)

# Create year-month grouping
df['year_month'] = df['order_date'].dt.to_period('M')
monthly_sales = df.groupby('year_month')['sales_clean'].sum().reset_index()

# Convert period to timestamp for plotting
monthly_sales['year_month'] = monthly_sales['year_month'].dt.to_timestamp()

print("\nMonthly sales data:")
print(monthly_sales.head())

# Create the plot
# ============================================
# CHART 1: MONTHLY SALES TREND (Line Chart)
# ============================================

plt.figure(figsize=(14, 6))

plt.plot(monthly_sales['year_month'], monthly_sales['sales_clean'], 
         marker='o', linewidth=2.5, markersize=5, 
         color=COLORS['primary'], label='Monthly Sales')

plt.fill_between(monthly_sales['year_month'], monthly_sales['sales_clean'], 
                 alpha=0.3, color=COLORS['primary'])

plt.title("Monthly Sales Trend (2011-2014)", fontsize=16, fontweight='bold', pad=20)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Total Sales ($)", fontsize=12)
plt.xticks(rotation=45)

# Format y-axis to millions
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='upper left')

# Add annotation for peak
max_idx = monthly_sales['sales_clean'].idxmax()
max_row = monthly_sales.loc[max_idx]
plt.annotate(f'Peak: ${max_row["sales_clean"]/1e6:.2f}M', 
             xy=(max_row['year_month'], max_row['sales_clean']),
             xytext=(10, 10), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['warning'], alpha=0.7),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

plt.tight_layout()
plt.savefig('chart1_monthly_trend.png', dpi=300, bbox_inches='tight')
print("Saved: chart1_monthly_trend.png")
plt.show()

# Check regions
print("Regions:", df['region'].unique())
print("Count:", df['region'].nunique())

# Check markets  
print("\nMarkets:", df['market'].unique())
print("Count:", df['market'].nunique())

# Check segments
print("\nSegments:", df['segment'].unique())
print("Count:", df['segment'].nunique())

# Check categories
print("\nCategories:", df['category'].unique())
print("Count:", df['category'].nunique())

# Check if Africa appears in both columns
print("Africa in region:", 'Africa' in df['region'].unique())
print("Africa in market:", 'Africa' in df['market'].unique())

# See sample rows where region = 'Africa'
print(df[df['region'] == 'Africa'][['region', 'market', 'country']].head())

# Group and clean aggregation
segment_sales = df.groupby('segment')['sales_clean'].sum()

# Verify it's a Series with 3 values
print("Type:", type(segment_sales))
print("Values:\n", segment_sales)
print("Sum check:", segment_sales.sum(), "==", df['sales_clean'].sum())



# Group and sort ONCE
category_sales = df.groupby('category')['sales_clean'].sum().sort_values(ascending=False)

print("Category Sales Ranking:")
for cat, sales in category_sales.items():
    pct = (sales / category_sales.sum()) * 100
    print(f"{cat}: ${sales:,.0f} ({pct:.1f}%)")

# Create publication-quality pie chart
plt.figure(figsize=(10, 8))

# Use consistent category colors
colors_list = [CATEGORY_COLORS[cat] for cat in category_sales.index]

wedges, texts, autotexts = plt.pie(
    category_sales.values,
    labels=None,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors_list,
    explode=[0.03, 0.03, 0.03],
    pctdistance=0.75,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_weight('bold')

plt.legend(wedges, category_sales.index, title="Product Categories",
           loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.title("Revenue Distribution by Product Category",
          fontsize=16, fontweight='bold', pad=20)

plt.figtext(0.5, 0.02,
            f"Total: ${category_sales.sum()/1e6:.2f}M | Tech leads with 14% margin",
            ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout()
plt.savefig('chart3_category_pie.png', dpi=300, bbox_inches='tight')
print("Saved: chart3_category_pie.png")
plt.show()

# Group segment data
segment_sales = df.groupby('segment')['sales_clean'].sum().sort_values(ascending=False)

print("\nSegment Sales Ranking:")
for seg, sales in segment_sales.items():
    pct = (sales / segment_sales.sum()) * 100
    print(f"{seg}: ${sales:,.0f} ({pct:.1f}%)")

plt.figure(figsize=(10, 8))

# Use consistent segment colors
colors_list = [SEGMENT_COLORS[seg] for seg in segment_sales.index]

wedges, texts, autotexts = plt.pie(
    segment_sales.values,
    labels=None,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors_list,
    explode=[0.03, 0.03, 0.03],
    pctdistance=0.75,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_weight('bold')

plt.legend(wedges, segment_sales.index, title="Customer Segments", 
           loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.title("Revenue Distribution by Customer Segment", 
          fontsize=16, fontweight='bold', pad=20)

plt.figtext(0.5, 0.02, 
            f"Total: ${segment_sales.sum()/1e6:.2f}M | {len(df):,} orders | Avg Margin: 11.6%",
            ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout()
plt.savefig('chart2_segment_pie.png', dpi=300, bbox_inches='tight')
print("Saved: chart2_segment_pie.png")
plt.show()

# ============================================
# DAY 8: PROFIT VS SALES ANALYSIS
# ============================================

# Step 1: Clean profit column (same pattern as sales)
print("\n" + "="*50)
print("PROFIT ANALYSIS")
print("="*50)

print("Sample profit values:")
print(df['profit'].head(10))
print(f"\nProfit dtype: {df['profit'].dtype}")

# Remove commas and convert to float
df['profit_clean'] = df['profit'].astype(str).str.replace(',', '').astype(float)

print(f"\nProfit range: ${df['profit_clean'].min():,.0f} to ${df['profit_clean'].max():,.0f}")
print(f"Negative profits (losses): {(df['profit_clean'] < 0).sum()} orders")

# Step 2: Fix data quality issue (remove zero sales)
print(f"\nOrders with $0 sales: {(df['sales_clean'] == 0).sum()}")
df = df[df['sales_clean'] > 0].copy()  # Keep only rows with sales > 0

# Step 3: Calculate profit margin
df['profit_margin'] = (df['profit_clean'] / df['sales_clean']) * 100

print("\nProfit margin statistics:")
print(df['profit_margin'].describe())

print(f"\nHighest margin: {df['profit_margin'].max():.1f}%")
print(f"Lowest margin: {df['profit_margin'].min():.1f}%")
print(f"Negative margins (losses): {(df['profit_margin'] < 0).sum()} orders")

# Step 4: Find Discount Disasters (high sales, negative profit)
discount_disasters = df[(df['sales_clean'] > 1000) & (df['profit_clean'] < 0)]
print(f"\nDiscount disasters: {len(discount_disasters)} orders")
print(discount_disasters[['product_name', 'sales_clean', 'profit_clean', 'discount', 'profit_margin']].head())

# Find Gold Mines (high margin)
gold_mines = df[df['profit_margin'] > 50]
print(f"\nHigh-margin products (>50%): {len(gold_mines)} orders")
print(gold_mines[['product_name', 'sales_clean', 'profit_clean', 'profit_margin']].head())

# Step 5: Category-Level Profit Analysis
print("\n" + "="*50)
print("PROFITABILITY BY CATEGORY")
print("="*50)

category_profit = df.groupby('category').agg({
    'sales_clean': 'sum',
    'profit_clean': 'sum',
    'profit_margin': 'mean'
}).round(2)

category_profit['overall_margin'] = (category_profit['profit_clean'] / category_profit['sales_clean'] * 100).round(1)

print(category_profit)

# ============================================
# VISUALIZATION 1: Profit Margin by Category (Bar Chart)
# ============================================

category_margin = df.groupby('category')['profit_margin'].mean().sort_values(ascending=False)

# Reorder to match color priority: Tech, Office, Furniture
category_margin = category_margin.reindex(['Technology', 'Office Supplies', 'Furniture'])

plt.figure(figsize=(10, 6))

bars = plt.bar(category_margin.index, category_margin.values,
               color=[CATEGORY_COLORS[cat] for cat in category_margin.index],
               edgecolor='black', linewidth=1.2)

plt.title('Average Profit Margin by Category', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Profit Margin (%)', fontsize=12)
plt.xlabel('')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add break-even line
plt.axhline(y=0, color=COLORS['danger'], linestyle='--', linewidth=2, alpha=0.7, label='Break-even')

# Add industry benchmark (typical retail: 10%)
plt.axhline(y=10, color=COLORS['success'], linestyle=':', linewidth=2, alpha=0.7, label='Industry Benchmark (10%)')

plt.legend(loc='upper right')
plt.ylim(-5, 20)
plt.grid(True, alpha=0.3, axis='y')

# Add warning text for Furniture
plt.text(2, 3, '[WARNING] Below benchmark', ha='center', fontsize=10, 
         color=COLORS['danger'], fontweight='bold')

plt.tight_layout()
plt.savefig('chart4_profit_margin.png', dpi=300, bbox_inches='tight')
print("Saved: chart4_profit_margin.png")
plt.show()

# ============================================
# VISUALIZATION 2: Sales vs Profit Scatter Plot
# ============================================

# ============================================
# CHART 5: SALES VS PROFIT (Scatter Plot)
# ============================================

plt.figure(figsize=(12, 8))

# Create scatter with category colors
for category in df['category'].unique():
    cat_data = df[df['category'] == category]
    plt.scatter(cat_data['sales_clean'], cat_data['profit_clean'],
                c=CATEGORY_COLORS[category], label=category,
                alpha=0.6, s=40, edgecolors='black', linewidth=0.5)

plt.axhline(y=0, color=COLORS['danger'], linestyle='--', linewidth=2, alpha=0.8, label='Break-even')
plt.axvline(x=1000, color=COLORS['warning'], linestyle=':', linewidth=2, alpha=0.8, label='High Sales Threshold ($1K)')

plt.xlabel('Sales ($)', fontsize=12)
plt.ylabel('Profit ($)', fontsize=12)
plt.title('Sales vs Profit: The "Kill Zone" of Discount Disasters', 
          fontsize=16, fontweight='bold', pad=20)

# Highlight discount disasters zone
plt.fill_between([1000, 10000], [-2000, -2000], [0, 0], 
                 alpha=0.2, color=COLORS['danger'], label='Discount Disaster Zone')

plt.legend(loc='upper right', title='Categories')
plt.grid(True, alpha=0.3)

# Add annotation
plt.text(2500, -1500, '435 orders here\n(high sales, negative profit)', 
         fontsize=10, color=COLORS['danger'], fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('chart5_sales_profit_scatter.png', dpi=300, bbox_inches='tight')
print("Saved: chart5_sales_profit_scatter.png")
plt.show()



# ============================================
# CHART 6: PROFIT MARGIN BY SEGMENT (Bar Chart)
# ============================================

segment_margin = df.groupby('segment')['profit_margin'].mean()
# Reorder: Home Office, Corporate, Consumer (by margin)
segment_margin = segment_margin.sort_values(ascending=False)

plt.figure(figsize=(10, 6))

bars = plt.bar(segment_margin.index, segment_margin.values,
               color=[SEGMENT_COLORS[seg] for seg in segment_margin.index],
               edgecolor='black', linewidth=1.2)

plt.title('Profit Margin by Customer Segment', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Profit Margin (%)', fontsize=12)
plt.xlabel('')

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.2,
             f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add benchmark line
plt.axhline(y=10, color=COLORS['success'], linestyle=':', linewidth=2, alpha=0.7, label='Industry Benchmark (10%)')

plt.legend(loc='upper right')
plt.ylim(0, 15)
plt.grid(True, alpha=0.3, axis='y')

# Add insight text
plt.text(0.5, 13, 'Home Office: Small but profitable!', 
         fontsize=10, color=COLORS['success'], fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('chart6_segment_margin.png', dpi=300, bbox_inches='tight')
print("Saved: chart6_segment_margin.png")
plt.show()

# ============================================
# DASHBOARD LAYOUT PREVIEW (For Streamlit)
# ============================================

print("\n" + "="*60)
print("DASHBOARD LAYOUT PLAN")
print("="*60)

dashboard_layout = """
┌─────────────────────────────────────────────────────────────┐
│  SUPERSTORE SALES DASHBOARD          [Filter: Region ▼]    │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  KPI Card 1  │  │  KPI Card 2  │  │  KPI Card 3  │      │
│  │ Total Sales  │  │ Total Profit │  │ Avg Margin   │      │
│  │   $12.6M     │  │   $1.47M     │  │    11.6%     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  [Chart 1: Monthly Sales Trend]                             │
│  Line chart with growth trajectory                          │
├─────────────────────────────────────────────────────────────┤
│  [Chart 2: Segment Pie]        [Chart 3: Category Pie]      │
│  Revenue distribution          Revenue distribution         │
├─────────────────────────────────────────────────────────────┤
│  [Chart 4: Profit Margin by Category]                       │
│  Bar chart showing Furniture problem                        │
├─────────────────────────────────────────────────────────────┤
│  [Chart 5: Sales vs Profit Scatter]                         │
│  Interactive: Hover to see discount disasters               │
├─────────────────────────────────────────────────────────────┤
│  [Chart 6: Segment Margin]     [Data Table: Top Products]   │
│  Who's most profitable          Sortable, searchable        │
└─────────────────────────────────────────────────────────────┘
"""

print(dashboard_layout)

print("\nKey Insights for Viva:")
print("1. Technology = highest margin (14%) despite mid-level sales")
print("2. Furniture = margin killer (7%) due to 60% discounts")
print("3. Home Office = smallest segment but highest margin (12%)")
print("4. 435 discount disasters = $1M+ in preventable losses")
print("5. Consumer volume ≠ profit (11.5% vs Home Office 12%)")


# ============================================
# AUTOMATED REPORT GENERATOR (Fixed - No Emojis)
# ============================================

print("\n" + "="*60)
print("EXECUTIVE SUMMARY REPORT")
print("="*60)

total_sales = df['sales_clean'].sum()
total_profit = df['profit_clean'].sum()
overall_margin = (total_profit / total_sales) * 100
loss_orders = (df['profit_clean'] < 0).sum()

report = f"""
SUPERSTORE SALES ANALYSIS REPORT (2011-2014)
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

FINANCIAL OVERVIEW:
- Total Revenue: ${total_sales/1e6:.2f} million
- Total Profit: ${total_profit/1e6:.2f} million  
- Overall Margin: {overall_margin:.1f}%
- Total Orders: {len(df):,}
- Loss-making Orders: {loss_orders:,} ({loss_orders/len(df)*100:.1f}%)

SEGMENT PERFORMANCE:
- Consumer: 51% of sales, 11.5% margin (volume leader, margin laggard)
- Corporate: 30% of sales, 11.6% margin (balanced)
- Home Office: 18% of sales, 12.0% margin (efficiency champion)

CATEGORY PERFORMANCE:
- Technology: 37% of sales, 14.0% margin [STAR PERFORMER]
- Office Supplies: 30% of sales, 13.7% margin [SOLID]
- Furniture: 33% of sales, 7.0% margin [MARGIN KILLER]

CRITICAL ISSUES:
- 435 'discount disasters' (high sales, negative profit)
- Worst case: 60% discount on furniture = -133% margin
- Furniture shipping costs eroding profitability

RECOMMENDATIONS:
1. Cap furniture discounts at 20% (currently seeing 60%)
2. Prioritize Home Office segment expansion (12% margin)
3. Bundle high-margin Office Supplies with Technology
4. Discontinue or reprice SAFCO Executive Armchair
5. Investigate Technology category for expansion

FILES GENERATED:
- chart1_monthly_trend.png
- chart2_segment_pie.png  
- chart3_category_pie.png
- chart4_profit_margin.png
- chart5_sales_profit_scatter.png
- chart6_segment_margin.png
"""

print(report)

# Save report to file with UTF-8 encoding (handles all characters)
with open('executive_summary_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
print("\nSaved: executive_summary_report.txt")