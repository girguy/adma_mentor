from navigation import make_sidebar
import streamlit as st
from config import constant
from config.utils import load_dataset_from_blob
from config.utils import clean_df
from config.utils import adjust_the_sidebar_width
from config.utils import reduce_white_space_above_title
from config.utils import extract_unique_elements


# Function to display specific columns of the mentee DataFrame
def display_mentee_info(column_name):
    st.dataframe(mentee_df[[column_name]], hide_index=True, use_container_width=True)


# Set the Streamlit page configuration to a wide layout
st.set_page_config(layout="wide")

# Reduce the white space above the title
st.markdown(reduce_white_space_above_title(), unsafe_allow_html=True)

# Adjust the sidebar width
adjust_the_sidebar_width()

# Create the sidebar
make_sidebar()

# Display the page title
st.write("# 📚 Mentee dataset")

# Load and clean the mentee dataset from the blob storage
mentee_df = load_dataset_from_blob(st.session_state.blob_service_client,
                                   st.session_state.container_name,
                                   st.session_state.mentee_blob_path)

mentee_df = clean_df(mentee_df)
mentee_df.columns = constant.MENTEE_DF_COLUMNS

# Combine first and last name to create a full name column
mentee_df['Full Name'] = mentee_df[constant.FIRST_NAME] + ' ' + mentee_df[constant.LAST_NAME]

# Extract unique mentee names and add an option for 'All'
list_people = extract_unique_elements(mentee_df['Full Name'])
list_people.append('All')

# Create a selectbox for choosing a mentee
mentee_name = st.selectbox("", list_people)

# Display the relevant data based on the selected mentee
if mentee_name != 'All':
    mentee_df = mentee_df[mentee_df['Full Name'] == mentee_name]

    # List of columns to display
    columns_to_display = [
        constant.EMAIL, constant.AGE, constant.NATIONALITY, constant.ORIGINE, constant.POSTAL_CODE,
        constant.TOWN, constant.MENTEE_QUESTION_1, constant.MENTEE_QUESTION_2, constant.MENTEE_QUESTION_3,
        constant.MENTEE_QUESTION_4, constant.MENTEE_QUESTION_5, constant.MENTEE_QUESTION_6, constant.MENTEE_QUESTION_7,
        constant.MENTEE_QUESTION_8, constant.MENTEE_QUESTION_9, constant.MENTEE_QUESTION_10, constant.MENTEE_QUESTION_11,
        constant.MENTEE_QUESTION_12, constant.MENTEE_QUESTION_13, constant.DATETIME
    ]

    # Display each column
    for column in columns_to_display:
        display_mentee_info(column)
else:
    # Drop unnecessary columns and display the entire DataFrame
    st.dataframe(mentee_df.drop([constant.SUBMITTED_DATETIME, constant.DATETIME, 'Full Name'], axis=1))
