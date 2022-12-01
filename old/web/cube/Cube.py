from typing import List

import old.l1.etl.DatabaseIO as dbio
from pandas import DataFrame
import re
data = dbio.read_from_db("hospital_inpatient_discharges")

diabetes_group = ["Diabetes mellitus with complications", "Diabetes mellitus without complication"]


def get_cube(data, slicer: list, filters: dict, values: list):
    cube = data.loc[:, slicer + values]
    for key in filters:
        if type(filters[key]) is list:
            query_str = "%s==%s" % (key, filters[key])
        else:
            query_str = "%s=='%s'" % (key, filters[key])
        cube = cube.query(query_str)

    return cube


def query_available_options(data, column):
    options = data.loc[:, column].drop_duplicates()
    options = options.tolist()
    if column == "ccs_diagnosis_description":
        options += ["Diabetes Group", "Non Diabetes Group"]
    return options


def group_cube(cube, column):
    return cube.groupby(by=[column])


def match_all_value_of_wildcard(data, column: str, wildcard: str):
    unique_values = data.loc[:, column].unique()
    matched_values = []
    for v in unique_values.tolist():
        if re.match(wildcard.lower(), v.lower()):
            matched_values.append(v)

    return matched_values


def match_columns(data: DataFrame, column: str, wildcard: str) -> List[str]:
    available_columns: List[str] = query_available_options(data, column)
    matched_columns: List[str] = []
    for column in available_columns:
        if re.match(wildcard, column):
            matched_columns.append(column)
    return matched_columns


# run tests
if __name__ == "__main__":
    print("run tests")
    # res1 = get_cube(data, ["ccs_diagnosis_description"], {"ccs_diagnosis_description": "Diabetes Group"}, ["length_of_stay"])
    # print(res1)
    # res2 = query_available_options(data, "ccs_diagnosis_description")
    # print(res2)
    res3 = match_columns(data, "ccs_diagnosis_description", "Dia.*")
    print(res3)




