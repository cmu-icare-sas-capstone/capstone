# Important
Please check requirements.txt file to install missing packages if there's any. Make sure you update that list when you add new third-party packages.

These codes add the project capstone path to you working environment (spider, jupiter, etc.), so you can use self created packages that locate in this project. Please change the absolute path to your local capstone path.
```python
import sys
sys.path.extend(['absolute path'])
```
# Database IO

```python
# after you include the project path
import l1.etl.DatabaseIO as dbio

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

# Database Setup
Connect through workbench or any others use this information
connection type: standard TCP
host = 216.128.148.102

port = 3306

database = capstone

username = root

password = ?2?QaB%,s?F7A8Jrs/+4bh0^vn1R77pt
