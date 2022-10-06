import l1.etl.DatabaseIO as dbio

data = dbio.read_from_db("hospital_inpatient_discharges")


def group_by(column: str):
    group = data.groupby([column]).count()
    group = group["index"]
    group = group.rename("count")
    return group


group_by("age_group")
