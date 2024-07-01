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
        'First_Name': [st.session_state.first_name_mentee], 'Last_Name': [st.session_state.last_name_mentee],
        'Datetime': [st.session_state.date_time], 'SubmittedDatetime': [get_date_time()],
        'Age': [str(int(st.session_state.age_mentee))], 'Email': [st.session_state.email_mentee],
        'Nationality': [st.session_state.nationality_mentee], 'Origine': [st.session_state.origine_mentee],
        'Postal_Code': [str(int(st.session_state.postal_code_mentee))], 'Town': [st.session_state.town_mentee],
        'Question_1': [st.session_state.question_1_mentee], 'Question_2': [st.session_state.question_2_mentee],
        'Question_3': [st.session_state.question_3_mentee], 'Question_4': [st.session_state.question_4_mentee],
        'Question_5': [st.session_state.question_5_mentee], 'Question_6': [st.session_state.question_6_mentee],
        'Question_7': [st.session_state.question_7_mentee], 'Question_8': [st.session_state.question_8_mentee],
        'Question_9': [st.session_state.question_9_mentee], 'Question_10': [st.session_state.question_10_mentee],
        'Question_11': [st.session_state.question_11_mentee], 'Question_12': [st.session_state.question_12_mentee],
        'Question_13': [st.session_state.question_13_mentee], 'Interviewer': [st.session_state.interviewer]
        })
    st.session_state.mentee_data = pd.concat([st.session_state.mentee_data, row])
    upload_blob_to_container(st.session_state.mentee_data,
                             st.session_state.blob_service_client,
                             st.session_state.container_name,
                             st.session_state.mentee_blob_path)

st.write(
"""
# 🕵️ Add a new mentee to ADMA

"""
)


make_sidebar()

mentee_form = st.form(key='mentee_form')
with mentee_form:

    cols = st.columns(4)
    with cols[0]:
        st.session_state.first_name_mentee = st.text_input('Prénom', key='First_Name')
    with cols[1]:
        st.session_state.last_name_mentee = st.text_input('Nom', key='Last_Name')
    with cols[2]:
        st.session_state.age_mentee = st.text_input('Age', key='Age')
    with cols[3]:
        st.session_state.email_mentee = st.text_input('Email', key='Email')

    cols = st.columns(4)
    with cols[0]:
        st.session_state.nationality_mentee = st.text_input('Nationalité', key='Nationality')
    with cols[1]:
        st.session_state.origine_mentee = st.text_input('Origine', key='Origine')
    with cols[2]:
        st.session_state.postal_code_mentee = st.text_input('Code Postal', key='Postal_Code')
    with cols[3]:
        st.session_state.town_mentee = st.text_input('Commune', key='Town')

    st.session_state.question_1_mentee = st.selectbox(
        "Quel est ton niveau d'études ?", ("Etudes secondaires", "Etudes supérieures", "Autres")
        )

    st.session_state.question_2_mentee = st.selectbox(
        "Dans quel type d'enseignement es-tu ?",
        ("Université", "Hautes-Ecoles", "Formation en alternance", "Enseignement général",
         "Enseignement technique de transition", "Enseignement technique de qualification",
         "Enseignement artistique", "Enseignement professionnel", "Promotion social", "Autre")
        )

    st.session_state.question_3_mentee = st.text_area("Dans quelle option es-tu ?", key='Question_3')
    st.session_state.question_4_mentee = st.text_area("Nom de l'établissement", key='Question_4')
    st.session_state.question_5_mentee = st.text_area("Comment se passe ton parcours scolaire et/ou carrière professionnelle ?", key='Question_5')

    st.session_state.question_6_mentee = st.selectbox(
        "Souhaiterais-tu te réorienter ?", ("Oui", "Non")
        )

    st.session_state.question_7_mentee = st.text_area("Si oui, pourquoi souhaiterais-tu te réorienter ?", key='Question_7')
    st.session_state.question_8_mentee = st.text_area("As-tu une idee de ce que tu voudrais faire après tes études ?", key='Question_8')

    st.session_state.question_9_mentee = st.multiselect(
        "A quelle fréquence aimerais-tu intéragir avec ton mentor ?",
        ["1 fois / par mois", "2 fois / par mois", "3 fois / par mois", "4 fois / par mois"]
        )

    st.session_state.question_10_mentee = st.multiselect(
        "Qu'attends-tu d'un mentor en termes de soutien et de guidance?",
        ["Choix d'etude", "Choix de metier", "Etude pour des cours",
         "Inspiration et motivation", "Development personnel"])

    st.session_state.question_11_mentee = st.text_area("Quels sont tes hobbys ?", key='Question_11')
    st.session_state.question_12_mentee = st.text_area("Quels sont tes 3 plus grands rêve?", key='Question_12')
    st.session_state.question_13_mentee = st.text_area("Commentaires généraux", key='Question_13')

    submitted = st.form_submit_button()
    if submitted:
        add_row_to_dataframe()
