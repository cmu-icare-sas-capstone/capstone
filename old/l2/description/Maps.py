import pgeocode
import old.l1.etl.DatabaseIO as dbio


def heatmap_los():
    # TODO add pickle read and write to sql
    sql = \
        "select z.zip, round(avg(c.length_of_stay),2) avg_los from cms_medicare_with_covid_risk c \
         join zip_match z \
         on c.zip_code_3_digits = z.zip_code_3_digits \
         group by z.zip"

    df = dbio.read_from_db(table_name=None, sql=sql)

    nomi = pgeocode.Nominatim("us")
    postal_info_map = {}

    for index, row in df.iterrows():
        zipcode = str(int(row["zip"]))
        if zipcode not in postal_info_map:
            postal_info = nomi.query_postal_code(zipcode)
            postal_info_map[zipcode] = postal_info

        postal_info = postal_info_map[zipcode]
        latitude = postal_info["latitude"]
        longitude = postal_info["longitude"]
        df.at[index, "latitude"] = latitude
        df.at[index, "longitude"] = longitude

    data = df.loc[:, ('latitude', 'longitude')]
    max_los = df["avg_los"].max()
    min_los = df["avg_los"].min()
    data["weight"] = (df.loc[:, "avg_los"] - min_los) / (max_los - min_los)

    return data
