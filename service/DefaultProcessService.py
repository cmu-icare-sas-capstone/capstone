from service.ProcessService import ProcessService
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
