
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

#st.subheader(SECTION_TWO)
instructions()

# Initialize a dictionary to hold variables
question_variables = {}

for idx, (question_key, question_config) in enumerate(config.items(), start=1):
    if question_key.startswith("question"):  # Only process keys starting with 'question'
        # Process the question using create_question
        updated_bins, percentage_difference, num_bins = create_question(question_config)

        # Process the effect size using effect_size_question
        effect_size = effect_size_question(question_config)

        # Store results in the dictionary using dynamic keys
        question_variables[f"updated_bins_question_{idx}_df"] = updated_bins
        question_variables[f"percentage_difference{idx}"] = percentage_difference
        question_variables[f"num_bins{idx}"] = num_bins
        question_variables[f"effect_size_question{idx}"] = effect_size
col2, _ = st.columns(2)
with col2:
    st.image("SatSunGraph.png", width = 350)
st.write("Saturday and Sunday temperatures in Washington DC for each weekend in 2022. As we might expect, there is a strong correlation between the temperature on a Saturday and on the Sunday, since some parts of the year are hot, and others colder. The correlation here is 0.88.")

# q8_config = config['question8']
# updated_bins_question_8_df, percentage_difference8, num_bins8 = create_question(q8_config)    
    
st.subheader("Question 9 - Cost/Benefit Ratio")
st.write("In simple terms, a cost-benefit ratio is used to compare the costs of a project against the benefits it delivers. For instance, if a program costs €100.000 and the monetized value of its benefits is €150.000, the cost-benefit ratio would be 1:1.5. This means that for every euro spent, the program delivers one and a half euro in benefits. A higher ratio indicates greater efficiency and value for money. This question prompts to consider the efficiency and economic justification for scaling a program, ensuring that the decision aligns with both fiscal responsibility and the desired impact. At what cost-benefit ratio would you consider scaling the EEnergy Efficiency Project?\n Consider “benefits” that occurred after two years of running the program and “costs” as the total expenses incurred to implement, operate, and maintain a program or project (including administration and overhead costs).")

col1, _= st.columns(2)
with col1:
    # list needed later in the cost/benefit question
    cost_benefit_list = [f"1:{round(i, 1)}" for i in np.arange(0.6, 3.1, .2)]
    st.select_slider("Please move the slider to indicate your preference.", cost_benefit_list, key = "cost_benefit")

st.subheader("Question 10 - Risk Aversion")
st.write("Rate your willingness to take risks in general on a 10-point scale, with 1 completely unwilling and 10 completely willing.")

col1, _= st.columns(2)
with col1:   
    st.slider("Please move the slider to indicate your preference.", 1, 10, key= "risk_aversion")

submit = st.button("Submit", on_click= add_submission)

if st.session_state['submit']:
    st.success(f"Thank you for completing the Survey on {config['header']['survey_title']}!")
