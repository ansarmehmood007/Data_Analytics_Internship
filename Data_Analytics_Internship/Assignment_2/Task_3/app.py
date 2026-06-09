import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Business Dashboard", layout="wide")

st.title("📊 Interactive Business Dashboard")


# Load Dataset
df = pd.read_csv("superstore.csv")

# Correct the Columns datatypes
df["Order.Date"] = pd.to_datetime(df["Order.Date"])
df["Ship.Date"] = pd.to_datetime(df["Ship.Date"])


# Sidebar Filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub.Category"].unique(),
    default=df["Sub.Category"].unique()
)


# Apply Filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub.Category"].isin(sub_category))
]

# creat KPIs

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

col1, col2 = st.columns(2)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.2f}")

# Sales by Region

st.subheader("Sales by Region")

sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig1 = px.bar(sales_region, x="Region", y="Sales", color="Region")
st.plotly_chart(fig1, use_container_width=True)


# Profit by Category
st.subheader("Profit by Category")

profit_category = filtered_df.groupby("Category")["Profit"].sum().reset_index()

fig2 = px.bar(profit_category, x="Category", y="Profit", color="Category")
st.plotly_chart(fig2, use_container_width=True)


# find Top 5 Customers

st.subheader("Top 5 Customers by Sales")

top5 = (
    filtered_df.groupby("Customer.Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig3 = px.bar(top5, x="Customer.Name", y="Sales", color="Sales")
st.plotly_chart(fig3, use_container_width=True)

# Segment Performance

st.subheader("Segment-wise Performance")

segment = filtered_df.groupby("Segment")[["Sales", "Profit"]].sum().reset_index()

fig4 = px.bar(segment, x="Segment", y=["Sales", "Profit"], barmode="group")
st.plotly_chart(fig4, use_container_width=True)