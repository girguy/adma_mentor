from navigation import make_sidebar
import streamlit as st
import pandas as pd
from config import constant
from config.utils import upload_blob_to_container
from config.utils import adjust_the_sidebar_width
from config.utils import reduce_white_space_above_title
from config.utils import get_date_time


def add_row_to_dataframe():
    row = pd.DataFrame({
        constant.FIRST_NAME: [st.session_state.first_name_mentor],
        constant.LAST_NAME: [st.session_state.last_name_mentor],
        constant.DATETIME: [st.session_state.date_time],
        constant.SUBMITTED_DATETIME: [get_date_time()],
        constant.AGE: [st.session_state.age_mentor],
        constant.EMAIL: [st.session_state.email_mentor],
        constant.MENTOR_QUESTION_1: [st.session_state.question_1_mentor],
        constant.MENTOR_QUESTION_2: [st.session_state.question_2_mentor],
        constant.MENTOR_QUESTION_3: [st.session_state.question_3_mentor],
        constant.MENTOR_QUESTION_4: [st.session_state.question_4_mentor],
        constant.MENTOR_QUESTION_5: [st.session_state.question_5_mentor],
        constant.MENTOR_QUESTION_6: [st.session_state.question_6_mentor],
        constant.MENTOR_QUESTION_7: [st.session_state.question_7_mentor],
        constant.MENTOR_QUESTION_8: [st.session_state.question_8_mentor],
        constant.MENTOR_QUESTION_9: [st.session_state.question_9_mentor],
        constant.MENTOR_QUESTION_10: [st.session_state.question_10_mentor],
        constant.MENTOR_QUESTION_11: [st.session_state.question_11_mentor],
        constant.MENTOR_QUESTION_12: [st.session_state.question_12_mentor],
        constant.MENTOR_QUESTION_13: [st.session_state.question_13_mentor],
        constant.MENTOR_QUESTION_14: [st.session_state.question_14_mentor],
        constant.MENTOR_QUESTION_15: [st.session_state.question_15_mentor],
        constant.REMARQUE: [st.session_state.question_16_mentor],
        constant.INTERVIEWER: [st.session_state.interviewer]
        })

    st.session_state.mentor_data = pd.concat([st.session_state.mentor_data, row])
    upload_blob_to_container(st.session_state.mentor_data,
                             st.session_state.blob_service_client,
                             st.session_state.container_name,
                             st.session_state.mentor_blob_path)

# Set the Streamlit page configuration
st.set_page_config(layout="wide")

st.markdown(reduce_white_space_above_title(), unsafe_allow_html=True)

# Adjust the sidebar width
adjust_the_sidebar_width()

st.write("""# 🕵️ Add a new mentor to the team""")

make_sidebar()

mentor_form = st.form(key='mentor_form')
with mentor_form:

    cols = st.columns(4)
    with cols[0]:
        st.session_state.first_name_mentor = st.text_input('Prénom')
    with cols[1]:
        st.session_state.last_name_mentor = st.text_input('Nom')
    with cols[2]:
        st.session_state.age_mentor = st.text_input('Age')
    with cols[3]:
        st.session_state.email_mentor = st.text_input('Email')

    st.session_state.question_1_mentor = st.text_area(constant.MENTOR_QUESTION_1)
    st.session_state.question_2_mentor = st.text_area(constant.MENTOR_QUESTION_2)
    st.session_state.question_3_mentor = st.text_area(constant.MENTOR_QUESTION_3)
    st.session_state.question_4_mentor = st.text_area(constant.MENTOR_QUESTION_4)
    st.session_state.question_5_mentor = st.text_area(constant.MENTOR_QUESTION_5)
    st.session_state.question_6_mentor = st.text_area(constant.MENTOR_QUESTION_6)
    st.session_state.question_7_mentor = st.text_area(constant.MENTOR_QUESTION_7)
    st.session_state.question_8_mentor = st.text_area(constant.MENTOR_QUESTION_8)
    st.session_state.question_9_mentor = st.text_area(constant.MENTOR_QUESTION_9)
    st.session_state.question_10_mentor = st.text_area(constant.MENTOR_QUESTION_10)
    st.session_state.question_11_mentor = st.text_area(constant.MENTOR_QUESTION_11)
    st.session_state.question_12_mentor = st.text_area(constant.MENTOR_QUESTION_12)
    st.session_state.question_13_mentor = st.text_area(constant.MENTOR_QUESTION_13)
    st.session_state.question_14_mentor = st.text_area(constant.MENTOR_QUESTION_14)
    st.session_state.question_15_mentor = st.text_area(constant.MENTOR_QUESTION_15)

    submitted = st.form_submit_button()
    if submitted:
        add_row_to_dataframe()
