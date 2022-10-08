import l1.etl.DatabaseIO as dbio
import re
data = dbio.read_from_db("hospital_inpatient_discharges")


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
    return options.tolist()


def group_cube(cube, column):
    return cube.groupby(by=[column])


def match_all_value_of_wildcard(data, column: str, wildcard: str):
    unique_values = data.loc[:, column].unique()
    matched_values = []
    for v in unique_values.tolist():
        if re.match(wildcard.lower(), v.lower()):
            matched_values.append(v)

    return matched_values