import pandas as pd
import l1.etl.DatabaseIO as dbio

def los_heatmap():
    sql = \
        "select \
            zip_code_3_digits, \
            round (avg(length_of_stay),0) as avg_los \
        from cms_medicare_with_covid_risk \
        where \
            covid=1 \
            and primary_diagnosis = 'COVID-19' \
            and zip_code_3_digits is not null \
            and zip_code_3_digits != 'OOS' \
        group by zip_code_3_digits \
        order by zip_code_3_digits, avg_los;"

    df = dbio.read_from_db(None, sql)
