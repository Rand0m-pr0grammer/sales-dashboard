
import pandas as pd
import plotly.express as px
import streamlit as st

# PAGE CONFIG

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Sales Dashboard")
st.markdown("---")


# LOAD DATA

@st.cache_data
def load_data():
    df = pd.read_excel(
        "supermarkt_sales.xlsx",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
        engine="openpyxl"
    )

    # Create hour column
    df["hour"] = pd.to_datetime(
        df["Time"],
        format="%H:%M:%S"
    ).dt.hour

    return df


df = load_data()


# SIDEBAR FILTERS

st.sidebar.header("Filter Data")

city = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select Customer Type",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)


# FILTER DATA

df_selection = df[
    df["City"].isin(city)
    & df["Customer_type"].isin(customer_type)
    & df["Gender"].isin(gender)
]


# HANDLE EMPTY DATA

if df_selection.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# KPI SECTION

total_sales = int(df_selection["Total"].sum())

average_rating = round(
    df_selection["Rating"].mean(),
    1
)

average_sales = round(
    df_selection["Total"].mean(),
    2
)

star_rating = "⭐" * round(average_rating)

left, middle, right = st.columns(3)

with left:
    st.subheader("Total Sales")
    st.subheader(f"MYR {total_sales:,}")

with middle:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")

with right:
    st.subheader("Average Transaction")
    st.subheader(f"MYR {average_sales}")

st.markdown("---")


# SALES BY PRODUCT LINE

sales_by_product = (
    df_selection
    .groupby("Product line")["Total"]
    .sum()
    .sort_values()
)

fig_product = px.bar(
    sales_by_product,
    x=sales_by_product.values,
    y=sales_by_product.index,
    orientation="h",
    title="Sales by Product Line",
    template="plotly_white"
)

fig_product.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Sales",
    yaxis_title=""
)


# SALES BY HOUR

sales_by_hour = (
    df_selection
    .groupby("hour")["Total"]
    .sum()
)

fig_hour = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y=sales_by_hour.values,
    title="Sales by Hour",
    template="plotly_white"
)

fig_hour.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)"
)


# DISPLAY BAR CHARTS

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )

with right_col:
    st.plotly_chart(
        fig_product,
        use_container_width=True
    )


# DONUT CHART

product_distribution = (
    df_selection
    .groupby("Product line")["Total"]
    .sum()
    .reset_index()
)

fig_donut = px.pie(
    product_distribution,
    values="Total",
    names="Product line",
    hole=0.5,
    title="Product Line Distribution"
)

st.plotly_chart(
    fig_donut,
    use_container_width=True
)


# DATA TABLE

st.markdown("### Filtered Data")

st.dataframe(
    df_selection,
    use_container_width=True
)


# HIDE STREAMLIT DEFAULTS

hide_style = """
<style>
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
</style>
"""

st.markdown(hide_style, unsafe_allow_html=True)
