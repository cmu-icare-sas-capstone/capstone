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
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# df = pd.read_pickle("app_data")
# df = df.astype(float)
# print(df.dtypes)
# corrM1 = df.corr()
# corrM = corrM1[['total_costs', 'length_of_stay']]
# corrM1 = df.corr()
# pd.set_option("display.max_columns", None)
# fig, ax = plt.subplots(figsize=(10, 30))
# sns.heatmap(corrM, annot=True)
# plt.title(' TOTAL_COSTS                     LENGTH_OF_STAY')
# fig.show()
# import pandas as pd
# from repository.Repository import Repository
# import configuration.AppConfiguration as app_config
# from configuration.DuckDbConfiguration import duckdb_configuration
# repo = Repository(app_config, duckdb_configuration.get_connection())
# df = pd.read_csv("data/files/CMS_PUBLIC_COMMENTS_2022_7-9.csv")
# print(df.dtypes)
# repo.save_df(df, "comment")

import plotly.graph_objects as go
from plotly.subplots import make_subplots

labels = ['1st', '2nd', '3rd', '4th', '5th']

# Define color sets of paintings
night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
sunflowers_colors = ['rgb(177, 127, 38)', 'rgb(205, 152, 36)', 'rgb(99, 79, 37)',
                     'rgb(129, 180, 179)', 'rgb(124, 103, 37)']
irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                 'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
cafe_colors =  ['rgb(146, 123, 21)', 'rgb(177, 180, 34)', 'rgb(206, 206, 40)',
                'rgb(175, 51, 21)', 'rgb(35, 36, 21)']

# Create subplots, using 'domain' type for pie charts
specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
fig = make_subplots(rows=2, cols=2, specs=specs)

# Define pie charts
fig.add_trace(go.Pie(title=labels, values=[38, 27, 18, 10, 7], name='Starry Night',
                     marker_colors=night_colors), 1, 1)
fig.add_trace(go.Pie(labels=labels, values=[28, 26, 21, 15, 10], name='Sunflowers',
                     marker_colors=sunflowers_colors), 1, 2)
fig.add_trace(go.Pie(labels=labels, values=[38, 19, 16, 14, 13], name='Irises',
                     marker_colors=irises_colors), 2, 1)
fig.add_trace(go.Pie(labels=labels, values=[31, 24, 19, 18, 8], name='The Night Café',
                     marker_colors=cafe_colors), 2, 2)

# Tune layout and hover info
fig.update_traces(hoverinfo='label+percent+name', textinfo='none')
fig.update(layout_title_text='Van Gogh: 5 Most Prominent Colors Shown Proportionally',
           layout_showlegend=False)

fig = go.Figure(fig)
fig.show()
