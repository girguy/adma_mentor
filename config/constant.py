FIRST_NAME = 'First Name'
LAST_NAME = 'Last Name'
DATETIME = 'Datetime'
SUBMITTED_DATETIME = 'SubmittedDatetime'
AGE = 'Age'
EMAIL = 'Email'
INTERVIEWER = 'Interviewer'
REMARQUE = 'Remarque'

NATIONALITY = 'Nationality'
ORIGINE = 'Origine'
POSTAL_CODE = 'Postal_Code'
TOWN = 'Town'

MENTEE_QUESTION_1 = "Quel est ton niveau d'études ?"
MENTEE_QUESTION_2 = "Dans quel type d'enseignement es-tu ?"
MENTEE_QUESTION_3 = "Dans quelle option es-tu ?"
MENTEE_QUESTION_4 = "Nom de l'établissement"
MENTEE_QUESTION_5 = "Comment se passe ton parcours scolaire et/ou carrière professionnelle ?"
MENTEE_QUESTION_6 = "Souhaiterais-tu te réorienter ?"
MENTEE_QUESTION_7 = "Si oui, pourquoi souhaiterais-tu te réorienter ?"
MENTEE_QUESTION_8 = "As-tu une idee de ce que tu voudrais faire après tes études ?"
MENTEE_QUESTION_9 = "A quelle fréquence aimerais-tu intéragir avec ton mentor ?"
MENTEE_QUESTION_10 = "Qu'attends-tu d'un mentor en termes de soutien et de guidance?"
MENTEE_QUESTION_11 = "Quels sont tes hobbys ?"
MENTEE_QUESTION_12 = "Quels sont tes 3 plus grands rêve?"
MENTEE_QUESTION_13 = 'Commentaires généraux'

MENTEE_DF_COLUMNS = [
    FIRST_NAME, LAST_NAME, DATETIME, SUBMITTED_DATETIME, AGE, EMAIL, NATIONALITY,
    ORIGINE, POSTAL_CODE, TOWN, MENTEE_QUESTION_1, MENTEE_QUESTION_2, MENTEE_QUESTION_3, MENTEE_QUESTION_4,
    MENTEE_QUESTION_5, MENTEE_QUESTION_6, MENTEE_QUESTION_7, MENTEE_QUESTION_8, MENTEE_QUESTION_9, MENTEE_QUESTION_10, MENTEE_QUESTION_11,
    MENTEE_QUESTION_12, MENTEE_QUESTION_13, INTERVIEWER
    ]


MENTOR_QUESTION_1 = 'Parcours académique'
MENTOR_QUESTION_2 = 'Parcours professionel'
MENTOR_QUESTION_3 = 'Quelles ont été vos influences ?'
MENTOR_QUESTION_4 = 'Pourquoi souhaitez-vous devenir mentor ?'
MENTOR_QUESTION_5 = 'Quelles connaissances et expériences spécifiques pensez-vous pouvoir amener en tant que mentor ?'
MENTOR_QUESTION_6 = 'Quelles sont vos attentes vis-à-vis des mentorés tant d\'un point de vue de l\'attitude mais également des disponibilités ?'
MENTOR_QUESTION_7 = 'Pouvez-vous nous donner un exemple concret dans lequel vous devez expliquer un problème complexe à un public non initié ?'
MENTOR_QUESTION_8 = 'Quelle est votre définition de l\'empathie ?'
MENTOR_QUESTION_9 = 'Comment gérez-vous les différences de style, de personnalité ou de valeurs entre vous et vos mentorés ? Pouvez-vous donner un exemple concret d\'une expérience vécue ?'
MENTOR_QUESTION_10 = 'Comment établissez-vous des objectifs pour un programme de mentorat et Comment mesurez-vous le progrès et le succès de vos mentorés ?'
MENTOR_QUESTION_11 = 'Comment définiriez-vous votre approche du mentorat ? Quels sont vos principes directeurs en tant que mentor ?'
MENTOR_QUESTION_12 = 'Comment envisagez-vous l\'évolution de votre rôle de mentor à long terme ? Quelles sont vos attentes par rapport à cette expérience de mentorat ?'
MENTOR_QUESTION_13 = 'Que diriez-vous si votre mentee vous demande un conseil d\'orientation dans le domaine de _____ (sélectionner un domaine à priori inconnu au mentor).'
MENTOR_QUESTION_14 = 'Que feriez-vous dans une situation ou votre mentee n\'a appliqué aucun des conseils que vous lui avez recommandé ?'
MENTOR_QUESTION_15 = 'Commentaires généraux'

MENTOR_DF_COLUMNS = [
    FIRST_NAME, LAST_NAME, AGE, EMAIL, DATETIME, SUBMITTED_DATETIME,
    MENTOR_QUESTION_1, MENTOR_QUESTION_2, MENTOR_QUESTION_3, MENTOR_QUESTION_4,
    MENTOR_QUESTION_5, MENTOR_QUESTION_6, MENTOR_QUESTION_7, MENTOR_QUESTION_8,
    MENTOR_QUESTION_9, MENTOR_QUESTION_10, MENTOR_QUESTION_11, MENTOR_QUESTION_12,
    MENTOR_QUESTION_13, MENTOR_QUESTION_14, MENTOR_QUESTION_15,
    REMARQUE, INTERVIEWER
    ]
