import streamlit as st
import pandas as pd
import pandas_gbq
import pandas 
import os
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime, timedelta
from scipy.stats import chi2_contingency
from PIL import Image
from git import Repo
import base64
import requests
import json
from google.cloud import storage

credentials = service_account.Credentials.from_service_account_info(
          st.secrets["gcp_service_account"]
      )
client = bigquery.Client(credentials=credentials)

#### Information to be changed when switching accounts ###
Account = "Sunpower"
bucket_name = "creativetesting_images"
main_table_id = 'sunpower-375201.sunpower_segments.sunpower_platform_ad_level'
creativetesting_table_id = 'sunpower-375201.sunpower_streamlit.CreativeTestingStorage'
correct_hashed_password = "Sunpower1234"


st.set_page_config(page_title= f"{Account} Creative Ad Testing Dash",page_icon="🧑‍🚀",layout="wide")

def initialize_storage_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    storage_client = storage.Client(credentials=credentials)
    return storage_client

# Use this client for GCS operations
storage_client = initialize_storage_client()


def password_protection():
  if 'authenticated' not in st.session_state:
      st.session_state.authenticated = False
      
  if not st.session_state.authenticated:
      password = st.text_input("Enter Password:", type="password")
      
      if st.button("Login"):
          if password == correct_hashed_password:
              st.session_state.authenticated = True
              main_dashboard()
          else:
              st.error("Incorrect Password. Please try again or contact the administrator.")
  else:
      main_dashboard()

  def main_dashboard():
    st.markdown(f"<h1 style='text-align: center;'>{Account} Creative Ad Testing</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Current Test</h2>", unsafe_allow_html=True)
    # Calculate the date one year ago from today
    one_year_ago = (datetime.now() - timedelta(days=365)).date()
  
    if 'full_data' not in st.session_state:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = bigquery.Client(credentials=credentials)
        # Modify the query
        query = f"""
        SELECT * FROM `{main_table_id}` 
        WHERE Date BETWEEN '{one_year_ago}' AND CURRENT_DATE() """
      
        st.session_state.full_data = pandas.read_gbq(query, credentials=credentials)

    data = st.session_state.full_data
    st.write(data)
