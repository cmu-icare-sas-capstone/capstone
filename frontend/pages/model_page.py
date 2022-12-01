import pandas as pd
import streamlit as st
from bean.GlobalState import state
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pypika import Query, Table, Field


repo = state.get("repo")
meta_data_repo = state.get("meta_data_repo")


def create_model_page():
    dataset = st.selectbox(
        label="dataset",
        options=meta_data_repo.get_all_tables()
    )
    model = st.selectbox(
        label="Model",
        options=("ridge", "XGBoost")
    )

    with st.expander("Model Input"):
        age_group = st.selectbox(
            label="age_group",
            options=("0-17", "18-44", "45-64", "65-74", "75+")
        )
        enc_age_dict = {'0-17': 0, '18-44': 1, '45-64': 2, '65-74': 3, '75+': 4}
        age_group = enc_age_dict[age_group]

        apr_severity_of_illness_code = st.selectbox(
            label="apr_severity_of_illness_code",
            options=(1, 2, 3, 4)
        )

        covid_hosp = st.selectbox(
            label="covid_hosp",
            options=(0, 1)
        )
        gender = st.selectbox(
            label="gender",
            options=("M", "F")
        )
        gender_dict = {"M": 1, "F": 0}
        gender_M = gender_dict[gender]

        race = st.selectbox(
            label="race",
            options=("White", "Black", "Multi-racial", "Other Race")
        )
        ethnicity = st.selectbox(
            label="ethnicity",
            options=("Spanish/Hispanic", "Not Span/Hispanic")
        )
        type_of_admission = st.selectbox(
            label="type_of_admission",
            options=("Trauma", "Urgent")
        )
        payment_typology = st.selectbox(
            label="payment_typology",
            options=("Federal/State/Local/VA", "Medicaid", "Medicare")
        )

        tbl = Table(dataset)
        q = Query\
            .from_(tbl)\
            .select("patient_disposition")\
            .where(
                tbl.ccs_diagnosis_description.isin(
                    ['Diabetes mellitus without complication', 'Diabetes mellitus with complications']))\
            .where(tbl.patient_disposition != 'Another Type Not Listed')\
            .distinct()

        patient_disposition = st.selectbox(
            label="patient_disposition",
            options=repo.get_values_of_one_column_by_query(q.get_sql())
        )

        apr_drg_description = st.selectbox(
            label="apr_drg_description",
            options=repo.get_values_of_one_column_by_filters(
                dataset,
                "apr_drg_description",
                {
                    "ccs_diagnosis_description":
                        ['Diabetes mellitus without complication', 'Diabetes mellitus with complications']
                }
            )
        )
        apr_drg_code = repo.get_values_of_one_column_by_filters(
            dataset,
            "apr_drg_code",
            {
                "apr_drg_description": [apr_drg_description]
            }
        )[0]

        apr_mdc_description = st.selectbox(
            label="apr_mdc_description",
            options=repo.get_values_of_one_column_by_filters(
                dataset,
                "apr_mdc_description",
                {
                    "ccs_diagnosis_description":
                        ['Diabetes mellitus without complication', 'Diabetes mellitus with complications']
                }
            )
        )
        apr_mdc_code = repo.get_values_of_one_column_by_filters(
            dataset,
            "apr_mdc_code",
            {
                "apr_mdc_description":
                    [apr_mdc_description]
            }
        )[0]

    columns = ['age_group', 'apr_severity_of_illness_code', 'covid_hosp',
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
       'apr_mdc_code_5', 'apr_mdc_code_8', 'apr_mdc_code_9']
    x = pd.DataFrame(columns=columns)

    x = x.append({
        "age_group": age_group,
        "apr_severity_of_illness_code": apr_severity_of_illness_code,
        "covid_hosp": covid_hosp,
        "covid_risk_factor": 1,
        "gender_M": gender_M,
        "race_"+race: 1,
        "ethnicity_"+ethnicity: 1,
        "type_of_admission_"+type_of_admission: 1,
        "payment_typology_1_"+payment_typology: 1,
        "patient_disposition_"+patient_disposition: 1,
        "apr_drg_code_"+str(apr_drg_code): 1,
        "apr_mdc_code_"+str(apr_mdc_code): 1
    }, ignore_index=True)
    x = x.fillna(0)

    if model == "ridge":
        with open("/Users/mtong/Documents/project/capstone/model/ridge.pkl", 'rb') as file:
            f = pickle.load(file)
    elif model == "XGBoost":
        with open("/Users/mtong/Documents/project/capstone/model/xgb_model.pkl", 'rb') as file:
            f = pickle.load(file)

    predict_value = f.predict(x)
    if predict_value < 0:
        predict_value = 0

    st.write("Estimated LOS: " + str(predict_value))

    with st.expander("Model Analysis"):
        if model == "ridge":
            coeff = f.coef_.tolist()
            feat_dict = {}
            for col, val in sorted(zip(columns, coeff), key=lambda x: x[1], reverse=True):
                feat_dict[col] = val

            feat_df = pd.DataFrame({'Feature': feat_dict.keys(), 'Importance': feat_dict.values()})
            feat_df_pos = feat_df.loc[feat_df['Importance'] > 0, :].sort_values("Importance", ascending=False)
            feat_df_neg = feat_df.loc[feat_df['Importance'] < 0, :].sort_values("Importance", ascending=False)

            featdf_postop = feat_df_pos.head(10)
            featdf_negtop = feat_df_neg.tail(10)

            feat_dftop = pd.concat([featdf_postop, featdf_negtop], ignore_index=True)

            values = feat_dftop.Importance
            idx = feat_dftop.Feature
            fig = plt.figure(figsize=(10, 8))
            clrs = ['green' if (x < max(values)) else 'red' for x in values]
            sns.barplot(y=idx, x=values, palette=clrs).set(title='Important features to predict LOS')
            plt.show()
            st.pyplot(fig)
