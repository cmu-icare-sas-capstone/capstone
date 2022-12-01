import init
from bean.GlobalState import state

repo = state.get("repo")

# sql = "SELECT facility_id, SUM(long_stay) as sum, COUNT(long_stay) as count " \
#       "FROM default_data_clean " \
#       "WHERE ccs_diagnosis_description='Diabetes mellitus with complications' " \
#       "OR ccs_diagnosis_description='Diabetes mellitus without complication' " \
#       "GROUP BY facility_id"
#
# # sql = "SELECT DISTINCT ccs_diagnosis_description FROM default_data_clean WHERE ccs_diagnosis_description LIKE '%Diabetes%'"
# df = repo.execute(sql)
# df["percentage"]=df["sum"]/df["count"]
# df = df.sort_values(by=["percentage"])
# df.to_csv("percentage")

# sql = "SELECT facility_id, AVG(length_of_stay) AS avg_los FROM default_data_clean " \
#       "WHERE ccs_diagnosis_description='Diabetes mellitus with complications' " \
#       "OR ccs_diagnosis_description='Diabetes mellitus without complication' " \
#       "GROUP BY facility_id"
#
# df = repo.execute(sql)
# df = df.sort_values(by="avg_los")
# df.to_csv("los")

df = repo.read_df("default_data_clean")
# sql = "SELECT " \
#       "length_of_stay, " \
#       "AVG(average_of_bene_avg_risk_scre_2019_physician_other_providers_puf) as avg_hcc_score " \
#       "FROM default_data_clean " \
#       "GROUP BY length_of_stay"
#
# df = repo.execute(sql)
# df.to_csv("los_hcc_long_stay.csv")
def los():
      sql = "SELECT facility_id, " \
             "COUNT(CASE WHEN length_of_stay <= 3 THEN 1 ELSE NULL END) as let3, " \
             "COUNT(CASE WHEN length_of_stay > 3 AND length_of_stay < 5.5 THEN 1 ELSE NULL END) as gt3lt6, " \
             "COUNT(CASE WHEN length_of_stay >= 6 AND length_of_stay <= 9 THEN 1 ELSE NULL END) as get6let9, " \
             "COUNT(CASE WHEN length_of_stay > 9 THEN 1 ELSE NULL END) as gt9, " \
             "COUNT(CASE WHEN length_of_stay >= 25 THEN 1 ELSE NULL END) as gt25, " \
             "COUNT(*) as total " \
             "FROM default_data_clean " \
             "WHERE ccs_diagnosis_description='Diabetes mellitus with complications' " \
             "OR ccs_diagnosis_description='Diabetes mellitus without complication' " \
             "GROUP BY facility_id"

      res = repo.execute(sql)
      res.to_csv("los_separate.csv")

los()