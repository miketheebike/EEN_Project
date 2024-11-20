import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io
import numpy as np
import requests
#from requests_oauthlib import OAuth2Session
import csv
import altair as alt
import plotly.graph_objs as go
from streamlit_sortables import sort_items

def secrets_to_json():
    return {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"],
        
    }
def personal_information():
    st.subheader(SECTION_ONE)
    col1, _ = st.columns(2)
    with col1:
        st.text_input("Please, enter your full name:", key = 'user_full_name')
        st.text_input("Please, enter your working title:", key = 'user_position')
        st.selectbox('Please, specify your professional category:', ('Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor', 'Entrepreneur/Firm Representative'), key="professional_category")
        
def submit(): 
    st.session_state['submit'] = True
