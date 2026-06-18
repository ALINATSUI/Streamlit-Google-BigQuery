from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# Streamlit app URL from environment variable (or default)
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://bq--catalog.streamlit.app/")

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        wait = WebDriverWait(driver, 15)
        try:
            # Look for the wake-up button
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("Wake-up button found. Clicking...")
            button.click()

            # After clicking, check if it disappears
            try:
                wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
                print("Button clicked and disappeared ✅ (app should be waking up)")
            except TimeoutException:
                print("Button was clicked but did NOT disappear ❌ (possible failure)")
                exit(1)

        except TimeoutException:
            # No button at all → app is assumed to be awake
            print("No wake-up button found. Assuming app is already awake ✅")

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
    finally:
        driver.quit()
        print("Script finished.")

if __name__ == "__main__":
    main()



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

rows = run_query("SELECT name,brand,retail_price,category FROM `bigquery-public-data.thelook_ecommerce.products` LIMIT 15")
st.title('TLab: SQL Project')
st.write("Question 1: Catalog Snapshot")

f_1 = pd.read_csv("q1.csv")
f1_df = pd.DataFrame(f_1)
f1_df.rename(columns={
    'retail_price': 'RETAIL_PRICE($)',
    'name': 'PRODUCT NAME',
    'brand': 'BRAND',
    'category': 'CATEGORY',
    
}, inplace=True)
st.dataframe(f1_df, height='content')

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

f2 = pd.read_csv('q2.csv')
f2_df = pd.DataFrame(f2)
f2_df.rename(columns={
    'retail_price' : 'RETAIL PRICE($)',
    'name' : 'PRODUCT NAME', 
    'brand' : 'BRAND'
}, inplace=True)
st.dataframe(f2_df)
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
row3 = run_query("SELECT cost,retail_price, name, retail_price-cost AS profit_margin " \
"FROM `bigquery-public-data.thelook_ecommerce.products`ORDER BY profit_margin DESC")
f3 = pd.read_csv('q3.csv')
f3_df = pd.DataFrame(f3)
f3_df.rename(columns={
    'cost': 'COST($)',
    'retail_price': 'RETAIL_PRICE($)',
    'profit_margin': 'PROFIT_MARGIN($)',
    'name': 'PRODUCT NAME'
}, inplace=True)
st.dataframe(f3_df)
st.divider(width='stretch')

q4 = st.container(width='stretch', height='content', autoscroll=True, border=True)
q4.header('Question 4: Category Inventory Count')
q4.subheader(body='''How many products does TheLook carry in each category? Show the category name and the total count, sorted from largest category to smallest.
💡 Tip: Group your rows by category and count what falls inside each group.
''', anchor=False)


