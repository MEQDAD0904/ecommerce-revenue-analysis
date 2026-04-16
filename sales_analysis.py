import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# upload data
customers = pd.read_csv('customers.csv')
orders = pd.read_csv('orders.csv')
order_items = pd.read_csv('order_items.csv')
products = pd.read_csv('products.csv')
payments = pd.read_csv('order_payments.csv')

# data cleaning
order_items = order_items.dropna(subset=["price", "freight_value"])
payments = payments.dropna(subset=["payment_value"])
# transform data
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

# reconciliation operation
items_total = order_items.groupby("order_id").agg({
    "price" : "sum",
    "freight_value" : "sum"
})
items_total["total_items"] = items_total["price"] + items_total["freight_value"]
payments_total = payments.groupby("order_id")["payment_value"].sum().to_frame("total_paid")
comparison = items_total.join(payments_total,how="inner")
comparison["difference"] = comparison["total_paid"] - comparison["total_items"]
comparison.describe()
comparison["difference"].sum()
diff_ratio = comparison["difference"].sum() / comparison["total_paid"].sum()
diff_ratio
comparison["difference"].mean()
comparison.sort_values("difference",key=abs,ascending=False).head(10)

# merge orders with payments
df = payments.merge(orders,on="order_id")

# create month column
df["month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
monthly_revenue = df.groupby("month")["payment_value"].sum()
monthly_revenue_mean = df.groupby("month")["payment_value"].mean()
monthly_revenue_mediam = df.groupby("month")["payment_value"].median()
monthly_orders = df.groupby("month")["order_id"].nunique()
monthly_aov = monthly_revenue / monthly_orders

# monthly revenue chart
plt.Figure(figsize=(10,5))
monthly_revenue.plot(marker="o",linewidth=2)
plt.title("Monthly Revenue",fontsize=14)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

# number of orders per month chart
sns.set_style("whitegrid")
plt.Figure()
monthly_orders.plot()
plt.title("Number of Orders per Month")
plt.xlabel("Month")
plt.ylabel("Orders Count")
plt.xticks(rotation=45)
plt.show()

#monthly aov charts
sns.set_style("whitegrid")
plt.Figure()
monthly_aov.plot()
plt.title("Average Order value (AOV)")
plt.xlabel("Month")
plt.ylabel("AOV")
plt.xticks(rotation=45)
plt.show()

#distribution of payments(Histogram)
sns.set_style("whitegrid")
plt.Figure()
df["payment_value"].plot(kind="hist",bins=100)
plt.title("Payment Value Distribution")
plt.xlabel("Payment Value")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()

# top orders (outliers)
top_orders = df.groupby("order_id")["payment_value"].sum().sort_values(ascending=False).head()
top_orders
sns.set_style("whitegrid")
plt.Figure()
top_orders.plot(kind="bar")
plt.title("Top 10 Orders by Payment Value")
plt.xlabel("Order ID")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

# simple sales dashboard
sns.set_style("whitegrid")
fig,  axes  = plt.subplots(2,2,figsize=(12,8))
monthly_revenue.plot(ax=axes[0,0],marker="o")
axes[0,0].set_title("Monthly Revenue")

monthly_orders.plot(ax=axes[0,1],marker="o")
axes[0,1].set_title("Orders Count")

monthly_aov.plot(ax=axes[1,0],marker="o")
axes[1,0].set_title("Average Order Value")

df["payment_value"].plot(kind="hist",bins=40,ax=axes[1,1])
axes[1,1].set_title("Payment Distribution")

plt.tight_layout()
plt.show()

#correlation between (revenue , orders , aov)
monthly_df = pd.DataFrame({
  "revenue" : monthly_revenue,
  "orders" : monthly_orders,
  "aov"  : monthly_aov
})
monthly_df.corr()

#scatter plot
sns.scatterplot(data=monthly_df,x="orders",y="revenue")
plt.title("Revenue vs Orders")
plt.show()

#checking growth percantage 
monthly_df["revenue_growth"] = monthly_df["revenue"].pct_change()
monthly_df["orders_growth"] = monthly_df["orders"].pct_change()
monthly_df["revenue_growth"]
monthly_df["orders_growth"]

#final check for data problem
monthly_df.tail()

# #boxplot for outliers
plt.Figure(figsize=(8,5))
sns.boxenplot(x=df["payment_value"])
plt.title("Boxplot of Payment Value")
plt.show()

#checking outliers percantage
q1 = df["payment_value"].quantile(0.25)
q3 = df["payment_value"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
outliers = df[df["payment_value"] > upper_bound]
outlier_ratio = len(outliers) / len(df)
outlier_ratio

#outliers impact on business
outlier_impact = outliers["payment_value"].sum() / df["payment_value"].sum()
outlier_impact

#data analysis without outliers 
df_no_outliers = df[df["payment_value"] <= upper_bound]
df_no_outliers

monthly_revenue_clean = df_no_outliers.groupby("month")["payment_value"].sum()
monthly_orders_clean = df_no_outliers.groupby("month")["order_id"].nunique()
monthly_aov_clean = monthly_revenue_clean / monthly_orders_clean


fig , axes = plt.subplots(2,2,figsize=(12,8))
#monthly revenue chart
monthly_revenue_clean.plot(ax=axes[0,0],marker="o")
axes[0,0].set_title("monthly revenue (no outliers)")

#number of orders per month chart
monthly_orders_clean.plot(ax=axes[0,1],marker="o")
axes[0,1].set_title("monthly orders (no outliers)")

#monthly aov charts
monthly_aov_clean.plot(ax=axes[1,0],marker="o")
axes[1,0].set_title("monthly aov (no outliers)")

#distribution
df_no_outliers["payment_value"].plot(kind="hist", bins=40, ax=axes[1,1])
axes[1,1].set_title("monthly distribution (no outliers)")

plt.tight_layout()
plt.show()

#comparing between all data and data without ouliers
fig , axes = plt.subplots(2,2,figsize=(12,8))
#comp_revenue
monthly_revenue.plot(ax=axes[0,0],marker="o",label="All Date")
monthly_revenue_clean.plot(ax=axes[0,0],marker="o",label="No Outliers")
axes[0,0].set_title("Monthly Revenue Comparison")
axes[0,0].legend()

#comp_orders
monthly_orders.plot(ax=axes[0,1],marker="o",label="All Date")
monthly_orders_clean.plot(ax=axes[0,1],marker="o",label="No Outliers")
axes[0,1].set_title("Monthly Orders Comparison")
axes[0,1].legend()

#comp_aov
monthly_aov.plot(ax=axes[1,0],marker="o",label="All Date")
monthly_aov_clean.plot(ax=axes[1,0],marker="o",label="No Outliers")
axes[1,0].set_title("Monthly AOV Comparison")
axes[1,0].legend()

#comp_distribution
axes[1,1].hist(df["payment_value"],bins=40, alpha=0.5, label="All Data")
axes[1,1].hist(df_no_outliers["payment_value"],bins=40, alpha=0.5, label="No outliers")
axes[1,1].set_title("Distribution Comparison")
axes[1,1].legend()

plt.tight_layout()
plt.show()

#top customers analysis
customer_revenue = df.groupby("customer_id")["payment_value"].sum().sort_values(ascending=False)
top_customers = customer_revenue.head(10)
top_10_ratio = top_customers.sum() / customer_revenue.sum() 

#top products analysis
df_items = df.merge(order_items,on="order_id")
product_revenue = df_items.groupby("product_id")["payment_value"].sum().sort_values(ascending=False)
top_products = product_revenue.head(10)
ratio_products = top_products.sum() / product_revenue.sum() 

#pareto analysis (80/20 rule)
cumulative_customers = customer_revenue.cumsum() / customer_revenue.sum()
cumulative_products = product_revenue.cumsum() / product_revenue.sum()
cumulative_customers
cumulative_products

#pareto chart for products
cumulative_products.plot()
plt.axhline(0.8, color="red")
plt.title("Pareto curve - Products")
plt.show()

#comparing between the price and order_value in products
comp_products = df_items.groupby("product_id")[["price","payment_value"]].mean().sort_values(by="payment_value",ascending=False).head(10)
product_orders = df_items.groupby("product_id")["order_id"].nunique().sort_values(ascending=False)

# final product analysis
product_analysis = pd.DataFrame({
    "revenue" : product_revenue,
    "orders" : product_orders
})

product_analysis["avg_order_value"] = product_analysis["revenue"] / product_analysis["orders"]
product_analysis.sort_values("revenue",ascending=False).head(10)

#quik check for missing values
df_items_wipr = df_items.merge(products,on="product_id",how='left')
missing = df_items_wipr['product_category_name'].isna().mean()

# category analysis
category_analysis =df_items.merge(products,on="product_id",how='left')
mynan = category_analysis.dropna(subset=["product_category_name"])
mynan["product_category_name"].isna().sum()
df_items.groupby(category_analysis['product_category_name'])["payment_value"].sum().sort_values(ascending=False).head(10)

#customer analysis
customer_orders = df.groupby("customer_id")["order_id"].nunique()
customer_orders.describe()


