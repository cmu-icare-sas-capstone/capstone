from service.ProcessService import ProcessService
import pandas as pd
import numpy as np
from scipy import stats
"""
clean rules: {
    columns: {
        column_name: []
    }

    rename: {
        column_name: "newName"
    },

    retype: {
        column_name: "newType"
    }
}
"""


class DefaultProcessService(ProcessService):
    CLEAN_RULES = {
        "columns": ["Facility Id", "Age Group", "Zip Code - 3 digits", "Gender",
                    "Race", "Ethnicity", "Length of Stay", "Type of Admission",
                    "Patient Disposition", "CCS Diagnosis Code", "CCS Diagnosis Description",
                    "APR DRG Code", "APR DRG Description", "APR MDC Code",
                    "APR MDC Description", "APR Severity of Illness Code",
                    "APR Severity of Illness Description", "Payment Typology 1",
                    "Attending Provider License Number",
                    "Total Charges", "Total Costs",
                    "FIPS_Code_x", "Area_name", "CDC 2018 Diagnosed Diabetes Percentage",
                    "CDC 2018 Overall SVI", "SUM of COUNTUNIQUE of Rndrng_NPI 2019 Physician Other Providers PUF",
                    "AVERAGE of Bene_Avg_Risk_Scre 2019 Physician Other Providers PUF",
                    "COVID", "COVID_HOSP", "PRIMARY_ADM_DIAG", "LAT", "LON"
                    ],
        "rename": {
            "SUM of COUNTUNIQUE of Rndrng_NPI 2019 Physician Other Providers PUF":
                "sum_countunique_rndrng_npi_physician_other_providers"
        },
        "retype": {
            "Length of Stay": "int",
            "Total Charges": "float",
            "Total Costs": "float",
            "PRIMARY_ADM_DIAG": "str",
            "Facility Id": "str"
        },
        "filters": {
            "Type of Admission": ["Emergency", "Urgent", "Trauma"],
            "Payment Typology 1": ["Federal/State/Local/VA", "Medicaid", "Medicare", "Blue Cross/Blue Shield"]
        },
        "revert_filters": {
            "PRIMARY_ADM_DIAG": ["#REF!"]
        },
        "drop_null": ["Zip Code - 3 digits", "PRIMARY_ADM_DIAG"],
    }
    FEA_RULES = {
        "calc_columns": [
            {
                "col": "length_of_stay",
                "calc_col": "long_stay",
                "dtype": "int",
                "conditions": [
                    ["gt", "5.5", "1"],
                    ["set", "5.5", "0"]
                ]
            }
        ]

    }

    def __init__(self, repo):
        super().__init__(repo)
        self.repo = repo

    # fetch a dataframe to see if it is default
    def is_default(self, df_name: str) -> bool:
        sql = "SELECT * FROM %s LIMIT 5" % df_name
        df = self.repo.execute(sql)
        for col in self.CLEAN_RULES["columns"]:
            if col.lower() not in df.columns:
                return False
        return True

    def process(self, df_name, progress_bar=None) -> str:
        exist = self.repo.exists_table(df_name + "_clean")
        if exist:
            return df_name + "_clean"
        super(DefaultProcessService, self).clean(df_name, self.CLEAN_RULES, progress_bar)
        progress_bar.progress(60)
        super(DefaultProcessService, self).feature_eng(df_name+"_clean", self.FEA_RULES)
        progress_bar.progress(80)
        self.repo.delete_table(df_name)
        return df_name + "_clean"

    def model_feature_eng(self, df_name, progress_bar=None):
        df = self.repo.read_df(df_name)
        df = df[df["ccs_diagnosis_description"].str.contains("diabetes", case=False)]  # 26816 remains
        df = df[~df["ccs_diagnosis_description"].str.contains("pancrea", case=False)]
        # (19731, 35)

        # Target only Age 65+
        df = df[(df['age_group'].str.contains("75+", case=False)) | (df['age_group'].str.contains("65-74", case=False))]

        df = df[df['gender'] != 'U']  # drop 5 rows whose Gender is 'U'

        # cleaning the 'covid' column
        df.loc[df['covid'] == 'FASLE', 'covid'] = 'FALSE'
        df.loc[df['covid'] == '0', 'covid'] = 'FALSE'
        df.loc[df['covid'] == '1', 'covid'] = 'TRUE'

        # drop columns where there are only 1 or NAN values
        df = df.drop(
            columns=['ccs_diagnosis_description', 'primary_adm_diag', 'apr_mdc_description', 'apr_drg_description',
                     "cdc_2018_overall_svi"])
        # drop the variables that are not useful in model: 'index', 'facility ID','zip code','area_name',attending_provider_license_number ''
        df = df.drop(
            columns=['area_name', 'zip_code_3_digits', 'attending_provider_license_number', 'fips_code_x', 'lat',
                     'lon'])
        # drop highly correlated columns
        df = df.drop(columns=['apr_severity_of_illness_description'])
        # drop non-related columns
        df = df.drop(columns=['cdc_2018_diagnosed_diabetes_percentage'])
        progress_bar.progress(30)
        target_vars = ['length_of_stay', 'total_charges', 'total_costs']

        df['apr_drg_code'] = df['apr_drg_code'].astype(str)
        df['apr_mdc_code'] = df['apr_mdc_code'].astype(str)
        df['ccs_diagnosis_code'] = df['ccs_diagnosis_code'].astype(str)

        for col in ['length_of_stay']:
            for i in range(1, len(df[col])):
                df = df.loc[np.abs(stats.zscore(df[col])) < 5]

        progress_bar.progress(70)
        df = df.drop(columns=['facility_id'])
        # Gender
        gender_male = pd.get_dummies(df['gender'], prefix='gender', prefix_sep='_', drop_first=True)
        df = pd.concat([df.drop(labels=['gender'], axis=1), gender_male], axis=1)

        # Race (4 races)
        race_encode = pd.get_dummies(df['race'], prefix='race', prefix_sep='_', drop_first=True)
        df = pd.concat([df.drop(labels=['race'], axis=1), race_encode], axis=1)

        # Covid
        covid_encode = pd.get_dummies(df['covid'], prefix='covid', prefix_sep='_', drop_first=True)
        df = pd.concat([df.drop(labels=['covid'], axis=1), covid_encode], axis=1)

        # ethnicity
        ethnicity_encode = pd.get_dummies(df['ethnicity'], prefix='ethnicity', prefix_sep='_', drop_first=True)
        df = pd.concat([df.drop(labels=['ethnicity'], axis=1), ethnicity_encode], axis=1)

        # type_of_admission
        admin_type_encode = pd.get_dummies(df['type_of_admission'], prefix='type_of_admission', prefix_sep='_',
                                           drop_first=True)
        df = pd.concat([df.drop(labels=['type_of_admission'], axis=1), admin_type_encode], axis=1)

        # payment typology
        payment_encode = pd.get_dummies(df['payment_typology_1'], prefix='payment_typology_1', prefix_sep='_',
                                        drop_first=True)
        df = pd.concat([df.drop(labels=['payment_typology_1'], axis=1), payment_encode], axis=1)

        # Patient Disposition
        disposition_encode = pd.get_dummies(df['patient_disposition'], prefix='patient_disposition', prefix_sep='_',
                                            drop_first=True)
        df = pd.concat([df.drop(labels=['patient_disposition'], axis=1), disposition_encode], axis=1)

        # apr_drg_code
        apr_drg_encode = pd.get_dummies(df['apr_drg_code'], prefix='apr_drg_code', prefix_sep='_', drop_first=True)
        df = pd.concat([df.drop(labels=['apr_drg_code'], axis=1), apr_drg_encode], axis=1)

        # apr_mdc_code
        apr_mdc_encode = pd.get_dummies(df['apr_mdc_code'], prefix='apr_mdc_code', prefix_sep='_', drop_first=True)
        df = pd.concat([df.drop(labels=['apr_mdc_code'], axis=1), apr_mdc_encode], axis=1)

        # ccs_diagnosis_code
        ccs_diagnosis_encode = pd.get_dummies(df['ccs_diagnosis_code'], prefix='ccs_diagnosis_code', prefix_sep='_',
                                              drop_first=True)
        df = pd.concat([df.drop(labels=['ccs_diagnosis_code'], axis=1), ccs_diagnosis_encode], axis=1)

        # Age Group (s5 age groups)
        enc_age_dict = {'0-17': 0, '18-44': 1, '45-64': 2, '65-74': 3,
                        '75+': 4}  # Define a dictionary for encoding target variable
        df['age_group'] = df['age_group'].map(enc_age_dict)  # Replace temp column values with the mapped values

        self.repo.save_df(df, df_name+"_model")
        progress_bar.progress(100)
