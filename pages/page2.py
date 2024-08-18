from navigation import make_sidebar
import streamlit as st
from config import constant
from config.utils import load_dataset_from_blob
from config.utils import clean_df
from config.utils import adjust_the_sidebar_width
from config.utils import reduce_white_space_above_title
from config.utils import extract_unique_elements


# Function to display specific columns of the mentor DataFrame
def display_mentor_info(column_name):
    st.dataframe(mentor_df[[column_name]], hide_index=True, use_container_width=True)


# Set the Streamlit page configuration to a wide layout
st.set_page_config(layout="wide")

# Reduce the white space above the title
st.markdown(reduce_white_space_above_title(), unsafe_allow_html=True)

# Adjust the sidebar width
adjust_the_sidebar_width()

# Create the sidebar
make_sidebar()

# Display the page title
st.write("# 📚 Mentor dataset")

# Load and clean the mentor dataset from the blob storage
mentor_df = load_dataset_from_blob(st.session_state.blob_service_client,
                                   st.session_state.container_name,
                                   st.session_state.mentor_blob_path)

mentor_df = clean_df(mentor_df)
mentor_df.columns = constant.MENTOR_DF_COLUMNS_1

# Combine first and last name to create a full name column
mentor_df['Full Name'] = mentor_df[constant.FIRST_NAME] + ' ' + mentor_df[constant.LAST_NAME]

# Extract unique mentor names and add an option for 'All'
list_people = extract_unique_elements(mentor_df['Full Name'])
list_people.append('All')

# Create a selectbox for choosing a mentor
mentor_name = st.selectbox("", list_people)

# Display the relevant data based on the selected mentor
if mentor_name != 'All':
    mentor_df = mentor_df[mentor_df['Full Name'] == mentor_name]

    # List of columns to display
    columns_to_display = [
        constant.EMAIL, constant.AGE, constant.DOMAIN, constant.RESIDENCE, constant.PROFESSION,
        constant.UNIVERSITY, constant.MENTOR_QUESTION_1, constant.MENTOR_QUESTION_2,
        constant.MENTOR_QUESTION_3, constant.MENTOR_QUESTION_4, constant.MENTOR_QUESTION_5,
        constant.MENTOR_QUESTION_6, constant.MENTOR_QUESTION_7, constant.MENTOR_QUESTION_8,
        constant.MENTOR_QUESTION_9, constant.MENTOR_QUESTION_10, constant.MENTOR_QUESTION_11,
        constant.MENTOR_QUESTION_12, constant.MENTOR_QUESTION_13, constant.MENTOR_QUESTION_14,
        constant.REMARQUE, constant.DATETIME
    ]

    # Display each column
    for column in columns_to_display:
        display_mentor_info(column)
else:
    # Drop unnecessary columns and display the entire DataFrame
    st.dataframe(mentor_df.drop([constant.SUBMITTED_DATETIME, constant.DATETIME, 'Full Name'], axis=1))
