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
    # Add custom CSS to disable horizontal scrolling
    # Add custom CSS to prevent horizontal scrolling and reduce vertical spacing on mobile
    st.markdown(
        """
        <style>
            /* Prevent horizontal scrolling */
            body {
                overflow-x: hidden;
            }
            
            /* Ensure the main content doesn't exceed screen width */
            .main, .block-container {
                max-width: 100vw;
                overflow-x: hidden;
            }
    
            /* Adjust spacing for mobile */
            @media only screen and (max-width: 768px) {
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                }
                .element-container {
                    margin-bottom: 0.5rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
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
            # 'User Years of Experience': [],
            # 'Working Hours': [],
            'Minimum Effect Size Q1': [],
            # 'Minimum Effect Size Q2': [],    
            # 'Minimum Effect Size Q3': [],
            # 'Minimum Effect Size Q4': [],
            # 'Minimum Effect Size Q5': [],
            # 'Minimum Effect Size Q6': [],
            # 'Minimum Effect Size Q7': [],
            # 'Minimum Effect Size Q8': [],
            # 'Cost-Benefit Ratio': [],
            # 'Risk Aversion': [],
        }
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]

def survey_title_subtitle(header_config):
    st.title(header_config['survey_title'])
    st.write(header_config['survey_description'])



def create_question(jsonfile_name):
    minor_value = str(jsonfile_name['minor_value'])
    min_value = jsonfile_name['min_value_graph']
    max_value = jsonfile_name['max_value_graph']
    interval = jsonfile_name['step_size_graph']
    major_value = str(jsonfile_name['major_value'])

    # Create a list of ranges based on the provided values
    x_axis = [minor_value] + [f"{round(i, 1)}% to {round((i + interval - 0.01), 2)}%" for i in np.arange(min_value, max_value, interval)] + [major_value]

    # TODO: find a way to remove it
    if jsonfile_name['min_value_graph'] == -1:
        x_axis.insert(6, "0%")
        x_axis[1] = '-0.99% to -0.81%'
        x_axis[7] = '0.01% to 0.19%'
    elif jsonfile_name['min_value_graph'] == -10:
        x_axis.insert(3, "0%")
        x_axis[5] = '0.01% to 4.99%'
    elif jsonfile_name['min_value_graph'] == 0:    
        x_axis[1] = '0.01% to 4.99%'

    y_axis = np.zeros(len(x_axis))

    # Create dataframe for bins and their values
    data = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[jsonfile_name['column_1'], jsonfile_name['column_2']])
            

    # Display title and subtitle for the question
    st.subheader(jsonfile_name['title_question'])
    st.write(jsonfile_name['subtitle_question'])

    # Create a container for the data editor and other elements
    data_container = st.container()

    # Integrate the updated logic for displaying data editor and handling percentages
    with data_container:
        # Create table and plot layout
        table, plot = st.columns([0.4, 0.6], gap="large")

        with table:
            # Calculate the height based on the number of rows
            row_height = 35  # Adjust as necessary based on row size
            table_height = ((len(data)+1) * row_height) 
            # Display the data editor
            bins_grid = st.data_editor(data, 
                                       key=jsonfile_name['key'], 
                                       hide_index=True, 
                                       use_container_width=True, 
                                       disabled=[jsonfile_name['column_1']],
                                       height = table_height)

            # Calculate the remaining percentage to be allocated
            percentage_difference = round(100 - sum(bins_grid[jsonfile_name['column_2']]))

            # Helper function to display status message
            def display_message(message, color):
                styled_message = f'<b style="font-family:sans-serif; color:{color}; font-size: 20px; padding: 10px;">{message}</b>'
                st.markdown(styled_message, unsafe_allow_html=True)

            # Display appropriate message based on the percentage difference
            if percentage_difference > 0:
                display_message(f'You still have to allocate {percentage_difference}% probability.', 'Red')
            elif percentage_difference == 0:
                display_message('You have allocated all probabilities!', 'Green')
            else:
                display_message(f'You have inserted {abs(percentage_difference)}% more, please review your percentage distribution.', 'Red')

                        
    # with data_container:
    #     table, plot = st.columns([0.4, 0.6], gap="large")
    #     with table:
    #         bins_grid = st.data_editor(data, key= jsonfile_name['key'], hide_index=True, use_container_width=True, disabled=[jsonfile_name['column_1']])
    #         percentage_difference = 100 - sum(bins_grid[jsonfile_name['column_2']])

    #         # Display the counter
    #         if percentage_difference > 0:
    #             missing_prob = f'<b style="font-family:sans-serif; color:Red; font-size: 20px; ">You still have to allocate {percentage_difference}% probability.</b>'
    #             st.markdown(missing_prob, unsafe_allow_html=True)
                
    #         elif percentage_difference == 0:
    #             total_prob = f'<b style="font-family:sans-serif; color:Green; font-size: 20px; ">You have allocated all probabilities!</b>'
    #             st.markdown(total_prob, unsafe_allow_html=True)
    #         else:
    #             exceeding_prob = f'<b style="font-family:sans-serif; color:Red; font-size: 20px; ">You have inserted {abs(percentage_difference)}% more, please review your percentage distribution.</b>'
    #             st.markdown(exceeding_prob, unsafe_allow_html=True)
                      
        with plot:
            # Extract the updated values from the second column
            updated_values = bins_grid[jsonfile_name['column_2']]

            # Get rid of plot menu
            config = {'displayModeBar': False, "staticPlot": True }
                    
            # Plot the updated values as a bar plot
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=bins_grid[jsonfile_name['column_1']], 
                y=updated_values, 
                marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
                marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
                marker_line_width=2,  # Width of the bar outline
                text=[f"{p}" for p in bins_grid[jsonfile_name['column_2']]],  # Adding percentage labels to bars
                textposition='auto',
                name='Probability'
            ))

            fig.update_layout(
                title={
                    'text': "Probability distribution",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title="Expectation Range",
                yaxis_title="Probability (%)",
                yaxis=dict(
                    range=[0, 100], 
                    gridcolor='rgba(255, 255, 255, 0.2)',  # Light grid on dark background
                    showline=True,
                    linewidth=2,
                    linecolor='white',
                    mirror=True
                ),
                xaxis=dict(
                    tickangle=-45,
                    showline=True,
                    linewidth=2,
                    linecolor='white',
                    mirror=True
                ),
                font=dict(color='white'),  # White font color for readability
            width = 350,
            height = 400
            )
            st.plotly_chart(fig, config = config ,use_container_width=True)
            updated_bins_list1 = [pd.DataFrame(bins_grid)] 
            
            def restructure_df1(df, i):
                transposed_df1 = df.transpose()
                transposed_df1.columns =  [f'Q{i + 1}  {col}' for col in list(transposed_df1.iloc[0])]
                transposed_df1 = transposed_df1.iloc[1:]
                return transposed_df1
        
            transposed_bins_list1 = []
            for i, df in enumerate(updated_bins_list1):
                transposed_bins_list1.append(restructure_df1(df, i))
        
            # Concatenating transposed dataframes
            questions_df1 = pd.concat(transposed_bins_list1, axis=1)
        
            # Resetting index if needed
            questions_df1.reset_index(drop=True, inplace=True)
            # data = st.session_state['data']
            st.dataframe(questions_df1)
            test = pd.DataFrame(st.session_state['data'])
            st.dataframe(test)
            # st.write(data)
            st.dataframe(pd.concat([test, questions_df1.set_index(test.index)], axis=1))
    return pd.DataFrame(bins_grid), percentage_difference, len(bins_grid)
    
def effect_size_question(jsonfile_name):
    col1, _ = st.columns(2)
    with col1:
        st.markdown(jsonfile_name['effect_size'])
        st.text_input("Please insert a number or skip if you are unsure.", key = jsonfile_name['num_input_question'])



def add_submission(updated_bins_question_1_df ):
#updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df, updated_bins_question_8_df
    updated_bins_list = [updated_bins_question_1_df]#, updated_bins_question_2_df]
#updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df, updated_bins_question_8_df
    def restructure_df(df, i):
        transposed_df = df.transpose()
        transposed_df.columns =  [f'Q{i + 1}  {col}' for col in list(transposed_df.iloc[0])]
        transposed_df = transposed_df.iloc[1:]
        return transposed_df

    transposed_bins_list = []
    for i, df in enumerate(updated_bins_list):
        transposed_bins_list.append(restructure_df(df, i))

    # Concatenating transposed dataframes
    questions_df = pd.concat(transposed_bins_list, axis=1)

    # Resetting index if needed
    questions_df.reset_index(drop=True, inplace=True)
    # Step 2: Retrieve session state data as a DataFrame
    data = st.session_state['data']

    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'
    #YEARS_OF_EXPERIENCE = 'User Years of Experience'
    #WORKING_HOURS = 'Working Hours'
    MIN_EFF_SIZE_Q1 = 'Minimum Effect Size Q1'
    #MIN_EFF_SIZE_Q2 = 'Minimum Effect Size Q2'
    # MIN_EFF_SIZE_Q3 = 'Minimum Effect Size Q3'
    # MIN_EFF_SIZE_Q4 = 'Minimum Effect Size Q4'
    # MIN_EFF_SIZE_Q5 = 'Minimum Effect Size Q5'
    # MIN_EFF_SIZE_Q6 = 'Minimum Effect Size Q6'
    # MIN_EFF_SIZE_Q7 = 'Minimum Effect Size Q7'
    # MIN_EFF_SIZE_Q8 = 'Minimum Effect Size Q8'
    # COST_BENEFIT_RATIO = 'Cost-Benefit Ratio'
    # RISK_AVERSION = 'Risk Aversion'
    # Append user inputs to the session state data dictionary
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))
    #data[YEARS_OF_EXPERIENCE].append(safe_var('years_of_experience'))
    #data[WORKING_HOURS].append(safe_var('working_hours'))
    data[MIN_EFF_SIZE_Q1].append(safe_var('num_input_question1'))
    #data[MIN_EFF_SIZE_Q2].append(safe_var('num_input_question2'))
    # data[MIN_EFF_SIZE_Q3].append(safe_var('num_input_question3'))
    # data[MIN_EFF_SIZE_Q4].append(safe_var('num_input_question4'))
    # data[MIN_EFF_SIZE_Q5].append(safe_var('num_input_question5'))
    # data[MIN_EFF_SIZE_Q6].append(safe_var('num_input_question6'))
    # data[MIN_EFF_SIZE_Q7].append(safe_var('num_input_question7'))
    # data[MIN_EFF_SIZE_Q8].append(safe_var('num_input_question8'))
    # data[COST_BENEFIT_RATIO].append(safe_var('cost_benefit'))
    # data[RISK_AVERSION].append(safe_var('risk_aversion'))
    
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
