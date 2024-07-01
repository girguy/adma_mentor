from navigation import make_sidebar
import streamlit as st
import base64
import pandas as pd
import io
from config import constant

st.set_page_config(layout="wide")

# size of the white space above the title
reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0.4rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

# size of the side bar

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def load_dataset_from_blob(blob_service_client, container_name, blob_path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)

    # Download the blob as bytes
    blob_data = blob_client.download_blob().readall()

    # Convert the bytes data to a StringIO object and then to a DataFrame
    csv_data = io.StringIO(blob_data.decode('utf-8'))
    df = pd.read_csv(csv_data, sep=';', header=0)

    return df


def clean_df(df):
    # Convert 'SubmittedDatetime' to datetime format
    df['SubmittedDatetime'] = pd.to_datetime(df['SubmittedDatetime'], dayfirst=True)
    # Group by 'id' and get the index of the row with the maximum 'time' for each group
    idx = df.groupby('Email')['SubmittedDatetime'].idxmax()
    # Use the indices to select the corresponding rows from the DataFrame
    most_recent_df = df.loc[idx].reset_index(drop=True)
    most_recent_df = most_recent_df.fillna(value='/')
    most_recent_df['Age'] = most_recent_df['Age'].apply(str)
    most_recent_df['Postal_Code'] = most_recent_df['Postal_Code'].apply(str)
    return most_recent_df


def extract_list_mentees(df):
    list_of_names = pd.unique(df).tolist()
    return list_of_names

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: 100vw 100vh;
    background-position: center;
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


make_sidebar()

st.write(
"""
# 📚 Mentor dataset
"""
)

mentee_df = load_dataset_from_blob(st.session_state.blob_service_client,
                                   st.session_state.container_name,
                                   st.session_state.mentee_blob_path)

mentee_df = clean_df(mentee_df)
mentee_df.columns = constant.MENTEE_DF_COLUMNS

mentee_df['Full Name'] = mentee_df[constant.FIRST_NAME] + ' ' + mentee_df[constant.LAST_NAME]
list_people = extract_list_mentees(mentee_df['Full Name'])
list_people.append('All')

mentee_name = st.selectbox("Liste des mentees", list_people)

if mentee_name != 'All':
    mentee_df = mentee_df[mentee_df['Full Name'] == mentee_name]

    st.dataframe(mentee_df[[constant.EMAIL]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.AGE]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.NATIONALITY]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.ORIGINE]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.POSTAL_CODE]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.TOWN]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_1]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_2]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_3]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_4]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_5]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_6]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_7]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_8]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_9]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_10]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_11]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_12]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.MENTEE_QUESTION_13]], hide_index=True, use_container_width=True)
    st.dataframe(mentee_df[[constant.DATETIME]], hide_index=True, use_container_width=True)
else:
    st.dataframe(mentee_df.drop([constant.SUBMITTED_DATETIME, constant.DATETIME, 'Full Name'], axis=1))
