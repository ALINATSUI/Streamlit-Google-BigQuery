import streamlit as st, pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)
@st.cache_data(ttl=600)



def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

row1 = run_query("SELECT name,brand,retail_price,category FROM `bigquery-public-data.thelook_ecommerce.products` LIMIT 15")
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

''')




# f_1 = pd.read_csv("q1.csv")
# f1_df = pd.DataFrame(f_1)
# f1_df.rename(columns={
#     'retail_price': 'RETAIL_PRICE($)',
#     'name': 'PRODUCT NAME',
#     'brand': 'BRAND',
#     'category': 'CATEGORY',
    
# }, inplace=True)
st.dataframe(pd.DataFrame(row1), height='content')

# code = '''def run_query(query):
#     query_job = client.query(query)
#     rows_raw = query_job.result()
#     rows = [dict(row) for row in rows_raw]
#     return rows
# rows1 = run_query("SELECT name FROM `bigquery-public-data.thelook_ecommerce.products` LIMIT 15")    
# '''
# st.code(code, language="python")
st.divider(width='stretch')

# with st.expander(label='Question 2: Premium Products', width='stretch'):

#     st.write('''Finance wants a list of all products with a retail_price greater than $200. Show the product name, brand, and retail_price, sorted from most expensive to least expensive.''')
q2 = st.container(
    width='stretch', 
    height='content', 
    border=True,
    autoscroll=True,

    )
q2.header('Question 2: Premium Products')
q2.subheader(body = '''
         Finance wants a list of all products with a retail_price greater than $200. Show the product name, brand, and retail_price, sorted from most expensive to least expensive.''', anchor=False)
rows2 = run_query("SELECT name, brand, retail_price FROM `bigquery-public-data.thelook_ecommerce.products`")   

# f2 = pd.read_csv('q2.csv')
# f2_df = pd.DataFrame(f2)
# f2_df.rename(columns={
#     'retail_price' : 'RETAIL PRICE($)',
#     'name' : 'PRODUCT NAME', 
#     'brand' : 'BRAND'
# }, inplace=True)
st.dataframe(pd.DataFrame(rows2))
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
    "SELECT cost,retail_price, name, retail_price-cost AS profit_margin " \
"FROM `bigquery-public-data.thelook_ecommerce.products`" \
"ORDER BY profit_margin DESC" \
"")
# f3 = pd.read_csv('q3.csv')
# f3_df = pd.DataFrame(f3)
# f3_df.rename(columns={
#     'cost': 'COST($)',
#     'retail_price': 'RETAIL_PRICE($)',
#     'profit_margin': 'PROFIT_MARGIN($)',
#     'name': 'PRODUCT NAME'
# }, inplace=True)
st.dataframe(pd.DataFrame(row3))
st.divider(width='stretch')

q4 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q4.header('Question 4: Category Inventory Count')
q4.subheader(body='''How many products does TheLook carry in each category? Show the category name and the total count, sorted from largest category to smallest.
💡 Tip: Group your rows by category and count what falls inside each group.
''', anchor=False)

row4 = run_query("SELECT category, COUNT(*) AS CATEGORY_COUNT " \
"FROM `bigquery-public-data.thelook_ecommerce.products` " \
"GROUP BY category " \
"ORDER BY 2 DESC")
st.dataframe(pd.DataFrame(row4))
st.divider(width='stretch')

q5 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q5.header('Question 5: Department Split')
q5.subheader(body='''
            The buying team wants to know how the catalog is split by department. Show each department and the number of unique products in it.
💡 Tip: This is similar to Q4 but applied to the department column instead of category.
''', anchor=False)
row5 = run_query("SELECT department, COUNT(*) AS UNIQUE_PRODUCTS " \
"FROM `bigquery-public-data.thelook_ecommerce.products` " \
"GROUP BY department")
st.dataframe(pd.DataFrame(row5))
st.divider(width='stretch')

q6 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q6.header('Question 6: Women\'s Outerwear')
q6.subheader(body= '''
            Find all products in the 'Outerwear & Coats' category that belong to the 'Women' department. Show the product name, brand, and retail_price.
💡 Tip: You will need to filter on two columns at the same time and so both conditions must be true.
''', anchor=False)
row6 = run_query("SELECT category, department, name, brand, retail_price " \
"FROM `bigquery-public-data.thelook_ecommerce.products` " \
"WHERE category = 'Outerwear & Coats' AND department = 'Women'")
st.dataframe(pd.DataFrame(row6))
st.divider(width='stretch')

q7 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q7.header('Question 7: Average Price by Category')
q7.subheader(body='''
            What is the average retail_price for each category? Show the category and the average price, rounded to 2 decimal places, sorted from highest average to lowest.
💡 Tip: Use an aggregate function to find the mean, and look up ROUND() to clean up the decimal places.
''' )
row7 = run_query("SELECT category, ROUND(AVG(retail_price), 2) " \
"AS AVG_RETAIL_PRICE FROM `bigquery-public-data.thelook_ecommerce.products` " \
"GROUP BY category ORDER BY 2 DESC")
st.dataframe(pd.DataFrame(row7))
st.divider(width='stretch')


