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
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
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
        'first_name': [st.session_state.first_name_mentee], 'last_name': [st.session_state.last_name_mentee],
        'datetime': [st.session_state.date_time], 'submitted_datetime': [get_date_time()],
        'age': [str(int(st.session_state.age_mentee))], 'email': [st.session_state.email_mentee],
        'nationality': [st.session_state.nationality_mentee], 'origine': [st.session_state.origine_mentee],
        'postal_code': [str(int(st.session_state.postal_code_mentee))], 'town': [st.session_state.town_mentee],
        'question_1': [st.session_state.question_1_mentee], 'question_2': [st.session_state.question_2_mentee],
        'question_3': [st.session_state.question_3_mentee], 'question_4': [st.session_state.question_4_mentee],
        'question_5': [st.session_state.question_5_mentee], 'question_6': [st.session_state.question_6_mentee],
        'question_7': [st.session_state.question_7_mentee], 'question_8': [st.session_state.question_8_mentee],
        'question_9': [st.session_state.question_9_mentee], 'question_10': [st.session_state.question_10_mentee],
        'question_11': [st.session_state.question_11_mentee], 'question_12': [st.session_state.question_12_mentee],
        'remarque': [st.session_state.remarque_mentee], 'interviewer': [st.session_state.interviewer]
        })
    
    if set(row.columns) == set(st.session_state.mentee_data.columns):
        st.session_state.mentee_data = pd.concat([st.session_state.mentee_data, row])
        
        upload_blob_to_container(st.session_state.mentee_data,
                                st.session_state.blob_service_client,
                                st.session_state.container_name,
                                st.session_state.mentee_blob_path)
        
    else:
        print(row.columns)
        print(st.session_state.mentee_data.columns)
        st.text("Columns are not the same. Can not save this mentee interview")
        print("columns are not the same. Can not save this mentee interview")

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
        st.session_state.first_name_mentee = st.text_input('Prénom', key='first_name')
    with cols[1]:
        st.session_state.last_name_mentee = st.text_input('Nom', key='last_name')
    with cols[2]:
        st.session_state.age_mentee = st.text_input('Age', key='age')
    with cols[3]:
        st.session_state.email_mentee = st.text_input('Email', key='email')

    cols = st.columns(4)
    with cols[0]:
        st.session_state.nationality_mentee = st.text_input('Nationalité', key='nationality')
    with cols[1]:
        st.session_state.origine_mentee = st.text_input('Origine', key='origine')
    with cols[2]:
        st.session_state.postal_code_mentee = st.text_input('Code Postal', key='postal_code')
    with cols[3]:
        st.session_state.town_mentee = st.text_input('Commune', key='town')

    st.session_state.question_1_mentee = st.selectbox(
        "Quel est ton niveau d'études ?", ("Etudes secondaires", "Etudes supérieures", "Autres")
        )

    st.session_state.question_2_mentee = st.selectbox(
        "Dans quel type d'enseignement es-tu ?",
        ("Université", "Hautes-Ecoles", "Formation en alternance", "Enseignement général",
         "Enseignement technique de transition", "Enseignement technique de qualification",
         "Enseignement artistique", "Enseignement professionnel", "Promotion social", "Autre")
        )

    st.session_state.question_3_mentee = st.text_area("Dans quelle option es-tu ?", key='question_3')
    st.session_state.question_4_mentee = st.text_area("Nom de l'établissement", key='question_4')
    st.session_state.question_5_mentee = st.text_area("Comment se passe ton parcours scolaire et/ou carrière professionnelle ?", key='question_5')

    st.session_state.question_6_mentee = st.selectbox(
        "Souhaiterais-tu te réorienter ?", ("Oui", "Non")
        )

    st.session_state.question_7_mentee = st.text_area("Si oui, pourquoi souhaiterais-tu te réorienter ?", key='question_7')
    st.session_state.question_8_mentee = st.text_area("As-tu une idee de ce que tu voudrais faire après tes études ?", key='question_8')

    st.session_state.question_9_mentee = st.selectbox(
        "A quelle fréquence aimerais-tu intéragir avec ton mentor ?",
        ("1 fois / par mois", "2 fois / par mois", "3 fois / par mois", "4 fois / par mois")
        )

    st.session_state.question_10_mentee = st.multiselect(
        "Qu'attends-tu d'un mentor en termes de soutien et de guidance?",
        ["Choix d'etude", "Choix de metier", "Etude pour des cours",
         "Inspiration et motivation", "Development personnel"])

    st.session_state.question_11_mentee = st.text_area("Quels sont tes hobbys ?", key='question_11')
    st.session_state.question_12_mentee = st.text_area("Quels sont tes 3 plus grands rêve?", key='question_12')
    st.session_state.remarque_mentee = st.text_area("Remarque", key='remarque')

    submitted = st.form_submit_button()
    if submitted:
        add_row_to_dataframe()
