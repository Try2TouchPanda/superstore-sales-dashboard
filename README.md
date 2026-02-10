# Superstore Sales Analysis Dashboard

## 📊 Project Overview
Interactive dashboard analyzing 51,289 sales orders from 2011-2014, revealing critical insights about profitability, discount disasters, and customer segments.

## 🎯 Key Features
- **Real-time filtering** by date, category, segment, region, and sales range
- **Profitability analysis** identifying 12,542 loss-making orders
- **Discount impact visualization** showing 435 "discount disasters"
- **Interactive charts** with hover details and drill-down capability
- **CSV export** for further analysis

## 🛠️ Tech Stack
- **Python** - Data processing
- **Pandas** - Data manipulation
- **Matplotlib** - Static visualizations
- **Streamlit** - Interactive dashboard

## 📈 Key Insights
1. **Technology** leads with 14.0% profit margin
2. **Furniture** is the margin killer at only 7.0%
3. **Home Office** segment has highest margin (12.0%) despite smallest volume
4. **24% of orders are unprofitable** due to excessive discounting
5. **Consumer segment** drives 51% of sales but lowest margin

## 🚀 How to Run
```bash
pip install streamlit pandas matplotlib
streamlit run dashboard.py