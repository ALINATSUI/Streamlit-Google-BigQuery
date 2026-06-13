Using a public dataset available on Google Cloud BigQuery, I used SQL queries to answer 3 business questions:
1. What are the names, brands and category of product catalog?
2. What are product name, brand and retail  price (sorted from most expensive to least)?
3. Profit margin calculation of each product

To make this project more interesting and technically challenging(!), I've connected Google BigQuery library to Streamlit (Python library used for creating interactive 
data web apps. 

Some challenges with this project were:
1.  While I did have a personal email account for Google Cloud, I discovered that I could not make use of organizational features such as creating private keys which I needed to authenticate.
    As I had a private domain, I added in TXT/CNAME records for domain verification purposes that allowed me to create a free account for Google Cloud Identity. Cloud Identity acts as
   the centralized directory from a single platform.

2.  Tweaking the necessary Identity and Access Management roles needed to run query jobs which weren't specified on the documentation, so this took some debugging and
   troubleshooting. Initially, I created a Data Viewer service account with view access only. Once the BigQuery job user role was added, the service account was then able to run query jobs. 
3. For some reason, the initial installation of Google auth modules weren't successfully installed the first time, which resulted in "No module found."

The second part of this project involved coding out Python, pandas on Streamlit platform. This was a great learning experience that challenged me which I found to be rewarding. 
