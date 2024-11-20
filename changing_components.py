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

def add_submission_to_sheet(*updated_bins_dfs):
    # Step 1: Process the transposed question data
    def restructure_df(df, question_number):
        return (df.transpose()
                  .rename(columns=lambda col: f'Q{question_number + 1} {df.iloc[0, col]}')
                  .iloc[1:])

    # Process and transpose all DataFrames
    questions_df = pd.concat([restructure_df(df, i) for i, df in enumerate(updated_bins_dfs)], axis=1)

    # Step 2: Retrieve session state data as a DataFrame
    data = st.session_state['data']

    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'

    # Append user inputs to the session state data dictionary
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))

    session_state_df = pd.DataFrame(data)

    # Combine `session_state_df` with `questions_df`
    concatenated_df = pd.concat(
        [session_state_df, questions_df.set_index(session_state_df.index)],
        axis=1
    )

    # Step 3: Authenticate and open Google Sheet
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    client = gspread.authorize(creds)

    sheet = client.open("EEN_Survey_Data").sheet1

    # Step 4: Handle dynamic headers
    existing_headers = sheet.row_values(1)  # Retrieve headers from the first row
    if not existing_headers:
        existing_headers = []

    # Ensure all concatenated DataFrame columns have corresponding headers in the sheet
    for column_name in concatenated_df.columns:
        if column_name not in existing_headers:
            existing_headers.append(column_name)
            # Update the sheet header row
            sheet.update(f"A1:{gspread.utils.rowcol_to_a1(1, len(existing_headers))}", [existing_headers])

    # Step 5: Write data to corresponding columns
    existing_data = sheet.get_all_values()
    next_row = len(existing_data) + 1

    for column_name in concatenated_df.columns:
        if column_name in existing_headers:
            col_index = existing_headers.index(column_name) + 1
            value_to_write = concatenated_df.iloc[-1][column_name]
            cell_address = gspread.utils.rowcol_to_a1(next_row, col_index)
            sheet.update(cell_address, value_to_write)

    st.success("Data successfully added to the sheet!")
