
---

```markdown
# Methodology: Superstore Sales Analysis

## 1. Data Collection
- **Source:** Superstore sales dataset (CSV)
- **Records:** 51,289 orders
- **Time Period:** 2011-2014
- **Fields:** Order date, ship date, customer info, product details, sales, profit, discount

## 2. Data Cleaning
### Issues Found:
- Sales/profit columns stored as strings with commas
- 1 order with $0 sales (division by zero risk)
- 12,542 orders with negative profit

### Cleaning Steps:
```python
# Remove commas and convert to float
df['sales_clean'] = df['sales'].astype(str).str.replace(',', '').astype(float)
df['profit_clean'] = df['profit'].astype(str).str.replace(',', '').astype(float)

# Remove zero sales to prevent division errors
df = df[df['sales_clean'] > 0]

# Calculate profit margin
df['profit_margin'] = (df['profit_clean'] / df['sales_clean']) * 100