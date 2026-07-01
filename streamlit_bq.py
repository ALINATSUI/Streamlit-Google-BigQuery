import streamlit as st, pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(credentials=credentials)
# st.set_page_config(layout="wide")

def run_query(query: str):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

row1 = run_query("SELECT name,brand,ROUND((retail_price), 2) retail_price,category FROM `bigquery-public-data.thelook_ecommerce.products` LIMIT 15")
st.title('TLab: SQL Project')
q1 = st.container(
    width='stretch', 
    height='content', 
    border=True,
    autoscroll=True,

    )
q1.header("Question 1: Catalog Snapshot")
q1.subheader(body = '''
             The merchandising team wants a quick preview of what is in the product catalog. Show the name, brand, category, and retail_price for the first 15 products.
💡 Tip: Think about how to limit the number of rows returned rather than pulling the entire table.

''', anchor=False)

row1_df = pd.DataFrame(row1)
row1_df.rename(columns={
    'retail_price': 'RETAIL_PRICE($)',
    'name': 'PRODUCT NAME',
    'brand': 'BRAND',
    'category': 'CATEGORY'
    
}, inplace=True)
# row1_AgGrid_return = AgGrid(row1_df)

st.dataframe(row1_df)
st.divider(width='stretch')


q2 = st.container(
    width='stretch', 
    height='content', 
    border=True,
    autoscroll=True,

    )
q2.header('Question 2: Premium Products')
q2.subheader(body = '''
         Finance wants a list of all products with a retail_price greater than $200. Show the product name, brand, and retail_price, sorted from most expensive to least expensive.''', anchor=False)

rows2 = run_query(""" SELECT ROUND((retail_price), 2) retail_price, name, brand FROM `bigquery-public-data.thelook_ecommerce.products` WHERE retail_price > 200 ORDER BY retail_price DESC """)   


rows2_df = pd.DataFrame(rows2)
rows2_df.rename(columns={
    'retail_price' : 'RETAIL PRICE($) - DESC',
 'name' : 'PRODUCT NAME', 
'brand' : 'BRAND'
}, inplace=True)

st.dataframe(rows2_df)
st.divider()

q3 = st.container(
    width='stretch', 
    height='content', 
    autoscroll=True, 
    border=True, 
    )
q3.header('Question 3: Profit Margin Calculation')
q3.subheader(body='''
Calculate the gross profit margin for each product. Gross profit margin is defined as the difference between retail_price and cost. Name this new column profit_margin. Show the product name, retail_price, cost, and profit_margin, sorted by highest margin first.
💡 Tip: You can subtract one column from another directly inside SELECT, then give the result a clean name using AS.
''', anchor=False)

row3 = run_query(
    '''SELECT ROUND((cost), 2) cost, retail_price, name, ROUND((retail_price - cost),2) AS profit_margin FROM `bigquery-public-data.thelook_ecommerce.products` ORDER BY profit_margin DESC ''')

rows3_df = pd.DataFrame(row3)
rows3_df.rename(columns={
    'cost': 'COST($)',
    'retail_price': 'RETAIL_PRICE($)',
    'profit_margin': 'PROFIT_MARGIN($) - DESC',
    'name': 'PRODUCT NAME'
}, inplace=True)
# rows3_AgGrid_return = AgGrid(rows3_df)
st.dataframe(rows3_df, width='stretch')
st.divider(width='stretch')

q4 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q4.header('Question 4: Category Inventory Count')
q4.subheader(body='''How many products does TheLook carry in each category? Show the category name and the total count, sorted from largest category to smallest.
💡 Tip: Group your rows by category and count what falls inside each group.
''', anchor=False)

row4 = run_query("""SELECT category, COUNT(*) AS CATEGORY_COUNT 
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY category 
ORDER BY 2 DESC""")
row4_df = pd.DataFrame(row4)
row4_df.rename(columns={
    'category': 'CATEGORY'
})
row4_AgGrid_return = AgGrid(row4_df)
# st.dataframe(row4_df)
st.divider(width='stretch')

q5 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q5.header('Question 5: Department Split')
q5.subheader(body='''
            The buying team wants to know how the catalog is split by department. Show each department and the number of unique products in it.
💡 Tip: This is similar to Q4 but applied to the department column instead of category.
''', anchor=False)
row5 = run_query("""SELECT department, COUNT(*) AS UNIQUE_PRODUCTS 
FROM `bigquery-public-data.thelook_ecommerce.products` 
GROUP BY department""")
row5_df = pd.DataFrame(row5)
row5_df.rename(columns={
    'department': 'DEPT',
    'UNIQUE_PRODUCTS': 'UNIQUE_PROD_COUNT'
})
row5_AgGrid_return = AgGrid(row5_df)
# st.dataframe(pd.DataFrame(row5))
st.divider(width='stretch')

q6 = st.container(width='content', height='content', autoscroll=True, border=True)
q6.header('Question 6: Women\'s Outerwear')
q6.subheader(body= '''
            Find all products in the 'Outerwear & Coats' category that belong to the 'Women' department. Show the product name, brand, and retail_price.
💡 Tip: You will need to filter on two columns at the same time and so both conditions must be true.
''', anchor=False)

# q6 = st.write(""" Question 6 : Find all products in the 'Outerwear & Coats' category that belong to the 'Women' department. Show the product name, brand, and retail_price.
# 💡 Tip: You will need to filter on two columns at the same time and so both conditions must be true.""")
row6 = run_query("""SELECT category, department, name, brand, ROUND((retail_price), 2) retail_price
FROM `bigquery-public-data.thelook_ecommerce.products` 
WHERE category = 'Outerwear & Coats' AND department = 'Women'""")

row6_df = pd.DataFrame(row6)
row6_df.rename(columns={
    'category': 'CATEGORY',
    'department': 'DEPT', 
    'name': 'ITEM NAME', 
    'brand': 'BRAND',
    'retail_price': 'RETAIL_PRICE ($)'
}, inplace=True)
# row6_AgGrid_return = AgGrid(row6_df)
st.dataframe(row6_df)

st.divider(width='stretch')

q7 = st.container(width='stretch', height='content', autoscroll=False, border=True)
q7.header('Question 7: Average Price by Category')
q7.subheader(body='''
            What is the average retail_price for each category? Show the category and the average price, rounded to 2 decimal places, sorted from highest average to lowest.
💡 Tip: Use an aggregate function to find the mean, and look up ROUND() to clean up the decimal places.
''', anchor=False)
row7 = run_query("""SELECT category, ROUND(AVG(retail_price), 2) 
AS AVG_RETAIL_PRICE FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY category ORDER BY 2 DESC""")
row7_df = pd.DataFrame(row7)
row7_df.rename(columns={
    'category': 'CATEGORY',
    'AVG_RETAIL_PRICE': 'RETAIL PRICE AVG ($) - DESC',

}, inplace=True)
row7_AgGrid_return = AgGrid(row7_df)
# st.dataframe(pd.DataFrame(row7_df))
st.divider(width='stretch')

q8 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q8.header('Question 8: Price Tier Classification')
q8.subheader(body='''
            Create a new column called price_tier that Tlabels each product as follows: retail_price under $50 is 'Budget', between $50 and $150 is 'Mid-Range', and above $150 is 'Premium'. Show the product name, retail_price, and price_tier.
💡 Tip: Use a multi-branch logic statement, one branch for each price range.
''', anchor=False)
row8 = run_query("""SELECT name,ROUND((retail_price), 2) retail_price,
CASE 
  WHEN retail_price < 50 THEN "Budget"
  WHEN retail_price =50 OR retail_price <=150 THEN "Mid-Range"
  WHEN retail_price > 150 THEN "Premium"
END AS price_tier
FROM `bigquery-public-data.thelook_ecommerce.products`""")

row8_df = pd.DataFrame(row8)
row8_AgGrid_return = AgGrid(row8_df)
# st.dataframe(row8_df)
st.divider(width='stretch')

q9 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q9.header('Question 9: Missing Data Audit')
q9.subheader(body='''
             The data team suspects some products might be missing a brand value. Write a query to identify any products where brand is NULL. Show the product name, category, and retail_price for those products.
💡 Tip: There is a specific SQL keyword for checking whether a value is completely absent.
''', anchor=False)
row9 = run_query("""
            SELECT name, category, ROUND((retail_price), 2) RETAIL_PRICE, brand
FROM `bigquery-public-data.thelook_ecommerce.products`
WHERE brand IS NULL
""")

row9_df = pd.DataFrame(row9)
st.dataframe(row9_df)
# row9_AgGrid_return = AgGrid(row9_df)
st.divider(width='stretch')


q10 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q10.header('Question 10: High-Value Categories')
q10.subheader(body='''
             Which product categories have an average retail_price above $80? Only include categories that have more than 10 products. Show the category, average price (rounded to 2 decimal places), and product count.
💡 Tip: After grouping and aggregating your data, you will need to apply a filter to the grouped results, not to the original rows.
''')
row10 = run_query('''
                  SELECT category, COUNT(*) AS category_count 
FROM `bigquery-public-data.thelook_ecommerce.products`
GROUP BY category
HAVING category_count > 10
ORDER BY category_count DESC''')
row_10_df = pd.DataFrame(row10)
row_10_AgGrid_return = AgGrid(row_10_df)











