E-commerce Revenue Analysis
Project Overview
This project analyzes e-commerce transaction data to uncover revenue drivers, customer behavior, and product performance.
The goal is to move beyond descriptive analysis into actionable business insights.
_____________________________________________
Objectives
Understand revenue trends over time
Identify key drivers of revenue (orders vs value)
Detect and measure the impact of outliers
Analyze customer vs product contribution
Support data-driven decision making
___________________________________________
Dataset
The dataset includes:
Orders
Order Items
Payments
Products
________________________________________________
Tools Used
Python (Pandas, Matplotlib)
Power BI
_______________________________________
Key Insights
1. Revenue is primarily driven by order volume
Revenue trend closely mirrors the number of orders
When orders dropped sharply, revenue dropped accordingly
Indicates growth is volume-driven, not price-driven

2. Outliers have a significant impact on revenue
Only ~7.6% of transactions are outliers
These contribute ~34% of total revenue
A small segment has disproportionate financial impact

3. Customer contribution is widely distributed
~48,766 customers are needed to reach 80% of revenue
Out of ~99,440 total customers
Revenue is not concentrated in a small VIP segment

4. Product contribution shows moderate concentration
~8,477 products generate 80% of revenue
Out of ~32,951 total products
Some level of concentration exists at product level
Products have more influence than customers

5. Revenue distribution is highly right-skewed
Most transactions fall in low price range (0–500)
Few transactions reach very high values (up to ~14,000)
Explains why mean is inflated by high-value transactions
6. Average Order Value (AOV) is unstable due to outliers
With outliers: fluctuates in higher range
Without outliers: stable in lower range
AOV alone can be misleading without segmentation
__________________________________________________
Dashboard Preview:
original Dashboard
sales_comparison
____________________________________
Project Structure:
sales_analysis.py → Data cleaning & analysis
Original dashboard.png → Main dashboard
sales_dashboard_no_outliers.png → Cleaned analysis
sales_comparison.png → With vs without outliers
_____________________________________
Business Recommendations:
1. Focus on increasing order volume
Since revenue is driven by number of orders
Invest in:
Marketing campaigns
Conversion optimization
Customer acquisition
2. Segment high-value transactions (Outliers)
Create a separate strategy for high spenders
Examples:
VIP programs
Personalized offers
Retention strategies
3. Optimize product portfolio
Products contribute more to revenue concentration than customers
Focus on:
Top-performing products
Bundling strategies
Pricing optimization
4. Do not rely on average metrics alone
AOV is distorted by outliers
Always analyze:
With vs without outliers
Median alongside mean
5. Investigate sudden drops in revenue
Sharp drop observed in last period likely due to: 
Data incompleteness OR
Operational issue
Requires validation before business action
______________________________________________
How to Run
Load datasets (orders, items, payments, products)
Run sales_analysis.py
Explore visualizations
______________________________________________
Final Conclusion
Revenue growth in this business is primarily driven by transaction volume, while a small fraction of high-value transactions significantly impacts overall performance.
Product-level optimization offers the strongest opportunity for improving revenue efficiency.
