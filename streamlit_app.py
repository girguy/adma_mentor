import streamlit as st
from time import sleep
from navigation import make_sidebar
from datetime import datetime
import pandas as pd
import re
import io
import base64
import hashlib
import json
from azure.storage.blob import BlobServiceClient


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

@st.cache_data
def get_users_passwords(file_name):
    # Load JSON data from file
    with open(file_name, 'r') as file:
        data = json.load(file)
    # Transform users list into a dictionary
    return {user['username']: user['password_hash'] for user in data['users']}

@st.cache_data
def hash_password(username, password):
    password_bytes = f"{username}{password}".encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
@st.cache_data
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


set_background('pictures/adma_background.jpg')


def create_blob_client_with_connection_string(connection_string):
    connection_string = re.sub(r'%2B', '+', connection_string)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client


def load_dataset_from_blob(blob_service_client, container_name, blob_path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)

    # Download the blob as bytes
    blob_data = blob_client.download_blob().readall()

    # Convert the bytes data to a StringIO object and then to a DataFrame
    csv_data = io.StringIO(blob_data.decode('utf-8'))
    df = pd.read_csv(csv_data, sep=';', header=0)

    return df


def get_date_time():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


make_sidebar()

st.session_state.container_name = 'bronze/'

folder_name = 'adma-mentor'
mentor_blob_name = 'adma_mentor_test.csv'
st.session_state.mentor_blob_path = f"{folder_name}/{mentor_blob_name}"

folder_name = 'adma-mentee'
mentee_blob_name = 'adma_mentee_test.csv'
st.session_state.mentee_blob_path = f"{folder_name}/{mentee_blob_name}"


# Create a blob client
connection_string = st.secrets["CONNECTION_STRING"]
st.session_state.blob_service_client = create_blob_client_with_connection_string(connection_string)
print("Successfully created blob client\n")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

users_dict = get_users_passwords('users.json')

if st.button("Log in", type="primary"):
    if hash_password(username, password) == users_dict[username]:
        st.session_state.interviewer = username
        st.session_state.logged_in = True
        st.session_state.date_time = get_date_time()

        st.session_state.mentor_data = load_dataset_from_blob(
            st.session_state.blob_service_client,
            st.session_state.container_name,
            st.session_state.mentor_blob_path
            )

        st.session_state.mentee_data = load_dataset_from_blob(
            st.session_state.blob_service_client,
            st.session_state.container_name,
            st.session_state.mentee_blob_path
            )

        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/page1.py")
    else:
        st.error("Incorrect username or password")
