# Database Setup
Connect through workbench or any others use this information

host = 216.128.148.102

port = 3306

database = capstone

username = root

password = ?2?QaB%,s?F7A8Jrs/+4bh0^vn1R77pt

# Database IO
```python
# under the root of the project
import L1.ETL.DatabaseIO as dbio

# read from the databaase
dbio.read_from_db("table_name")

# write to database 
# This should be done after cleaning
# check
#     1. valid table name
#     2. valid column name
#     3. data type if needed
# threads_num = number of lines of dataframe / 5000

dbio.write_to_db(df, "table_name", threads_num)
```
