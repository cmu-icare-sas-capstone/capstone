# import pandas
#
# import init
# from bean.GlobalState import state
#
# repo = state.get("repo")
#
# # sql = "SELECT facility_id, SUM(long_stay) as sum, COUNT(long_stay) as count " \
# #       "FROM default_data_clean " \
# #       "WHERE ccs_diagnosis_description='Diabetes mellitus with complications' " \
# #       "OR ccs_diagnosis_description='Diabetes mellitus without complication' " \
# #       "GROUP BY facility_id"
# #
# # # sql = "SELECT DISTINCT ccs_diagnosis_description FROM default_data_clean WHERE ccs_diagnosis_description LIKE '%Diabetes%'"
# # df = repo.execute(sql)
# # df["percentage"]=df["sum"]/df["count"]
# # df = df.sort_values(by=["percentage"])
# # df.to_csv("percentage")
#
# # sql = "SELECT facility_id, AVG(length_of_stay) AS avg_los FROM default_data_clean " \
# #       "WHERE ccs_diagnosis_description='Diabetes mellitus with complications' " \
# #       "OR ccs_diagnosis_description='Diabetes mellitus without complication' " \
# #       "GROUP BY facility_id"
# #
# # df = repo.execute(sql)
# # df = df.sort_values(by="avg_los")
# # df.to_csv("los")
#
# df = repo.read_df("default_data_clean")
# # sql = "SELECT " \
# #       "length_of_stay, " \
# #       "AVG(average_of_bene_avg_risk_scre_2019_physician_other_providers_puf) as avg_hcc_score " \
# #       "FROM default_data_clean " \
# #       "GROUP BY length_of_stay"
# #
# # df = repo.execute(sql)
# # df.to_csv("los_hcc_long_stay.csv")
# def los():
#       sql = "SELECT facility_id, " \
#              "COUNT(CASE WHEN length_of_stay <= 3 THEN 1 ELSE NULL END) as let3, " \
#              "COUNT(CASE WHEN length_of_stay > 3 AND length_of_stay < 5.5 THEN 1 ELSE NULL END) as gt3lt6, " \
#              "COUNT(CASE WHEN length_of_stay >= 6 AND length_of_stay <= 9 THEN 1 ELSE NULL END) as get6let9, " \
#              "COUNT(CASE WHEN length_of_stay > 9 THEN 1 ELSE NULL END) as gt9, " \
#              "COUNT(CASE WHEN length_of_stay >= 25 THEN 1 ELSE NULL END) as gt25, " \
#              "COUNT(*) as total " \
#              "FROM default_data_clean " \
#              "WHERE ccs_diagnosis_description='Diabetes mellitus with complications' " \
#              "OR ccs_diagnosis_description='Diabetes mellitus without complication' " \
#              "GROUP BY facility_id"
#
#       res = repo.execute(sql)
#       res.to_csv("los_separate.csv")
#
# def data7():
#     df = pandas.read_pickle("data/pickles/data7_0")
#     print(df.columns)
#
# def risk_score():
#     sql = "SELECT DISTINCT area_name, average_of_bene_avg_risk_scre_2019_physician_other_providers_puf FROM default_data_clean"
#     df = repo.execute(sql)
#     print(df)
#
# risk_score()
#
# # ['length_of_stay', 'age_group', 'apr_severity_of_illness_code',
# #        'cdc_2018_overall_svi',
# #        'sum_countunique_rndrng_npi_physician_other_providers',
# #        'average_of_bene_avg_risk_scre_2019_physician_other_providers_puf',
# #        'covid_hosp', 'long_stay', 'gender_M', 'race_Multi-racial',
# #        'race_Other Race', 'race_White', 'covid_True',
# #        'ethnicity_Not Span/Hispanic', 'ethnicity_Spanish/Hispanic',
# #        'ethnicity_Unknown', 'type_of_admission_Trauma',
# #        'type_of_admission_Urgent', 'payment_typology_1_Federal/State/Local/VA',
# #        'payment_typology_1_Medicaid', 'payment_typology_1_Medicare',
# #        'patient_disposition_Cancer Center or Children's Hospital',
# #        'patient_disposition_Court/Law Enforcement',
# #        'patient_disposition_Critical Access Hospital',
# #        'patient_disposition_Expired',
# #        'patient_disposition_Facility w/ Custodial/Supportive Care',
# #        'patient_disposition_Home or Self Care',
# #        'patient_disposition_Home w/ Home Health Services',
# #        'patient_disposition_Hospice - Home',
# #        'patient_disposition_Hospice - Medical Facility',
# #        'patient_disposition_Inpatient Rehabilitation Facility',
# #        'patient_disposition_Left Against Medical Advice',
# #        'patient_disposition_Medicaid Cert Nursing Facility',
# #        'patient_disposition_Medicare Cert Long Term Care Hospital',
# #        'patient_disposition_Psychiatric Hospital or Unit of Hosp',
# #        'patient_disposition_Short-term Hospital',
# #        'patient_disposition_Skilled Nursing Home', 'apr_drg_code_165',
# #        'apr_drg_code_166', 'apr_drg_code_167', 'apr_drg_code_169',
# #        'apr_drg_code_171', 'apr_drg_code_173', 'apr_drg_code_175',
# #        'apr_drg_code_180', 'apr_drg_code_191', 'apr_drg_code_197',
# #        'apr_drg_code_24', 'apr_drg_code_26', 'apr_drg_code_305',
# #        'apr_drg_code_309', 'apr_drg_code_310', 'apr_drg_code_312',
# #        'apr_drg_code_313', 'apr_drg_code_314', 'apr_drg_code_316',
# #        'apr_drg_code_317', 'apr_drg_code_320', 'apr_drg_code_321',
# #        'apr_drg_code_344', 'apr_drg_code_351', 'apr_drg_code_361',
# #        'apr_drg_code_364', 'apr_drg_code_380', 'apr_drg_code_4',
# #        'apr_drg_code_405', 'apr_drg_code_420', 'apr_drg_code_424',
# #        'apr_drg_code_440', 'apr_drg_code_444', 'apr_drg_code_447',
# #        'apr_drg_code_468', 'apr_drg_code_48', 'apr_drg_code_5',
# #        'apr_drg_code_6', 'apr_drg_code_710', 'apr_drg_code_73',
# #        'apr_drg_code_82', 'apr_drg_code_890', 'apr_drg_code_892',
# #        'apr_drg_code_894', 'apr_drg_code_950', 'apr_drg_code_951',
# #        'apr_drg_code_952', 'apr_mdc_code_10', 'apr_mdc_code_11',
# #        'apr_mdc_code_18', 'apr_mdc_code_2', 'apr_mdc_code_24',
# #        'apr_mdc_code_5', 'apr_mdc_code_8', 'apr_mdc_code_9']
#
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_pickle("app_data")
df = df.astype(float)
print(df.dtypes)
corrM1 = df.corr()
corrM = corrM1[['total_costs', 'length_of_stay']]
corrM1 = df.corr()
pd.set_option("display.max_columns", None)
fig, ax = plt.subplots(figsize=(10, 30))
sns.heatmap(corrM, annot=True)
plt.title(' TOTAL_COSTS                     LENGTH_OF_STAY')
fig.show()