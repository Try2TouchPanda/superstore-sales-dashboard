import pandas as pd
import matplotlib.pyplot as plt

# Load and clean (minimal version)
df = pd.read_csv("sales_data.csv")
df['sales_clean'] = df['sales'].astype(str).str.replace(',', '').astype(float)

# Group and sort ONCE
category_sales = df.groupby('category')['sales_clean'].sum().sort_values(ascending=False)

print("Category Sales Ranking:")
for cat, sales in category_sales.items():
    pct = (sales / category_sales.sum()) * 100
    print(f"{cat}: ${sales:,.0f} ({pct:.1f}%)")

# Create publication-quality pie chart
plt.figure(figsize=(10, 8))

# Professional color palette (coordinated)
colors = ['#2E86AB', '#A23B72', '#F18F01']  # Blue, Magenta, Orange — modern contrast

wedges, texts, autotexts = plt.pie(
    x=category_sales.values,
    labels=None,  # We'll use legend instead for cleaner look
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=[0.03, 0.03, 0.03],
    pctdistance=0.75,  # Pull percentages inward
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}  # White borders between slices
)

# Style the percentage text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_weight('bold')

# Add legend (better than labels for readability)
plt.legend(
    wedges, 
    category_sales.index,
    title="Categories",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1)  # Place legend to the right
)

# Title with context
plt.title("Revenue Distribution by Product Category", 
          fontsize=16, 
          fontweight='bold',
          pad=20)

# Add data source note at bottom
plt.figtext(0.5, 0.02, 
            f"Source: {len(df):,} orders | Total Revenue: ${category_sales.sum()/1e6:.2f}M",
            ha='center', 
            fontsize=9, 
            style='italic',
            color='gray')

plt.tight_layout()

# SAVE for your report (DO THIS!)
plt.savefig('category_sales_pie.png', dpi=300, bbox_inches='tight')
print("\nSaved: category_sales_pie.png")

plt.show()
# Group segment data
segment_sales = df.groupby('segment')['sales_clean'].sum().sort_values(ascending=False)

print("\nSegment Sales Ranking:")
for seg, sales in segment_sales.items():
    pct = (sales / segment_sales.sum()) * 100
    print(f"{seg}: ${sales:,.0f} ({pct:.1f}%)")

# Create matching pie chart
plt.figure(figsize=(10, 8))

# Different but coordinated colors
colors = ['#E63946', '#457B9D', '#1D3557']  # Red, Blue, Navy — business feel

wedges, texts, autotexts = plt.pie(
    x=segment_sales.values,
    labels=None,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=[0.03, 0.03, 0.03],
    pctdistance=0.75,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_weight('bold')

plt.legend(
    wedges,
    segment_sales.index,
    title="Customer Segments",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1)
)

plt.title("Revenue Distribution by Customer Segment",
          fontsize=16,
          fontweight='bold',
          pad=20)

plt.figtext(0.5, 0.02,
            f"Source: {len(df):,} orders | Total Revenue: ${segment_sales.sum()/1e6:.2f}M",
            ha='center',
            fontsize=9,
            style='italic',
            color='gray')

plt.tight_layout()
plt.savefig('segment_sales_pie.png', dpi=300, bbox_inches='tight')
print("Saved: segment_sales_pie.png")

plt.show()