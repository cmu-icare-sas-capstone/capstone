import time

import pandas as pd
import l1.etl.DatabaseIO as dbio
import l1.constants.FILEPATH as FILEPATH
from l1.etl.DataLoader import data_loader
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

"""
frequency of los
"""
# df = dbio.read_from_db("CMS_Medicare_Cancer_Alley_DATA1_4_")
# los_counts = pd.DataFrame({"count": df.value_counts(["length_of_stay"]), "percentage": df.value_counts(["length_of_stay"])/len(df)})
# los_counts = los_counts.sort_index()
# los_counts.to_csv(FILEPATH.BASE_PATH+"/data/files/medicare_los_count.csv")

# df = pd.read_excel("/Users/mtong/Documents/project/capstone/data/files/COVID_risk_factors.xlsx")
# df = data_loader.format_column_names(df)
# df = data_loader.format_column_types(df, filename=None, format_types={"ccs_diagnosis_code": str, "ccs_diagnosis_description": str, "covid": bool})
# df = df[["ccs_diagnosis_code", "covid"]]
# df = df.drop_duplicates()
#
# df = df.reset_index(drop=True)
# print(df)
# dbio.write_to_db(df, "ccs_covid_risk", 1)

# df = dbio.read_from_db("cms_medicare_with_covid_risk")
# print(df[["length_of_stay"]].describe())

group_sql =\
"select \
	zip_code_3_digits, \
    round (avg(length_of_stay),0) as avg_los, \
    round(avg(total_costs),2) as avg_cost, \
    round (avg(total_charges),2) as avg_charge \
from cms_medicare_with_covid_risk \
where \
	covid=1 \
    and primary_diagnosis = 'COVID-19' \
    and zip_code_3_digits is not null \
    and zip_code_3_digits != 'OOS' \
group by zip_code_3_digits \
order by zip_code_3_digits, avg_los;"

df = dbio.read_from_db(None, group_sql)
print(df)
df = df.set_index(["zip_code_3_digits"])
print(df)
axes = df.plot.bar(y=["avg_los", "avg_cost", "avg_charge"], subplots=True)
axes[1].legend(loc=3)
plt.show()
