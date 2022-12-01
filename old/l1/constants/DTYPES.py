"""
Data types for files
"""

# TODO: for other types that are not clear, cast them to string
MEDICARE_DTYPES = {
    "length_of_stay": float,
    "discharge_year": int,
    "total_charges": float,
    "total_costs": float,
    "covid_diagnosis": bool,
    "apr_drg_code": int
}

COMORBIDITIES_DTYPES = {
    "apr_drg_code": int,
    "covid_hosp": bool
}

DIAGNOSIS_REVIEW_DTYPES = {
    "apr_drg_code": int,
    "covid_hosp": bool,
    "covid": str
}

FINAL = {
    "length_of_stay": float,
    "total_charges": float,
    "total_costs": float,
    "primary_adm_diag": bool,
    "apr_drg_code": int
}
