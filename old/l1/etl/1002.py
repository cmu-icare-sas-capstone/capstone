import pandas as pd
df = pd.read_csv("../../data/files/data6_5.csv")
pd.set_option("display.max_columns", 20)
print(df.head(20))
columns = df.columns
important_cols = ['Facility Id', 'Age Group','Zip Code - 3 digits','Gender',
                  'Race','Ethnicity','Length of Stay','Type of Admission',
                  'Patient Disposition','CCS Diagnosis Code','CCS Diagnosis Description',
                  'APR DRG Code','APR DRG Description','APR MDC Code',
                  'APR MDC Description','APR Severity of Illness Code',
                  'APR Severity of Illness Description','Payment Typology 1',
                  'Attending Provider License Number',
                  'Total Charges','Total Costs',
                  'FIPS_Code_x','Area_name','CDC 2018 Diagnosed Diabetes Percentage',
                  'CDC 2018 Overall SVI','SUM of COUNTUNIQUE of Rndrng_NPI 2019 Physician Other Providers PUF',
                  'COVID','COVID_HOSP','PRIMARY_ADM_DIAG','LAT','LON']

df1 = df[important_cols]

##type of admission value restrictions
TOA_list = ['Emergency','Urgent','Trauma']
df1 = df1[df1['Type of Admission'].isin(TOA_list)]
##payment typology 1 value restrictions
paytypo_list = ['Federal/State/Local/VA','Medicaid','Medicare','Blue Cross/Blue Shield']
df1 = df1[df1['Payment Typology 1'].isin(paytypo_list)]

# Drop rows where zip codes are missing
df1 = df1[df1['Zip Code - 3 digits'].notna()] ##1041 rows affected
df1 = df1[~df1['PRIMARY_ADM_DIAG'].isin(['#REF!'])]
df1 = df1[df1['PRIMARY_ADM_DIAG'].notna()]
df1.to_pickle("data7_0")

print(len(df1))
# nullcolcount = df1.isnull().sum()



