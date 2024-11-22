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


# Insert consent
def add_consent():
    st.session_state['consent'] = True
    st.session_state['data']['Consent'] = ['Yes']
      

# Define a function to handle the Next button
def next_page():
    st.session_state['page'] += 1


def consent_form():
    st.markdown("""
    By submitting the form below you agree to your data being used for research purposes. 
    """)
    agree = st.checkbox("I understand and consent.")
    if agree:
        st.markdown("You have consented. Select \"Next\" to start the survey.")
        st.button('Next', on_click=add_consent)
        
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

SECTION_ONE = '''Section 1: Background Information'''
SECTION_THREE = '''Section 3: Final Section'''
SECTION_TWO = '''Section 2: Expectations about the Impacts of the Program'''

def personal_information():
    st.subheader("Section 1: Background Information")
    col1, _ = st.columns(2)
    with col1:
        st.text_input("Please, enter your full name:", key = 'user_full_name')
        st.text_input("Please, enter your working title:", key = 'user_position')
        st.selectbox('Please, specify your professional category:', ( 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor/Policy implementer', 'Entrepreneur/Firm Representative'), key="professional_category")
#'Policy implementer (EENergy consortium working package leaders)'
TITLE_INSTRUCTIONS = '''Instructions'''

SUBTITLE_INSTRUCTIONS = '''This example is designed to help you understand how to respond to this survey effectively.
\n\nFor each question, you will see a table with two columns. Please allocate percentages in the "Your Belief (%)" column to reflect how likely you think a specific event is. The total across all rows should add up to 100%. The plot next to the table will show the distribution of your answers.\n\nAs an example, suppose we asked about your expectations for tomorrow's maximum temperature in degrees Celsius in your city or town.'''

CAPTION_INSTRUCTIONS = '''**In this case, your prediction indicates a 45\% chance of the maximum temperature reaching 26 degrees Celsius, 20\% chance of it reaching 27 degrees Celsius, and so on.**\n\n'''


def sustainability_advisors_question():
    if st.session_state['professional_category'] == 'Sustainability Advisor/Policy implementer':
        st.write("")
        st.write("")
        st.subheader(SECTION_THREE)
        # st.write(SECTION_TWO_NOTES)
        col1, _ = st.columns(2)

        with col1:
            # Advisor Background and Experience
            st.subheader("Advisor Background and Experience")
            st.number_input(
                "1. How many years have you been working as an advisor on energy efficiency topics?",
                min_value=0.0,
                step=0.5,
                format="%.1f",
                key='years_as_advisor'
            )
            st.date_input("2. In which year did you join EEN?", key="join_date_een")
            st.radio(
                "3. Do you describe yourself as an energy efficiency expert, generalist, or other?",
                options=["Energy efficiency expert", "Generalist", "Other"],
                key="expert_or_generalist"
            )
            st.selectbox(
                "4. On average, what percentage of your work is related to energy efficiency topics?",
                options=["Less than 30%", "30-70%", "More than 70%"],
                key="work_dedication"
            )
            # Workload and Client Interactions
            st.subheader("Workload and Client Interactions")
            st.write("For the following questions, please reflect on your typical work within the **past 6 months**.")
            
            # Question 5: Number of firms advised
            st.number_input(
                "5. In a typical week, how many firms do you advise on energy efficiency topics? (Include all clients, not just those within EEN)",
                min_value=0,
                step=1,
                key="firms_consulted_pw"
            )
            
            st.number_input(
                "6. In a typical week, how many firms do you advise on sustainable development practices unrelated to energy efficiency?",
                min_value=0,
                step=1,
                key="num_firms_advised"
            )
            
            # Question 7: Average hours per client
            st.number_input(
                "7. On average, how many hours do you spend working with each client on a project or service?",
                min_value=0.0,
                step=0.5,
                key="working_hours"
            )
            
            # Question 8: Meeting frequency
            st.selectbox(
                "8. How often do you meet with the firms you advise?",
                options=["Daily", "Weekly", "Monthly", "Quarterly", "Annually", "As needed"],
                key="meeting_frequency_advisors"
            )
            
            # Question 9: Meeting duration
            st.selectbox(
                "9. How long are your typical meetings with the firms you advise?",
                options=["Less than 30 minutes", "30-60 minutes", "1-2 hours", "More than 2 hours"],
                key="meeting_duration_advisors"
            )
            
            # Consultancy and Advisory Fees
            st.subheader("Consultancy and Advisory Fees")
            st.radio(
                "10. What is your per hour consultancy fee?",
                options=[
                    "Less than €50",
                    "€50 - €100",
                    "€100 - €150",
                    "€150 - €200",
                    "More than €200"
                ],
                key="personal_hourly_fee"
            )
            
            st.radio(
                "11. Is your firm's per hour consultancy fee different from your personal fee?",
                options=["Yes", "No"],
                key="firm_fee_different"
            )
            
            if st.session_state.get("firm_fee_different") == "Yes":
                st.radio(
                    "What is your firm's average per hour consultancy fee?",
                    options=[
                        "Less than €50",
                        "€50 - €100",
                        "€100 - €150",
                        "€150 - €200",
                        "More than €200"
                    ],
                    key="firm_hourly_fee"
                )
            
            # Consultancy and Advisory Hours
            st.subheader("Consultancy and Advisory Hours")
            st.number_input(
                "12. In a typical week, how many hours of consulting/advice do you personally provide?",
                min_value=0,
                step=1,
                key="personal_hours_per_week"
            )
            
            st.number_input(
                "13. Approximately, how many hours of consulting/advice does your firm provide in a typical week?",
                min_value=0,
                step=1,
                key="firm_hours_per_week"
            )
            # # Workload and Client Interactions
            # st.subheader("Workload and Client Interactions")
            # st.write("For the following questions, please reflect on your typical work within the **past 6 months**.")
            # st.number_input(
            #     "5. How many firms do you advise on energy efficiency topics in a typical work week? (Include all clients, not just those within EEN)",
            #     min_value=0,
            #     step=1,
            #     key="firms_consulted_pw"
            # )
            # st.number_input(
            #     "6. On average, how many hours in total do you spend working with each client on a project or service?",
            #     min_value=0.0,
            #     step=0.5,
            #     key="working_hours"
            # )
            # st.number_input(
            #     "7. How many firms do you advise on sustainable development practices unrelated to energy efficiency?",
            #     min_value=0,
            #     step=1,
            #     key="num_firms_advised"
            # )
            # st.selectbox(
            #     "8. How often do you meet with the firms you advise?",
            #     options=["Daily", "Weekly", "Monthly", "Quarterly", "Annually", "As needed"],
            #     key="meeting_frequency_advisors"
            # )
            # st.selectbox(
            #     "9. How long are your typical meetings with the firms you advise?",
            #     options=["Less than 30 minutes", "30-60 minutes", "1-2 hours", "More than 2 hours"],
            #     key="meeting_duration_advisors"
            # )
            
            # # Consultancy and Advisory Fees
            # st.subheader("Consultancy and Advisory Fees")
            # st.radio(
            #     "10. What is your per hour consultancy fee, averaged for the last 30 days?",
            #     options=[
            #         "Less than €50",
            #         "€50 - €100",
            #         "€100 - €150",
            #         "€150 - €200",
            #         "More than €200"
            #     ],
            #     key="personal_hourly_fee"
            # )
            # st.radio(
            #     "11. What is the average per hour consultancy fee for your firm, if different, averaged for the last 30 days?",
            #     options=[
            #         "Less than €50",
            #         "€50 - €100",
            #         "€100 - €150",
            #         "€150 - €200",
            #         "More than €200",
            #         "Not applicable (same as personal)"
            #     ],
            #     key="firm_hourly_fee"
            # )
            
            # # Consultancy and Advisory Hours
            # st.subheader("Consultancy and Advisory Hours")
            # st.number_input(
            #     "12. In the last 30 days, how many hours of consulting/advice per week has **your firm** provided?",
            #     min_value=0,
            #     step=1,
            #     key="firm_hours_per_week"
            # )
            # st.number_input(
            #     "13. In the last 30 days, how many hours of consulting/advice per week have **you personally** provided?",
            #     min_value=0,
            #     step=1,
            #     key="personal_hours_per_week"
            # )
            
            # Effectiveness and Expected Outcomes
            st.subheader("Effectiveness and Expected Outcomes")
            st.number_input(
                "14. Of the 707 firms selected for the EENergy project, how many do you expect will achieve a reduction in energy use?",
                min_value=0,
                max_value=707,
                step=1,
                key="expected_reduction"
            )
            st.text_area(
                "15. In your opinion, what actions or solutions are **most helpful** for reducing a firm's energy use? (What might the success of an average firm depend on?)",
                key="measures_effectiveness_most"
            )
            st.text_area(
                "16. In your opinion, what actions or solutions are **least helpful** for reducing a firm's energy use?",
                key="measures_effectiveness_least"
            )
            
            # Rank Topics by Time Covered During Meetings
            st.subheader("Rank Topics by Time Covered During Meetings")
            st.write("Please rank the following topics based on the amount of time you typically spend discussing them during meetings with firms. Drag and drop to reorder the list, with the topic you spend the **most time** on at the top.")
            topics = [
                "Energy efficiency strategies",
                "Sustainable development practices",
                "Cost-saving measures",
                "Regulatory compliance",
                "Technology upgrades",
                "Employee training",
                "Environmental impact assessments",
                "Other"
            ]
            # Allow users to rank topics via drag-and-drop
            ranked_topics = sort_items(
                items=topics,
                direction="vertical",
                key="time_covered_ranking"
            )
            # Store the ranked topics in session state
            st.session_state['ranked_topics_output'] = ranked_topics
            
            # Display the final ranking
            st.write("You ranked the topics as follows (by time covered):")
            st.write(ranked_topics)
            

            

            # Advice Followed by Firms
            st.subheader("Advice Followed by Firms")
            st.text_area(
                "19. What advice have you given to firms that they have **chosen to follow**?",
                key="advice_followed_by_firms"
            )
            
            st.write("Why do you think firms chose to follow your advice?")
            st.multiselect(
                "Select all reasons that apply:",
                options=[
                    "Clear financial benefits",
                    "Strong management support",
                    "Technological feasibility",
                    "Regulatory compliance requirements",
                    "Alignment with sustainability goals",
                    "Other"
                ],
                key="reasons_for_firms_following"
            )
            
            # If 'Other' is selected, provide a text input for additional details
            if "Other" in st.session_state.get("reasons_for_firms_following", []):
                st.text_input(
                    "Please specify other reasons:",
                    key="reasons_for_firms_following_other"
                )
            
            st.subheader("Advice Not Followed by Firms")
            st.text_area(
                "21. What advice have you given to firms that they decided **not to follow**?",
                key="advice_not_followed_by_firms"
            )
            
            st.write("Why do you think firms chose **not to follow** your advice?")
            st.multiselect(
                "Select all reasons that apply:",
                options=[
                    "Financial costs",
                    "Labor costs",
                    "Lack of management support",
                    "Technological constraints",
                    "Insufficient perceived benefits",
                    "Other"
                ],
                key="reasons_firms_not_following"
            )
            
            # If 'Other' is selected, provide a text input for additional details
            if "Other" in st.session_state.get("reasons_firms_not_following", []):
                st.text_input(
                    "Please specify other reasons:",
                    key="reasons_firms_not_following_other"
                )
            # Firm Size Information
            st.subheader("Firm Size Information")
            st.number_input(
                "What is the typical monthly energy expenditure of the firms you usually advise? (in euros)",
                min_value=0,
                step=100,
                key="typical_monthly_energy_expenditure"
            )
            # Additional Questions
            st.subheader("Additional Questions")
            st.radio(
                "23. Please indicate your agreement with the following statement:\n\n**\"For energy efficiency investments to be successful, firms must usually undertake personnel training.\"**",
                options=[
                    "1 - Largely disagree",
                    "2 - Somewhat disagree",
                    "3 - Neither agree nor disagree",
                    "4 - Somewhat agree",
                    "5 - Largely agree"
                ],
                key="personnel_training_agreement"
            )
            st.radio(
                "24. What criterion do you consider most important when recommending a particular investment?",
                options=[
                    "Payback time / Breakeven time",
                    "Total cost savings, regardless of time",
                    "Other (please specify)"
                ],
                key="important_investment_criterion"
            )
            if st.session_state.get("important_investment_criterion") == "Other (please specify)":
                st.text_input("Please specify the criterion:", key="investment_criterion_other")

            # Technologies Effectiveness Assessment
            st.subheader("(Final Question!) Technologies Effectiveness Assessment")
            st.write("Please complete the table below for each technology. For **Energy Savings**, use the units **euros saved per euro invested (€/€1000 invested)**.")
            st.write("**Note:** Please consider this for a firm of the size you usually advise.")
            
            st.markdown("""
            - **Breakeven Time (months)**: How many months will it take to recover the money spent on this technology (e.g., '12' for 12 months).
            - **Energy Savings (€/€1000 invested)**: How much money is saved for every €1000 invested in this technology? For example, if the savings are €500 per €1000 invested, write '500'. If you are unsure, leave the field blank or provide an estimate.
            """)
            
            technologies = [
                "Renewable Energy (PV Panels)",
                "Energy Storage",
                "Combined Renewable + Storage",
                "Efficient Lighting",
                "HVAC Systems",
                "Building Upgrades",
                "Machinery Upgrades",
                "Energy-Efficient Vehicles"
            ]
            
            # Initialize data
            data_df = {
                "Technology": technologies,
                "Breakeven Time (months)": ["" for _ in technologies],
                "Energy Savings (€/€1000 invested)": ["" for _ in technologies]
            }
            
            df = pd.DataFrame(data_df)
            
            # Display the data editor
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                disabled=['Technology'],
                key='edited_df'
            )
            
            # # Advisor Background and Experience
            # st.subheader("Advisor Background and Experience")
            # st.number_input("How many years have you been working as an advisor on energy efficiency topics?", 
            #     min_value=0.0, 
            #     step=0.5, 
            #     format="%.1f", 
            #     key='years_as_advisor')
            # st.date_input("In which year did you join EEN?", key="join_date_een")
            # st.radio("Do you describe yourself as an energy efficiency expert, generalist, or other?", options=["Energy efficiency expert", "Generalist", "Other"], key="expert_or_generalist")
            # # st.multiselect("When evaluating energy efficiency, what do you rely on most? (Select all that apply)", options=["Formal training", "Professional knowledge", "Experience", "Combination"], key="assessment_basis")
            # st.selectbox("On average, what percentage of your work is related to energy efficiency topics?", options=["Less than 30%", "30-70%", "More than 70%"], key="work_dedication")
            # #st.selectbox("How do you usually find new clients or start working with them?", options=["Referrals", "Cold outreach", "Inbound inquiries", "Networking events", "Other"], key="client_acquisition")
            
            # # Workload and Client Interactions
            # st.subheader("Workload and Client Interactions")
            # st.write("For the following questions, please reflect on your typical work within the past 6 months.")
            # st.number_input("How many firms do you advise on energy efficiency topics in a typical work week? (include all clients, not just those within EEN)?", min_value=0, step=1, key="firms_consulted_pw")
            # st.number_input("On average, how many hours in total do you spend working with each client on a project or service?", min_value=0.0, step=0.5, key="working_hours")

            # st.number_input("How many firms do you advise on sustainable development practices unrelated to energy efficiency?", min_value=0, step=1, key="num_firms_advised")
            # st.subheader("Consultancy and Advisory Fees")

            # # Question 1: Per hour consultancy fees
            # st.radio(
            #     "What is your per hour consultancy fee, averaged for the last 30 days?",
            #     options=[
            #         "Less than €50",
            #         "€50 - €100",
            #         "€100 - €150",
            #         "€150 - €200",
            #         "More than €200"
            #     ],
            #     key="personal_hourly_fee"
            # )
            
            # # Question 2: Firm's average per hour consultancy fees
            # st.radio(
            #     "What is the average per hour consultancy fee for your firm, if different, averaged for the last 30 days?",
            #     options=[
            #         "Less than €50",
            #         "€50 - €100",
            #         "€100 - €150",
            #         "€150 - €200",
            #         "More than €200",
            #         "Not applicable (same as personal)"
            #     ],
            #     key="firm_hourly_fee"
            # )
            # # Client Engagement and Meeting Effectiveness
            # st.subheader("Client Engagement and Meeting Effectiveness")
            # st.selectbox("How often do you meet with the firms you advise?", options=["Daily", "Weekly", "Monthly", "Quarterly", "Annually", "As needed"], key="meeting_frequency_advisors")
            # st.selectbox("How long are your typical meetings with the firms you advise?", options=["Less than 30 minutes", "30-60 minutes", "1-2 hours", "More than 2 hours"], key="meeting_duration_advisors")

            
            # st.subheader("Consultancy and Advisory Hours")
            
            # # Question 3: Hours of consulting/advice provided by the firm
            # st.number_input(
            #     "In the last 30 days, how many hours of consulting/advice per week has your firm provided?",
            #     min_value=0,
            #     step=1,
            #     key="firm_hours_per_week"
            # )
            
            # # Question 4: Hours of consulting/advice you provided personally
            # st.number_input(
            #     "In the last 30 days, how many hours of consulting/advice per week have you personally provided?",
            #     min_value=0,
            #     step=1,
            #     key="personal_hours_per_week"
            # )
            # # Effectiveness of Energy Efficiency Measures and Expected Outcomes
            # st.write("**Effectiveness and Expected Outcomes**")
            # st.number_input("Of the 707 firms selected for the EENergy project, how many do you expect will achieve a reduction in energy use?", min_value=0, max_value=707, step=1, key="expected_reduction")
            # st.text_area("In your opinion, what actions or solutions are most helpful for reducing a firm's energy use? (What might the success of an average firm depend on?)", key="measures_effectiveness_most")
            # st.text_area("In your opinion, what actions or solutions are least helpful for reducing a firm's energy use?", key="measures_effectiveness_least")            
            # st.subheader("Rank Topics by Time Covered During Meetings")

            # # List of topics to rank
            # topics = [
            #     "Energy efficiency strategies",
            #     "Sustainable development practices",
            #     "Cost-saving measures",
            #     "Regulatory compliance",
            #     "Technology upgrades",
            #     "Employee training",
            #     "Environmental impact assessments",
            #     "Other"
            # ]
            
            # # Allow users to rank topics via drag-and-drop
            # ranked_topics = sort_items(
            #     topics, 
            #     key="time_covered_ranking", 
            #     direction="vertical"
            # )
            # # Explicitly store the ranked topics in session state
            # st.session_state['ranked_topics_output'] = ranked_topics

            # # Display the final ranking
            # st.write("You ranked the topics as follows (by time covered):")
            # st.write(ranked_topics)
        
            # # Shortened technology names
            # technologies = [
            #     "Renewable Energy (PV Panels)",
            #     "Energy Storage",
            #     "Combined Renewable + Storage",
            #     "Efficient Lighting",
            #     "HVAC Systems",
            #     "Building Upgrades",
            #     "Machinery Upgrades",
            #     "Energy-Efficient Vehicles"
            # ]
            
            # # Initialize data
            # data_df = {
            #     "Technology": technologies,
            #     "Payback Time (months)": ["" for _ in technologies],  # Empty for user input
            #     "Energy Savings (€/€1000)": ["" for _ in technologies]  # Empty for user input
            # }
            

            # df = pd.DataFrame(data_df)
            # df['Technology'] = df['Technology'].astype(str)
            

            
            # # Calculate table height dynamically
            # row_height = 35  # Approximate row height in pixels
            # table_height = (len(df) + 1) * row_height  # Add 1 for the header
            
            # # Display the table
            # st.subheader("Which technologies do you think are most effective in improving energy efficiency?")
            # st.write("Please complete the table below by filling in the following details for each technology:\n1. **Payback Time (months)**: Write how many months it will take to recover the money spent on this technology (e.g., '12' for 12 months). \n2. **Energy Savings (kWh/€1000)**: How much energy is saved for every €1,000 invested in this technology? For example, if the savings are 500 kWh per €1,000 invested, write ‘500’. If you are unsure, leave the field blank or provide an estimate.")
            # df['Technology'] = df['Technology'].astype(str)  # Ensure the first column is treated as strings
            
            # edited_df = st.data_editor(
            #     df,
            #     use_container_width=True,  # Expand to the full container width
            #     hide_index=True,  # Hide the default index
            #     disabled=['Technology'],  # Prevent editing the Technology column
            #     height=table_height,# Adjust height based on rows
            #     key='edited_df'
            # )

            
            # # Advice Given and Client Reactions
            # st.subheader("Advice Given and Client Reactions")
            # st.text_area("What advice have you given to firms that they have chosen to follow?", key="advice_followed_by_firms")
            # st.write("Why do you think firms chose to follow your advice?")
            # st.multiselect(
            #     "Select all reasons that apply:",
            #     options=[
            #         "Cost savings were clear and immediate",
            #         "The advice aligned with their sustainability goals",
            #         "Regulatory compliance requirements",
            #         "The technology or solution was easy to implement",
            #         "Financial support or subsidies were available",
            #         "Peer or industry pressure",
            #         "Trust in your expertise or reputation",
            #         "Other"
            #     ],
            #     key="reasons_for_firms_following"
            # )
            # st.text_area("What advice have you given to firms that they decided not to follow?", key="advice_not_followed_by_firms")
            # st.text_area("Why do you think firms chose not to follow your advice? (e.g., financial costs, labor costs, other reasons)", key="reasons_firms_not_following")

            
            # # Add new questions
            # st.subheader("Additional Questions")
            
            # # Question 1: Agreement on personnel training
            # st.radio(
            #     "Please indicate agreement with the following statement: "
            #     '"For energy efficiency investments to be successful, firms must usually undertake personnel training."',
            #     options=[
            #         "1 - Largely disagree",
            #         "2 - Somewhat disagree",
            #         "3 - Neither agree nor disagree",
            #         "4 - Somewhat agree",
            #         "5 - Largely agree"
            #     ],
            #     key="personnel_training_agreement"
            # )
            
            # # Question 2: Important investment criterion
            # st.radio(
            #     "What criterion do you consider most important when recommending a particular investment?",
            #     options=[
            #         "Payback time / Breakeven time",
            #         "Total cost savings, regardless of time",
            #         "Other (please specify)"
            #     ],
            #     key="important_investment_criterion"
            # )
            
            # if st.session_state.get("important_investment_criterion") == "Other (please specify)":
            #     st.text_input("Please specify the criterion:", key="investment_criterion_other")






def instructions():

    st.subheader(TITLE_INSTRUCTIONS)
    st.write(SUBTITLE_INSTRUCTIONS)

    st.subheader("Temperature Forecast Tomorrow in Your City")
    st.write('_Please scroll on the table to see all available options._')

    #with data_container:
    table, plot = st.columns([0.4, 0.6], gap = "large")
    
    with table:

        # Create some example data as a Pandas DataFrame
        values_column = ['< 20'] + list(range(21, 30)) + ['> 30']
        zeros_column = [0 for _ in values_column]
        zeros_column[4:9] = [5, 15, 45, 20, 15]

        data = {'Temperature': values_column, 'Your Belief (%)': zeros_column}
        df = pd.DataFrame(data)
        # Calculate the height based on the number of rows
        row_height = 35  # Adjust as necessary based on row size
        table_height = ((len(df)+1) * row_height) 
        
        df['Temperature'] = df['Temperature'].astype('str')
    
        st.data_editor(df, use_container_width=True, hide_index=True, disabled=('Temperature', "Your Belief (%)"), height=table_height)

    st.write(CAPTION_INSTRUCTIONS)

    with plot:
        config = {'displayModeBar': False, "staticPlot": True }
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=values_column, 
            y=df['Your Belief (%)'], 
            marker_color='rgba(50, 205, 50, 0.9)',  # A nice bright green
            marker_line_color='rgba(0, 128, 0, 1.0)',  # Dark green outline for contrast
            marker_line_width=2,  # Width of the bar outline
            text=[f"{p}" for p in df['Your Belief (%)']],  # Adding percentage labels to bars
            textposition='auto',
            name='Your Belief (%)'
        ))

        fig.update_layout(
            title={
                'text': "Temperature (Belief Distribution)",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Expectation Range",
            yaxis_title="Your Belief (%)",
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
            font=dict(color='white'),    # White font color for readability
        width = 350,# Adjust width here
        height = 400
        )
        st.plotly_chart(fig,config = config, use_container_width=True)
    

def submit(): 
    st.session_state['submit'] = True
