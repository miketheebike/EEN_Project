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
        YEARS_AS_ADVISOR = 'Years as Advisor'
        JOIN_DATE_EEN = 'Join Date EEN'
        EXPERT_OR_GENERALIST = 'Expert or Generalist'
        WORK_DEDICATION = 'Work Dedication'
        FIRMS_CONSULTED_PW = 'Firms Consulted Per Week'
        AVG_WORKING_HOURS_PER_CLIENT = 'Average Working Hours Per Client'
        NUM_FIRMS_ADVISED = 'Number of Firms Advised on Sustainability'
        PERSONAL_HOURLY_FEE = 'Personal Hourly Fee'
        FIRM_FEE_DIFFERENT = 'Is Firm Fee Different'
        FIRM_HOURLY_FEE = 'Firm Hourly Fee'
        MEETING_FREQUENCY_ADVISORS = 'Meeting Frequency with Firms'
        MEETING_DURATION_ADVISORS = 'Typical Meeting Duration'
        FIRM_HOURS_PER_WEEK = 'Firm Consulting Hours per Week'
        PERSONAL_HOURS_PER_WEEK = 'Personal Consulting Hours per Week'
        EXPECTED_REDUCTION = 'Expected Number of Firms Achieving Energy Reduction'
        MEASURES_EFFECTIVENESS_MOST = 'Most Effective Actions or Solutions'
        MEASURES_EFFECTIVENESS_LEAST = 'Least Effective Actions or Solutions'
        RANKED_TOPICS_BY_TIME_COVERED = 'Ranked Topics by Time Covered'
        ADVICE_FOLLOWED_BY_FIRMS = 'Advice Firms Chose to Follow'
        REASONS_FOR_FIRMS_FOLLOWING = 'Reasons Firms Followed Advice'
        REASONS_FOR_FIRMS_FOLLOWING_OTHER = 'Reasons Firms Followed Advice - Other'
        ADVICE_NOT_FOLLOWED_BY_FIRMS = 'Advice Firms Did Not Follow'
        REASONS_FIRMS_NOT_FOLLOWING = 'Reasons Firms Did Not Follow Advice'
        REASONS_FIRMS_NOT_FOLLOWING_OTHER = 'Reasons Firms Not Following Advice - Other'
        PERSONNEL_TRAINING_AGREEMENT = 'Agreement on Personnel Training'
        IMPORTANT_INVESTMENT_CRITERION = 'Important Investment Criterion'
        INVESTMENT_CRITERION_OTHER = 'Other Important Investment Criterion'
        TECHNOLOGY_EFFECTIVENESS_DATA = 'Technology Effectiveness Data'
        TYPICAL_MONTHLY_ENERGY_EXPENDITURE = 'Typical Monthly Energy Expenditure'
        st.session_state['data'] = {
            'User Full Name': [],
            'User Working Position': [],
            'User Professional Category': [],



            
            'Years as Advisor': [],
            'Join Date EEN': [],
            'Expert or Generalist': [],
            'Work Dedication': [],
            'Firms Consulted Per Week': [],
            'Average Working Hours Per Client': [],
            'Number of Firms Advised on Sustainability': [],
            PERSONAL_HOURLY_FEE: [],
            FIRM_FEE_DIFFERENT: [],  
            FIRM_HOURLY_FEE: [],
            MEETING_FREQUENCY_ADVISORS: [],
            MEETING_DURATION_ADVISORS: [],
            FIRM_HOURS_PER_WEEK: [],
            PERSONAL_HOURS_PER_WEEK: [],
            EXPECTED_REDUCTION: [],
            MEASURES_EFFECTIVENESS_MOST: [],
            MEASURES_EFFECTIVENESS_LEAST: [],
            
            RANKED_TOPICS_BY_TIME_COVERED: [],
            ADVICE_FOLLOWED_BY_FIRMS: [],
            REASONS_FOR_FIRMS_FOLLOWING: [],
            REASONS_FOR_FIRMS_FOLLOWING_OTHER: [],
            ADVICE_NOT_FOLLOWED_BY_FIRMS: [],
            REASONS_FIRMS_NOT_FOLLOWING: [],
            REASONS_FIRMS_NOT_FOLLOWING_OTHER: [],
            PERSONNEL_TRAINING_AGREEMENT: [],
            IMPORTANT_INVESTMENT_CRITERION: [],
            INVESTMENT_CRITERION_OTHER: [],
            TECHNOLOGY_EFFECTIVENESS_DATA: [],
            TYPICAL_MONTHLY_ENERGY_EXPENDITURE: [],
            # 'Meeting Frequency': [],
            # 'Meeting Duration': [],
            # 'Topics Discussed': [],
            # 'Time Covered Rankings': [],
            # #'Meeting Effectiveness': [],
            # 'Advice Followed by Firms': [],
            # 'Reasons Firms Followed Advice': [],
            # 'Advice Not Followed by Firms': [],
            # 'Reasons Firms Did Not Follow Advice': [],
            # 'Expected Reduction in Energy Use': [],
            # 'Most Effective Measures': [],
            # 'Least Effective Measures': [],
            # 'Personal Hourly Fee': [],
            # 'Firm Hourly Fee': [],
            # 'Firm Hours Per Week': [],
            # 'Personal Hours Per Week': [],
            # 'Reasons for Following Advice': [],
            # 'Meeting Effectiveness': [],
            #'Technologies Table': [],
            #'Ranked Topics': []



            
            'Minimum Effect Size Q1': [],
            'Minimum Effect Size Q2': [],    
            'Minimum Effect Size Q3': [],
            'Minimum Effect Size Q4': [],
            'Minimum Effect Size Q5': [],
            'Minimum Effect Size Q6': [],
            'Minimum Effect Size Q7': [],
            'Minimum Effect Size Q8': [],
            'Cost-Benefit Ratio': [],
            'Risk Aversion': [],
        }
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]

def survey_title_subtitle(header_config):
    st.title(header_config['survey_title'])
    st.write(header_config['survey_description'])
    
def create_question(jsonfile_name):
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    import streamlit as st

    minor_value = str(jsonfile_name['minor_value'])
    min_value = jsonfile_name['min_value_graph']
    max_value = jsonfile_name['max_value_graph']
    interval = jsonfile_name['step_size_graph']
    major_value = str(jsonfile_name['major_value'])

    # Create a list of ranges based on the provided values
    x_axis = [minor_value] + [f"{round(i, 1)}% to {round((i + interval - 0.01), 2)}%" for i in np.arange(min_value, max_value, interval)] + [major_value]

    # Handle special cases based on min_value_graph
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
            bins_grid = st.data_editor(
                data, 
                key=jsonfile_name['key'], 
                hide_index=True, 
                use_container_width=True, 
                disabled=[jsonfile_name['column_1']],
                height=table_height
            )

            # Replace None or NaN values in the probabilities column with zero
            bins_grid[jsonfile_name['column_2']] = bins_grid[jsonfile_name['column_2']].fillna(0)

            # Ensure the probabilities column is numeric
            bins_grid[jsonfile_name['column_2']] = pd.to_numeric(bins_grid[jsonfile_name['column_2']], errors='coerce').fillna(0)

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

            # Optional: Add a reset button with a unique key
            if st.button('Reset values to zero', key=f"reset_button_{jsonfile_name['key']}"):
                # Reset the probabilities column to zero
                bins_grid[jsonfile_name['column_2']] = 0
                # Update the session state for the data editor
                st.session_state[jsonfile_name['key']][jsonfile_name['column_2']] = 0
                # Re-run the script to refresh the UI
                st.experimental_rerun()

        with plot:
            # Extract the updated values from the second column
            updated_values = bins_grid[jsonfile_name['column_2']]

            # Plot configuration to hide the menu and make the plot static
            config = {'displayModeBar': False, "staticPlot": True }
                    
            # Plot the updated values as a bar plot
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=bins_grid[jsonfile_name['column_1']], 
                y=updated_values, 
                marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
                marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
                marker_line_width=2,  # Width of the bar outline
                text=[f"{p}" for p in updated_values],  # Adding percentage labels to bars
                textposition='auto',
                name='Probability'
            ))

            fig.update_layout(
                title={
                    'text': "Probability Distribution",
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
                width=350,
                height=400
            )
            st.plotly_chart(fig, config=config, use_container_width=True)

    return pd.DataFrame(bins_grid), percentage_difference, len(bins_grid)


# def create_question(jsonfile_name):
#     minor_value = str(jsonfile_name['minor_value'])
#     min_value = jsonfile_name['min_value_graph']
#     max_value = jsonfile_name['max_value_graph']
#     interval = jsonfile_name['step_size_graph']
#     major_value = str(jsonfile_name['major_value'])

#     # Create a list of ranges based on the provided values
#     x_axis = [minor_value] + [f"{round(i, 1)}% to {round((i + interval - 0.01), 2)}%" for i in np.arange(min_value, max_value, interval)] + [major_value]

#     # TODO: find a way to remove it
#     if jsonfile_name['min_value_graph'] == -1:
#         x_axis.insert(6, "0%")
#         x_axis[1] = '-0.99% to -0.81%'
#         x_axis[7] = '0.01% to 0.19%'
#     elif jsonfile_name['min_value_graph'] == -10:
#         x_axis.insert(3, "0%")
#         x_axis[5] = '0.01% to 4.99%'
#     elif jsonfile_name['min_value_graph'] == 0:    
#         x_axis[1] = '0.01% to 4.99%'

#     y_axis = np.zeros(len(x_axis))

#     # Create dataframe for bins and their values
#     data = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[jsonfile_name['column_1'], jsonfile_name['column_2']])
            

#     # Display title and subtitle for the question
#     st.subheader(jsonfile_name['title_question'])
#     st.write(jsonfile_name['subtitle_question'])

#     # Create a container for the data editor and other elements
#     data_container = st.container()

#     # Integrate the updated logic for displaying data editor and handling percentages
#     with data_container:
#         # Create table and plot layout
#         table, plot = st.columns([0.4, 0.6], gap="large")

#         with table:
#             # Calculate the height based on the number of rows
#             row_height = 35  # Adjust as necessary based on row size
#             table_height = ((len(data)+1) * row_height) 
#             # Display the data editor
#             bins_grid = st.data_editor(data, 
#                                        key=jsonfile_name['key'], 
#                                        hide_index=True, 
#                                        use_container_width=True, 
#                                        disabled=[jsonfile_name['column_1']],
#                                        height = table_height)

#             # Calculate the remaining percentage to be allocated
#             percentage_difference = round(100 - sum(bins_grid[jsonfile_name['column_2']]))

#             # Helper function to display status message
#             def display_message(message, color):
#                 styled_message = f'<b style="font-family:sans-serif; color:{color}; font-size: 20px; padding: 10px;">{message}</b>'
#                 st.markdown(styled_message, unsafe_allow_html=True)

#             # Display appropriate message based on the percentage difference
#             if percentage_difference > 0:
#                 display_message(f'You still have to allocate {percentage_difference}% probability.', 'Red')
#             elif percentage_difference == 0:
#                 display_message('You have allocated all probabilities!', 'Green')
#             else:
#                 display_message(f'You have inserted {abs(percentage_difference)}% more, please review your percentage distribution.', 'Red')


#         with plot:
#             # Extract the updated values from the second column
#             updated_values = bins_grid[jsonfile_name['column_2']]

#             # Get rid of plot menu
#             config = {'displayModeBar': False, "staticPlot": True }
                    
#             # Plot the updated values as a bar plot
#             fig = go.Figure()
#             fig.add_trace(go.Bar(
#                 x=bins_grid[jsonfile_name['column_1']], 
#                 y=updated_values, 
#                 marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
#                 marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
#                 marker_line_width=2,  # Width of the bar outline
#                 text=[f"{p}" for p in bins_grid[jsonfile_name['column_2']]],  # Adding percentage labels to bars
#                 textposition='auto',
#                 name='Probability'
#             ))

#             fig.update_layout(
#                 title={
#                     'text': "Probability distribution",
#                     'y':0.9,
#                     'x':0.5,
#                     'xanchor': 'center',
#                     'yanchor': 'top'
#                 },
#                 xaxis_title="Expectation Range",
#                 yaxis_title="Probability (%)",
#                 yaxis=dict(
#                     range=[0, 100], 
#                     gridcolor='rgba(255, 255, 255, 0.2)',  # Light grid on dark background
#                     showline=True,
#                     linewidth=2,
#                     linecolor='white',
#                     mirror=True
#                 ),
#                 xaxis=dict(
#                     tickangle=-45,
#                     showline=True,
#                     linewidth=2,
#                     linecolor='white',
#                     mirror=True
#                 ),
#                 font=dict(color='white'),  # White font color for readability
#             width = 350,
#             height = 400
#             )
#             st.plotly_chart(fig, config = config ,use_container_width=True)

#     return pd.DataFrame(bins_grid), percentage_difference, len(bins_grid)
    
def effect_size_question(jsonfile_name):
    col1, _ = st.columns(2)
    with col1:
        st.markdown(jsonfile_name['effect_size'])
        st.text_input("Please insert a number or skip if you are unsure.", key = jsonfile_name['num_input_question'])



def add_submission(updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df ):
#
    updated_bins_list = [updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df]#, updated_bins_question_2_df]

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
    # Create names
    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'


    
    YEARS_AS_ADVISOR = 'Years as Advisor'
    JOIN_DATE_EEN = 'Join Date EEN'
    EXPERT_OR_GENERALIST = 'Expert or Generalist'
    WORK_DEDICATION = 'Work Dedication'
    FIRMS_CONSULTED_PW = 'Firms Consulted Per Week'
    AVG_WORKING_HOURS_PER_CLIENT = 'Average Working Hours Per Client'
    NUM_FIRMS_ADVISED = 'Number of Firms Advised on Sustainability'
    PERSONAL_HOURLY_FEE = 'Personal Hourly Fee'
    FIRM_FEE_DIFFERENT = 'Is Firm Fee Different'
    FIRM_HOURLY_FEE = 'Firm Hourly Fee'
    MEETING_FREQUENCY_ADVISORS = 'Meeting Frequency with Firms'
    MEETING_DURATION_ADVISORS = 'Typical Meeting Duration'
    FIRM_HOURS_PER_WEEK = 'Firm Consulting Hours per Week'
    PERSONAL_HOURS_PER_WEEK = 'Personal Consulting Hours per Week'
    EXPECTED_REDUCTION = 'Expected Number of Firms Achieving Energy Reduction'
    MEASURES_EFFECTIVENESS_MOST = 'Most Effective Actions or Solutions'
    MEASURES_EFFECTIVENESS_LEAST = 'Least Effective Actions or Solutions'
    RANKED_TOPICS_BY_TIME_COVERED = 'Ranked Topics by Time Covered'
    ADVICE_FOLLOWED_BY_FIRMS = 'Advice Firms Chose to Follow'
    REASONS_FOR_FIRMS_FOLLOWING = 'Reasons Firms Followed Advice'
    REASONS_FOR_FIRMS_FOLLOWING_OTHER = 'Reasons Firms Followed Advice - Other'
    ADVICE_NOT_FOLLOWED_BY_FIRMS = 'Advice Firms Did Not Follow'
    REASONS_FIRMS_NOT_FOLLOWING = 'Reasons Firms Did Not Follow Advice'
    REASONS_FIRMS_NOT_FOLLOWING_OTHER = 'Reasons Firms Not Following Advice - Other'
    PERSONNEL_TRAINING_AGREEMENT = 'Agreement on Personnel Training'
    IMPORTANT_INVESTMENT_CRITERION = 'Important Investment Criterion'
    INVESTMENT_CRITERION_OTHER = 'Other Important Investment Criterion'
    TECHNOLOGY_EFFECTIVENESS_DATA = 'Technology Effectiveness Data'
    TYPICAL_MONTHLY_ENERGY_EXPENDITURE = 'Typical Monthly Energy Expenditure'
    # MEETING_FREQUENCY = 'Meeting Frequency'
    # MEETING_DURATION = 'Meeting Duration'
    # TOPICS_DISCUSSED = 'Topics Discussed'
    # TIME_COVERED_RANKINGS = 'Time Covered Rankings'
    # ADVICE_FOLLOWED = 'Advice Followed by Firms'
    # REASONS_FOLLOWED = 'Reasons Firms Followed Advice'
    # ADVICE_NOT_FOLLOWED = 'Advice Not Followed by Firms'
    # REASONS_NOT_FOLLOWED = 'Reasons Firms Did Not Follow Advice'
    # EXPECTED_REDUCTION = 'Expected Reduction in Energy Use'
    # MOST_EFFECTIVE_MEASURES = 'Most Effective Measures'
    # LEAST_EFFECTIVE_MEASURES = 'Least Effective Measures'
    # PERSONAL_HOURLY_FEE = "Personal Hourly Fee"
    # FIRM_HOURLY_FEE = "Firm Hourly Fee"
    # FIRM_HOURS_PER_WEEK = "Firm Hours Per Week"
    # PERSONAL_HOURS_PER_WEEK = "Personal Hours Per Week"
    # REASONS_FOR_FOLLOWING = "Reasons for Following Advice"
    # MEETING_EFFECTIVENESS = "Meeting Effectiveness"


    
    MIN_EFF_SIZE_Q1 = 'Minimum Effect Size Q1'
    MIN_EFF_SIZE_Q2 = 'Minimum Effect Size Q2'
    MIN_EFF_SIZE_Q3 = 'Minimum Effect Size Q3'
    MIN_EFF_SIZE_Q4 = 'Minimum Effect Size Q4'
    MIN_EFF_SIZE_Q5 = 'Minimum Effect Size Q5'
    MIN_EFF_SIZE_Q6 = 'Minimum Effect Size Q6'
    MIN_EFF_SIZE_Q7 = 'Minimum Effect Size Q7'
    MIN_EFF_SIZE_Q8 = 'Minimum Effect Size Q8'
    COST_BENEFIT_RATIO = 'Cost-Benefit Ratio'
    RISK_AVERSION = 'Risk Aversion'


    
    # Append user inputs to the session state data dictionary
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))



    
    
    data[YEARS_AS_ADVISOR].append(safe_var('years_as_advisor'))
    data[JOIN_DATE_EEN].append(safe_var('join_date_een'))
    data[EXPERT_OR_GENERALIST].append(safe_var('expert_or_generalist'))
    data[WORK_DEDICATION].append(safe_var('work_dedication'))
    data[FIRMS_CONSULTED_PW].append(safe_var('firms_consulted_pw'))
    data[AVG_WORKING_HOURS_PER_CLIENT].append(safe_var('working_hours'))
    data[NUM_FIRMS_ADVISED].append(safe_var('num_firms_advised'))
    data[PERSONAL_HOURLY_FEE].append(safe_var('personal_hourly_fee'))
    data[FIRM_FEE_DIFFERENT].append(safe_var('firm_fee_different'))
    #data[FIRM_HOURLY_FEE].append(safe_var('firm_hourly_fee'))
    data[MEETING_FREQUENCY_ADVISORS].append(safe_var('meeting_frequency_advisors'))
    data[MEETING_DURATION_ADVISORS].append(safe_var('meeting_duration_advisors'))
    data[FIRM_HOURS_PER_WEEK].append(safe_var('firm_hours_per_week'))
    data[PERSONAL_HOURS_PER_WEEK].append(safe_var('personal_hours_per_week'))
    data[EXPECTED_REDUCTION].append(safe_var('expected_reduction'))
    data[MEASURES_EFFECTIVENESS_MOST].append(safe_var('measures_effectiveness_most'))
    data[MEASURES_EFFECTIVENESS_LEAST].append(safe_var('measures_effectiveness_least'))
    data[ADVICE_FOLLOWED_BY_FIRMS].append(safe_var('advice_followed_by_firms'))
    
    data[REASONS_FOR_FIRMS_FOLLOWING].append(safe_var('reasons_for_firms_following'))
    data[ADVICE_NOT_FOLLOWED_BY_FIRMS].append(safe_var('advice_not_followed_by_firms'))
    data[REASONS_FIRMS_NOT_FOLLOWING].append(safe_var('reasons_firms_not_following'))
    #data[REASONS_FIRMS_NOT_FOLLOWING_OTHER].append(safe_var('reasons_firms_not_following_other'))
    data[PERSONNEL_TRAINING_AGREEMENT].append(safe_var('personnel_training_agreement'))
    data[IMPORTANT_INVESTMENT_CRITERION].append(safe_var('important_investment_criterion'))
    data[TYPICAL_MONTHLY_ENERGY_EXPENDITURE].append(safe_var('typical_monthly_energy_expenditure'))
    # data[MEETING_FREQUENCY].append(safe_var('meeting_frequency_advisors'))
    # data[MEETING_DURATION].append(safe_var('meeting_duration_advisors'))
    # data[TOPICS_DISCUSSED].append(safe_var('meeting_topics_advisors'))
    # data[TIME_COVERED_RANKINGS].append(safe_var('time_covered_ranking'))
    # data[ADVICE_FOLLOWED].append(safe_var('advice_followed_by_firms'))
    # data[REASONS_FOLLOWED].append(safe_var('reasons_for_firms_following'))
    # data[ADVICE_NOT_FOLLOWED].append(safe_var('advice_not_followed_by_firms'))
    # data[REASONS_NOT_FOLLOWED].append(safe_var('reasons_firms_not_following'))
    # data[EXPECTED_REDUCTION].append(safe_var('expected_reduction'))
    # data[MOST_EFFECTIVE_MEASURES].append(safe_var('measures_effectiveness_most'))
    # data[LEAST_EFFECTIVE_MEASURES].append(safe_var('measures_effectiveness_least'))
    # data[PERSONAL_HOURLY_FEE].append(safe_var('personal_hourly_fee'))
    # data[FIRM_HOURLY_FEE].append(safe_var('firm_hourly_fee'))
    # data[FIRM_HOURS_PER_WEEK].append(safe_var('firm_hours_per_week'))
    # data[PERSONAL_HOURS_PER_WEEK].append(safe_var('personal_hours_per_week'))
    # data[REASONS_FOR_FOLLOWING].append(safe_var('reasons_for_firms_following'))
    # data[MEETING_EFFECTIVENESS].append(safe_var('meeting_effectiveness_advisors'))



    
    data[MIN_EFF_SIZE_Q1].append(safe_var('num_input_question1'))
    data[MIN_EFF_SIZE_Q2].append(safe_var('num_input_question2'))
    data[MIN_EFF_SIZE_Q3].append(safe_var('num_input_question3'))
    data[MIN_EFF_SIZE_Q4].append(safe_var('num_input_question4'))
    data[MIN_EFF_SIZE_Q5].append(safe_var('num_input_question5'))
    data[MIN_EFF_SIZE_Q6].append(safe_var('num_input_question6'))
    data[MIN_EFF_SIZE_Q7].append(safe_var('num_input_question7'))
    data[MIN_EFF_SIZE_Q8].append(safe_var('num_input_question8'))
    data[COST_BENEFIT_RATIO].append(safe_var('cost_benefit'))
    data[RISK_AVERSION].append(safe_var('risk_aversion'))
    if safe_var('firm_fee_different') == "Yes":
        data[FIRM_HOURLY_FEE].append(safe_var('firm_hourly_fee'))
    else:
        data[FIRM_HOURLY_FEE].append(None) 
        
    # Append 'Other' reasons if provided
    if 'reasons_for_firms_following_other' in st.session_state:
        data[REASONS_FOR_FIRMS_FOLLOWING_OTHER].append(safe_var('reasons_for_firms_following_other'))
    else:
        data[REASONS_FOR_FIRMS_FOLLOWING_OTHER].append(None)

    # Append 'Other' reasons if provided
    if 'reasons_firms_not_following_other' in st.session_state:
        data[REASONS_FIRMS_NOT_FOLLOWING_OTHER].append(safe_var('reasons_firms_not_following_other'))
    else:
        data[REASONS_FIRMS_NOT_FOLLOWING_OTHER].append(None)
        
    # Handle the "Other" option for investment criterion
    if st.session_state.get("important_investment_criterion") == "Other (please specify)":
        data[INVESTMENT_CRITERION_OTHER].append(safe_var('investment_criterion_other'))
    else:
        data[INVESTMENT_CRITERION_OTHER].append(None)
    
    # For ranked topics, ensure you capture the user input
    # Assuming 'ranked_topics' is the list of topics after user ranking
    #data[RANKED_TOPICS_BY_TIME_COVERED].append(safe_var('time_covered_ranking'))
    data[RANKED_TOPICS_BY_TIME_COVERED].append(safe_var('ranked_topics_output'))
    # For the technology effectiveness data
    if 'edited_df' in st.session_state:
        edited_df_session = st.session_state['edited_df']
        
        # Debugging statements
        st.write("Type of edited_df:", type(edited_df_session))
        st.write("Content of edited_df:", edited_df_session)
        
        if isinstance(edited_df_session, pd.DataFrame):
            data[TECHNOLOGY_EFFECTIVENESS_DATA].append(edited_df_session.to_dict(orient='records'))
        elif isinstance(edited_df_session, dict):
            data[TECHNOLOGY_EFFECTIVENESS_DATA].append(edited_df_session)
        else:
            data[TECHNOLOGY_EFFECTIVENESS_DATA].append(None)
    else:
        data[TECHNOLOGY_EFFECTIVENESS_DATA].append(None)
    
    session_state_df = pd.DataFrame(data)


    # # Step 1: Align and concatenate DataFrames
    # if session_state_df.shape[0] > questions_df.shape[0]:
    #     questions_df = questions_df.reindex(session_state_df.index, fill_value=None)
    # elif questions_df.shape[0] > session_state_df.shape[0]:
    #     session_state_df = session_state_df.reindex(questions_df.index, fill_value=None)
    # concatenated_df = pd.concat(
    # [session_state_df, questions_df.set_index(session_state_df.index)],
    # axis=1
    # ).astype(str)  # Convert to string-compatible types
    
    # # Step 2: Authenticate with Google Sheets
    # scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    # client = gspread.authorize(creds)
    # sheet = client.open("EEN_Survey_Data").sheet1
    
    # # Step 3: Update headers only if necessary
    # existing_headers = sheet.row_values(1) or []
    # missing_headers = [col for col in concatenated_df.columns if col not in existing_headers]
    # if missing_headers:
    #     existing_headers += missing_headers
    #     sheet.update(f"A1:{gspread.utils.rowcol_to_a1(1, len(existing_headers))}", [existing_headers])
    
    # # Step 4: Append data in one batch
    # sheet.append_rows(concatenated_df.values.tolist())



    if session_state_df.shape[0] > questions_df.shape[0]:
        questions_df = questions_df.reindex(session_state_df.index, fill_value=None)
    elif questions_df.shape[0] > session_state_df.shape[0]:
        session_state_df = session_state_df.reindex(questions_df.index, fill_value=None)

    # Concatenate the DataFrames
    concatenated_df = pd.concat(
        [session_state_df, questions_df.set_index(session_state_df.index)],
        axis=1
    )

    # Ensure JSON compatibility
    concatenated_df = concatenated_df.applymap(
        lambda x: str(x) if not isinstance(x, (int, float, str)) else x
    )
    concatenated_df = concatenated_df.fillna("")  # Replace NaN/None with an empty string
    st.dataframe(session_state_df)
    st.dataframe(questions_df)
    st.dataframe(concatenated_df)
    # Step 2: Authenticate and access Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    client = gspread.authorize(creds)
    sheet = client.open("EEN_Survey_Data").sheet1

    # Step 3: Handle dynamic headers
    existing_headers = sheet.row_values(1) or []
    missing_headers = [col for col in concatenated_df.columns if col not in existing_headers]
    if missing_headers:
        existing_headers += missing_headers
        sheet.update(f"A1:{gspread.utils.rowcol_to_a1(1, len(existing_headers))}", [existing_headers])

    # Step 4: Append rows in one batch
    sheet.append_rows(concatenated_df.values.tolist())





    # if session_state_df.shape[0] > questions_df.shape[0]:
    #     questions_df = questions_df.reindex(session_state_df.index, fill_value="empty")
    # elif questions_df.shape[0] > session_state_df.shape[0]:
    #     session_state_df = session_state_df.reindex(questions_df.index, fill_value="empty")
    # # Combine `session_state_df` with `questions_df`
    # concatenated_df = pd.concat(
    #     [session_state_df, questions_df.set_index(session_state_df.index)],
    #     axis=1
    # )
    # st.dataframe(concatenated_df)
    # st.dataframe(session_state_df)
    # st.dataframe(questions_df)
    # # Step 3: Authenticate and open Google Sheet
    # scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    # client = gspread.authorize(creds)

    # sheet = client.open("EEN_Survey_Data").sheet1

    # # Step 4: Handle dynamic headers
    # existing_headers = sheet.row_values(1)  # Retrieve headers from the first row
    # if not existing_headers:
    #     existing_headers = []

    # # Ensure all concatenated DataFrame columns have corresponding headers in the sheet
    # for column_name in concatenated_df.columns:
    #     if column_name not in existing_headers:
    #         existing_headers.append(column_name)
    #         # Update the sheet header row
    #         sheet.update(f"A1:{gspread.utils.rowcol_to_a1(1, len(existing_headers))}", [existing_headers])

    # # Step 5: Write data to corresponding columns
    # existing_data = sheet.get_all_values()
    # next_row = len(existing_data) + 1

    # for column_name in concatenated_df.columns:
    #     if column_name in existing_headers:
    #         col_index = existing_headers.index(column_name) + 1
    #         value_to_write = concatenated_df.iloc[-1][column_name]
    #         cell_address = gspread.utils.rowcol_to_a1(next_row, col_index)
    #         sheet.update(cell_address, value_to_write)

    st.success("Data successfully added to the sheet!")
