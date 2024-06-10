from navigation import make_sidebar
import streamlit as st
import base64
import pandas as pd
import io

q1 = 'Parcours académique'
q2 = 'Parcours professionel'
q3 = 'Quelles ont été vos influences ?'
q4 = 'Pourquoi souhaitez-vous devenir mentor ?'
q5 = 'Quelles connaissances et expériences spécifiques pensez-vous pouvoir amener en tant que mentor ?'
q6 = 'Quelles sont vos attentes vis-à-vis des mentorés tant d\'un point de vue de l\'attitude mais également des disponibilités ?'
q7 = 'Pouvez-vous nous donner un exemple concret dans lequel vous devez expliquer un problème complexe à un public non initié ?'
q8 = 'Quelle est votre définition de l\'empathie ?'
q9 = 'Comment gérez-vous les différences de style, de personnalité ou de valeurs entre vous et vos mentorés ? Pouvez-vous donner un exemple concret d\'une expérience vécue ?'
q10 = 'Comment établissez-vous des objectifs pour un programme de mentorat et Comment mesurez-vous le progrès et le succès de vos mentorés ?'
q11 = 'Comment définiriez-vous votre approche du mentorat ? Quels sont vos principes directeurs en tant que mentor ?'
q12 = 'Comment envisagez-vous l\'évolution de votre rôle de mentor à long terme ?', 'Quelles sont vos attentes par rapport à cette expérience de mentorat ?'
q13 = 'Que diriez-vous si votre mentee vous demande un conseil d\'orientation dans le domaine de _____ (sélectionner un domaine à priori inconnu au mentor).'
q14 = 'Que feriez-vous dans une situation ou votre mentee n\'a appliqué aucun des conseils que vous lui avez recommandé ?'
q15 = 'Commentaires généraux'

columns = [
    'First Name', 'Last Name', 'Age', 'Email', 'Datetime', 'SubmittedDatetime',
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15,
    'Remarque', 'Interviewer'
    ]


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
    idx = df.groupby('Last_Name')['SubmittedDatetime'].idxmax()
    # Use the indices to select the corresponding rows from the DataFrame
    most_recent_df = df.loc[idx].reset_index(drop=True)
    most_recent_df = most_recent_df.fillna(value='/')
    return most_recent_df


def extract_list_mentors(df):
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

mentor_df = load_dataset_from_blob(st.session_state.blob_service_client,
                                   st.session_state.container_name,
                                   st.session_state.blob_path)

mentor_df = clean_df(mentor_df)
mentor_df.columns = columns

mentor_df['Full Name'] = mentor_df['First Name'] + ' ' + mentor_df['Last Name']
list_people = extract_list_mentors(mentor_df['Full Name'])
list_people.append('All')

mentor_name = st.selectbox("Liste des mentors", list_people)

if mentor_name != 'All':
    mentor_df = mentor_df[mentor_df['Full Name'] == mentor_name]

st.dataframe(mentor_df.drop(['SubmittedDatetime', 'Datetime', 'Full Name'], axis=1))

st.dataframe(mentor_df[['Email']], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[['Age']], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q1]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q2]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q3]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q4]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q5]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q6]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q7]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q8]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q9]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q10]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q11]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q12]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q13]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q14]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[[q15]], hide_index=True, use_container_width=True)
st.dataframe(mentor_df[['Datetime']], hide_index=True, use_container_width=True)
