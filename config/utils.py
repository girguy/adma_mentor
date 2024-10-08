import pandas as pd
import io
from azure.storage.blob import BlobServiceClient
import logging
from datetime import datetime
import streamlit as st
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_dataset_from_blob(blob_service_client: BlobServiceClient, container_name: str, blob_path: str) -> pd.DataFrame:
    """
    Loads a dataset from a blob storage and returns it as a pandas DataFrame.

    Args:
        blob_service_client (BlobServiceClient): An instance of the Azure BlobServiceClient.
        container_name (str): The name of the container where the blob is located.
        blob_path (str): The path to the blob within the container.

    Returns:
        pd.DataFrame: The dataset loaded from the blob.

    Raises:
        Exception: If there is an error during the blob download or data conversion.
    """
    try:
        logging.info(f"Loading dataset from blob: container={container_name}, path={blob_path}")
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)

        # Download the blob as bytes
        blob_data = blob_client.download_blob().readall()

        # Convert the bytes data to a StringIO object and then to a DataFrame
        csv_data = io.StringIO(blob_data.decode('utf-8'))
        df = pd.read_csv(csv_data, sep=';', header=0)

        logging.info("Dataset loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Failed to load dataset from blob: {e}")
        raise


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the given DataFrame by converting date columns, filtering for the most recent entries, and filling missing values.

    Args:
        df (pd.DataFrame): The input DataFrame to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame with the most recent entries for each email and missing values filled.

    Raises:
        Exception: If there is an error during the data cleaning process.
    """
    try:
        logging.info("Cleaning DataFrame.")
        # Convert 'submitted_datetime' to datetime format
        df['submitted_datetime'] = pd.to_datetime(df['submitted_datetime'], errors='coerce')

        # Drop rows with invalid datetime values
        df = df.dropna(subset=['submitted_datetime'])

        # Group by 'email' and get the index of the row with the maximum 'submitted_datetime' for each group
        idx = df.groupby('email')['submitted_datetime'].idxmax()

        # Use the indices to select the corresponding rows from the DataFrame
        most_recent_df = df.loc[idx].reset_index(drop=True)
        most_recent_df = most_recent_df.fillna(value='/')

        logging.info("DataFrame cleaned successfully.")
        return most_recent_df
    except Exception as e:
        logging.error(f"Failed to clean DataFrame: {e}")
        raise


def upload_blob_to_container(df: pd.DataFrame, blob_service_client: BlobServiceClient, container_name: str, blob_path: str) -> None:
    """
    Uploads a pandas DataFrame to a specified blob container as a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to be uploaded.
        blob_service_client (BlobServiceClient): An instance of the Azure BlobServiceClient.
        container_name (str): The name of the container to upload the blob to.
        blob_path (str): The path within the container where the blob will be stored.

    Returns:
        None

    Raises:
        Exception: If there is an error during the upload process.
    """
    try:
        logging.info(f"Uploading DataFrame to blob: container={container_name}, path={blob_path}")

        # Convert DataFrame to CSV in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, sep=';')
        csv_buffer.seek(0)  # Move the cursor to the start of the stream

        # Upload the CSV from the in-memory buffer
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
        blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)

        logging.info(f"DataFrame uploaded to container '{container_name}' with path '{blob_path}' successfully.")
    except Exception as e:
        logging.error(f"Failed to upload DataFrame to blob: {e}")
        raise


def get_date_time() -> str:
    """
    Get the current date and time as a formatted string.

    Returns:
        str: The current date and time formatted as "dd/mm/YYYY HH:MM:SS".
    """
    # Get the current date and time
    now = datetime.now()
    # Format the date and time as a string
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

def reduce_white_space_above_title() -> str:
    """
    Generate a CSS style block to reduce white space above the title in Streamlit.

    Returns:
        str: A string containing the CSS style block.
    """
    # Return the CSS style to reduce padding above the title
    return """<style> div.block-container {padding-top:0.4rem;} </style>"""


def adjust_the_sidebar_width():
    """
    Adjust the width of the Streamlit sidebar using CSS.

    This function modifies the sidebar width based on its expanded or collapsed state.
    """
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
        unsafe_allow_html=True
    )


def get_base64(bin_file: str) -> str:
    """
    Encode a binary file to a Base64 string.

    Args:
        bin_file (str): The path to the binary file.

    Returns:
        str: The Base64 encoded string of the file content.
    """
    # Open the file in binary read mode and read its content
    with open(bin_file, 'rb') as f:
        data = f.read()
    # Encode the binary data to a Base64 string
    return base64.b64encode(data).decode()


def set_background(png_file: str):
    """
    Set the background image of the Streamlit app.

    Args:
        png_file (str): The path to the PNG file to be used as background.
    """
    # Get the Base64 string of the PNG file
    bin_str = get_base64(png_file)
    # Define the CSS style to set the background image
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
    # Apply the CSS style to the Streamlit app
    st.markdown(page_bg_img, unsafe_allow_html=True)


def extract_unique_elements(df: pd.Series) -> list:
    """
    Extract unique elements from a pandas Series.

    Args:
        df (pd.Series): The input pandas Series.

    Returns:
        list: A list of unique elements from the Series.
    """
    # Get the unique elements from the Series and convert to a list
    list_of_names = pd.unique(df).tolist()
    return list_of_names
