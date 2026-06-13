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

rows = run_query("SELECT name FROM `bigquery-public-data.thelook_ecommerce.products` LIMIT 15")

st.write("Question 1: Catalog Snapshot")
# for row in rows:
    # st.write(row['name'] + row['brand'] + row['category'] + row['retail_price'])
    # st.write(row['name'])
# col1, col2, col3, col4 = st.columns(4)
# for row in rows:
#         # st.write(row['name'])
#         st.write(row['brand'])
f = pd.read_csv("query1.csv")
query1_df = pd.DataFrame(f)
st.dataframe(query1_df)

