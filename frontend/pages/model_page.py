import pandas as pd
import streamlit as st


def create_model_page():
    age_group = st.selectbox(
        label="age_group",
        options=("")
    )
    apr_severity_of_illness_code = ""
    covid_hosp = ""
    gender = ""
    race = ""
    ethnicity = ""
    type_of_admission = ""
    payment_typology = ""
    patient_disposition = ""
    apr_drg_code = ""
    apr_mdc_code = ""

    x = pd.DataFrame(columns=['age_group', 'apr_severity_of_illness_code', 'covid_hosp',
       'covid_risk_factor', 'gender_M', 'race_Multi-racial', 'race_Other Race',
       'race_White', 'ethnicity_Not Span/Hispanic',
       'ethnicity_Spanish/Hispanic', 'ethnicity_Unknown',
       'type_of_admission_Trauma', 'type_of_admission_Urgent',
       'payment_typology_1_Federal/State/Local/VA',
       'payment_typology_1_Medicaid', 'payment_typology_1_Medicare',
       'patient_disposition_Cancer Center or Children\'s Hospital',
       'patient_disposition_Court/Law Enforcement',
       'patient_disposition_Critical Access Hospital',
       'patient_disposition_Expired',
       'patient_disposition_Facility w/ Custodial/Supportive Care',
       'patient_disposition_Home or Self Care',
       'patient_disposition_Home w/ Home Health Services',
       'patient_disposition_Hospice - Home',
       'patient_disposition_Hospice - Medical Facility',
       'patient_disposition_Inpatient Rehabilitation Facility',
       'patient_disposition_Left Against Medical Advice',
       'patient_disposition_Medicaid Cert Nursing Facility',
       'patient_disposition_Medicare Cert Long Term Care Hospital',
       'patient_disposition_Psychiatric Hospital or Unit of Hosp',
       'patient_disposition_Short-term Hospital',
       'patient_disposition_Skilled Nursing Home', 'apr_drg_code_165',
       'apr_drg_code_166', 'apr_drg_code_167', 'apr_drg_code_169',
       'apr_drg_code_171', 'apr_drg_code_173', 'apr_drg_code_175',
       'apr_drg_code_180', 'apr_drg_code_191', 'apr_drg_code_197',
       'apr_drg_code_24', 'apr_drg_code_26', 'apr_drg_code_305',
       'apr_drg_code_309', 'apr_drg_code_310', 'apr_drg_code_312',
       'apr_drg_code_313', 'apr_drg_code_314', 'apr_drg_code_316',
       'apr_drg_code_317', 'apr_drg_code_320', 'apr_drg_code_321',
       'apr_drg_code_344', 'apr_drg_code_351', 'apr_drg_code_361',
       'apr_drg_code_364', 'apr_drg_code_380', 'apr_drg_code_4',
       'apr_drg_code_405', 'apr_drg_code_420', 'apr_drg_code_424',
       'apr_drg_code_440', 'apr_drg_code_444', 'apr_drg_code_447',
       'apr_drg_code_468', 'apr_drg_code_48', 'apr_drg_code_5',
       'apr_drg_code_6', 'apr_drg_code_710', 'apr_drg_code_73',
       'apr_drg_code_82', 'apr_drg_code_890', 'apr_drg_code_892',
       'apr_drg_code_894', 'apr_drg_code_950', 'apr_drg_code_951',
       'apr_drg_code_952', 'apr_mdc_code_10', 'apr_mdc_code_11',
       'apr_mdc_code_18', 'apr_mdc_code_2', 'apr_mdc_code_24',
       'apr_mdc_code_5', 'apr_mdc_code_8', 'apr_mdc_code_9'])

