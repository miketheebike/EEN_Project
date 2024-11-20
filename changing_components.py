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

def add_submission()
    # Update session state
    data = st.session_state['data']

    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'

    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))
    st.session_state['data'] = data
    for key, value in data.items():
        st.write(f"{key}: Length = {len(value)}")
    session_state_df = pd.DataFrame(data)
    
    personal_data_df = session_state_df.iloc[:, :5]
    min_eff_df = session_state_df.iloc[:, 5:]

    concatenated_df = pd.concat([personal_data_df, questions_df.set_index(personal_data_df.index), min_eff_df.set_index(personal_data_df.index)], axis=1)
      
    st.session_state['submit'] = True
    
    #save data to google sheet
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    client = gspread.authorize(creds)
 
    sheet = client.open("EEnergy_Efficiency_Survey_Data").sheet1

    column_names_list = concatenated_df.columns.tolist()
    #column_names = sheet.append_row(column_names_list)

    sheet_row_update = sheet.append_rows(concatenated_df.values.tolist()) #.values.tolist())
