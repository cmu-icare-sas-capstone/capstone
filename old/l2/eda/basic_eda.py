import old.l1.etl.DatabaseIO as dbio

data = dbio.read_from_db("hospital_inpatient_discharges")


def group_by_count(column: str):
    group = data.groupby([column]).count()
    group = group["index"]
    group = group.rename("count")
    return group


def group_by_average(column: str, value: str):
    temp_df = data.loc[:, [column, value]]
    group = temp_df.groupby([column]).mean()
    return group


def heatmap():
    temp_df = data.loc[:, ["lat", "lon", "length_of_stay"]]
    area_group = data.groupby(["lat", "lon"]).mean()
    print(area_group)

