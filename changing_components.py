import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import io
import numpy as np
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from requests_oauthlib import OAuth2Session
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from fixed_components import *
import plotly.graph_objs as go

def initialize_session_state():

    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
           
    if 'data' not in st.session_state:
        st.session_state['data'] = {
            'User Full Name': [],
            'User Working Position': [],
            'User Professional Category': [],
        }
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]

def add_submission():
    # Update session state
    data = st.session_state['data']

    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'

    # Append user inputs to the session state data dictionary
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))

    # Convert the data to a DataFrame
    session_state_df = pd.DataFrame(data)

    # Authenticate with Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    client = gspread.authorize(creds)

    # Open the target sheet
    sheet = client.open("EEN_Survey_Data").sheet1

    # Retrieve headers from the first row of the sheet
    existing_headers = sheet.row_values(1)  # Get the header row (1-based index)

    # Create missing headers
    if not existing_headers:
        existing_headers = []

    # Ensure all DataFrame columns have corresponding headers in the sheet
    for column_name in session_state_df.columns:
        if column_name not in existing_headers:
            # Add the missing header at the end of the existing headers
            existing_headers.append(column_name)
            # Update the sheet header row
            sheet.update(f"A1:{gspread.utils.rowcol_to_a1(1, len(existing_headers))}", [existing_headers])

    # Get the next empty row
    existing_data = sheet.get_all_values()
    next_row = len(existing_data) + 1

    # Write data to corresponding columns
    for column_name in session_state_df.columns:
        if column_name in existing_headers:
            # Find the column index (1-based) for the header
            col_index = existing_headers.index(column_name) + 1
            # Get the value from the last row of the DataFrame
            value_to_write = session_state_df.iloc[-1][column_name]
            # Update the specific cell
            cell_address = gspread.utils.rowcol_to_a1(next_row, col_index)
            sheet.update(cell_address, value_to_write)

    st.success("Data successfully added to the sheet!")
