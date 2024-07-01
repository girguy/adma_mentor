from navigation import make_sidebar
import streamlit as st
import pandas as pd
from datetime import datetime
import io


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


def get_date_time():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def upload_blob_to_container(df, blob_service_client, container_name, blob_path):
    # Convert DataFrame to CSV in memory
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, sep=';')
    csv_buffer.seek(0)  # Move the cursor to the start of the stream

    # Upload the CSV from the in-memory buffer
    blob_service_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
    blob_service_client.upload_blob(csv_buffer.getvalue(), overwrite=True)

    print(f"DataFrame uploaded to container 'bronze' with path {blob_path} successfully.")


def add_row_to_dataframe():
    row = pd.DataFrame({
        'First_Name': [st.session_state.first_name_mentor], 'Last_Name': [st.session_state.last_name_mentor],
        'Datetime': [st.session_state.date_time], 'SubmittedDatetime': [get_date_time()],
        'Age': [st.session_state.age_mentor], 'Email': [st.session_state.email_mentor],
        'Question_1': [st.session_state.question_1_mentor], 'Question_2': [st.session_state.question_2_mentor],
        'Question_3': [st.session_state.question_3_mentor], 'Question_4': [st.session_state.question_4_mentor],
        'Question_5': [st.session_state.question_5_mentor], 'Question_6': [st.session_state.question_6_mentor],
        'Question_7': [st.session_state.question_7_mentor], 'Question_8': [st.session_state.question_8_mentor],
        'Question_9': [st.session_state.question_9_mentor], 'Question_10': [st.session_state.question_10_mentor],
        'Question_11': [st.session_state.question_11_mentor], 'Question_12': [st.session_state.question_12_mentor],
        'Question_13': [st.session_state.question_13_mentor], 'Question_14': [st.session_state.question_14_mentor],
        'Question_15': [st.session_state.question_15_mentor], 'Remarque': [st.session_state.question_16_mentor],
        'Interviewer': [st.session_state.interviewer]
        })

    st.session_state.mentor_data = pd.concat([st.session_state.mentor_data, row])
    upload_blob_to_container(st.session_state.mentor_data,
                             st.session_state.blob_service_client,
                             st.session_state.container_name,
                             st.session_state.mentor_blob_path)

st.write(
"""
# 🕵️ Add a new mentor to the team

"""
)


make_sidebar()

mentor_form = st.form(key='mentor_form')
with mentor_form:

    cols = st.columns(4)
    with cols[0]:
        st.session_state.first_name_mentor = st.text_input('Prénom', key='First_Name')
    with cols[1]:
        st.session_state.last_name_mentor = st.text_input('Nom', key='Last_Name')
    with cols[2]:
        st.session_state.age_mentor = st.text_input('Age', key='Age')
    with cols[3]:
        st.session_state.email_mentor = st.text_input('Email', key='Email')

    st.session_state.question_1_mentor = st.text_area('Parcours académique', key='Question_1')
    st.session_state.question_2_mentor = st.text_area('Parcours professionel', key='Question_2')
    st.session_state.question_3_mentor = st.text_area('Quelles ont été vos influences ?', key='Question_3')
    st.session_state.question_4_mentor = st.text_area('Pourquoi souhaitez-vous devenir mentor ?', key='Question_4')
    st.session_state.question_5_mentor = st.text_area('Quelles connaissances et expériences spécifiques pensez-vous pouvoir amener en tant que mentor ?', key='Question_5')
    st.session_state.question_6_mentor = st.text_area('Quelles sont vos attentes vis-à-vis des mentorés tant d\'un point de vue de l\'attitude mais également des disponibilités ?', key='Question_6')
    st.session_state.question_7_mentor = st.text_area('Pouvez-vous nous donner un exemple concret dans lequel vous devez expliquer un problème complexe à un public non initié ?', key='Question_7')
    st.session_state.question_8_mentor = st.text_area('Quelle est votre définition de l\'empathie ?', key='Question_8')
    st.session_state.question_9_mentor = st.text_area('Comment gérez-vous les différences de style, de personnalité ou de valeurs entre vous et vos mentorés ? Pouvez-vous donner un exemple concret d\'une expérience vécue ?', key='Question_9')
    st.session_state.question_10_mentor = st.text_area('Comment établissez-vous des objectifs pour un programme de mentorat et Comment mesurez-vous le progrès et le succès de vos mentorés ?', key='Question_10')
    st.session_state.question_11_mentor = st.text_area('Comment définiriez-vous votre approche du mentorat ? Quels sont vos principes directeurs en tant que mentor ?', key='Question_11')
    st.session_state.question_12_mentor = st.text_area('Comment envisagez-vous l\'évolution de votre rôle de mentor à long terme ?', key='Question_12')
    st.session_state.question_13_mentor = st.text_area('Quelles sont vos attentes par rapport à cette expérience de mentorat ?', key='Question_13')
    st.session_state.question_14_mentor = st.text_area('Que diriez-vous si votre mentee vous demande un conseil d\'orientation dans le domaine de _____ (sélectionner un domaine à priori inconnu au mentor).', key='Question_14')
    st.session_state.question_15_mentor = st.text_area('Que feriez-vous dans une situation ou votre mentee n\'a appliqué aucun des conseils que vous lui avez recommandé ?', key='Question_15')
    st.session_state.question_16_mentor = st.text_area('Commentaires généraux', key='Question_16')

    submitted = st.form_submit_button()
    if submitted:
        add_row_to_dataframe()
