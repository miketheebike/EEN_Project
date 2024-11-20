#import streamlit as st
import json
from fixed_components import *
from changing_components import *
import numpy as np

st.set_page_config(layout="wide")

# Read the JSON file
config = json.load(open('config.json'))

initialize_session_state()
personal_information()
submit = st.button("Submit", on_click = add_submission)

if st.session_state['submit']:
    st.success(f"Thank you for completing the Survey on {config['header']['survey_title']}!")
