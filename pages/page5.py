from navigation import make_sidebar
import streamlit as st
from config import constant
from config.utils import load_dataset_from_blob
from config.utils import upload_blob_to_container
from config.utils import clean_df
from config.utils import adjust_the_sidebar_width
from config.utils import reduce_white_space_above_title


# Function to handle data editing and uploading
def handle_data_editing(df_key: str, blob_path: str, df_columns_1: list, df_columns_2: list):
    """
    Load, clean, edit, and upload the dataset for mentors or mentees.

    Args:
        df_key (str): The session state key for the DataFrame.
        blob_path (str): The blob path to load and upload the dataset.
        df_columns_1 (list): The list of column names for the DataFrame.
        df_columns_2 (list): The list of column names for the DataFrame.
    """
    df = load_dataset_from_blob(
        st.session_state.blob_service_client,
        st.session_state.container_name,
        blob_path
        )
    df = clean_df(df)
    df.columns = df_columns_1
    #if df_key not in st.session_state:
    st.session_state[df_key] = df

    edited_df = st.data_editor(st.session_state[df_key], use_container_width=True, hide_index=True)

    if not edited_df.equals(st.session_state[df_key]):
        print('updated')
        edited_df.columns = df_columns_2
        upload_blob_to_container(
            edited_df,
            st.session_state.blob_service_client,
            st.session_state.container_name,
            blob_path
        )
        #st.session_state[df_key] = edited_df
        st.session_state[df_key] = ''
        st.rerun()


# Set the Streamlit page configuration
st.set_page_config(layout="wide")

st.markdown(reduce_white_space_above_title(), unsafe_allow_html=True)

# Adjust the sidebar width
adjust_the_sidebar_width()

# Display the page title
st.write("# 🕵️ Update data")

make_sidebar()

# User selects whether to update mentor or mentee information
choice_made = st.selectbox(
    "Do you want to update a mentor information or a mentee information?",
    ("Mentee", "Mentor")
)
st.write("You selected:", choice_made)

# Handle mentor or mentee data based on user choice
if choice_made == 'Mentor':
    handle_data_editing('df_mentor', st.session_state.mentor_blob_path, constant.MENTOR_DF_COLUMNS_1, constant.MENTOR_DF_COLUMNS_2)
else:
    handle_data_editing('df_mentee', st.session_state.mentee_blob_path, constant.MENTEE_DF_COLUMNS_1, constant.MENTEE_DF_COLUMNS_2)
