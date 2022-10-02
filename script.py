import sys
sys.path.append("/Users/mtong/Documents/project/capstone")

import pandas as pd
import l1.etl.DatabaseIO as dbio
df = dbio.read_from_db("hospital_inpatient_discharges")
df.to_pickle()
print(df)