import pandas as pd

from l1.constants import FILEPATH
from l1.constants import DTYPES
from l1.etl.DatabaseIO import write_to_db

from pandas import DataFrame
import re

"""
DataLoader

refactor dataframe and load it to the database
will use datafilter to filter the data
will use dtypes to reformat the data 
"""


class DataLoader:
    strange_characters = r"(\s|:|\(|\)|\-|\+|\$|>|\.)"

    def __init__(self):
        return

    """
        reformat the column names to snake case
        1. all letters will be small cases
        2. words will be connected with _
        3. special characters will be removed, pls add them to strange_characters if meet new ones
        
        for example: 
            "Zip Code - 3 digits"  -> zip_code_3_digits
            "SUM(TOT_POP)" -> sum_tot_pop
    """

    def format_column_names(self, df: DataFrame) -> DataFrame:
        print("formatting columns")
        columns = df.columns
        mapper = {}
        for i in range(0, len(columns)):
            snake_column = columns[i].lower().strip()
            snake_column = re.sub(DataLoader.strange_characters, "_", snake_column)
            snake_column = re.sub(r"(_)\1+", "_", snake_column)
            mapper[columns[i]] = snake_column

        df = df.rename(columns=mapper)
        print("formatting finished")
        print(df.columns)
        return df

    def get_filename_from_path(self, absolute_path: str) -> str:
        path_tokens = re.split(r"[/\\]", absolute_path)
        filename = path_tokens[len(path_tokens) - 1].replace(r".csv", "").replace(r".xlsx", "")
        return filename

    """
        1. for every columns convert them to specified columns types as defined in DTYPES
        2. for other columns let pandas to decide the best types
        
        add new to the conversion block if needed
    """

    def format_column_types(self, df: DataFrame, filename: str = None, format_types: dict = None) -> DataFrame:
        print("converting data types")
        df = df.convert_dtypes()

        if filename is not None:
            # ------------- conversion block - filename ----------------#
            if filename == FILEPATH.CMS_Medicare_Cancer_Alley_DATA1_4_:
                for member in DTYPES.MEDICARE_DTYPES:
                    df[member] = df[member].replace(DataLoader.strange_characters, "", regex=True)
                df = df.astype(DTYPES.MEDICARE_DTYPES)

            elif filename == FILEPATH.Comorbidities_for_COVID_Synthetic_data:
                for member in DTYPES.COMORBIDITIES_DTYPES:
                    df[member] = df[member].replace(DataLoader.strange_characters, "", regex=True)
                df = df.astype(DTYPES.COMORBIDITIES_DTYPES)

            elif filename == FILEPATH.Diagnosis_Review:
                for member in DTYPES.DIAGNOSIS_REVIEW_DTYPES:
                    df[member] = df[member].replace(DataLoader.strange_characters, "", regex=True)
                df = df.dropna(subset=DTYPES.DIAGNOSIS_REVIEW_DTYPES.keys())
                df = df.astype(DTYPES.DIAGNOSIS_REVIEW_DTYPES)
            # ------------- conversion block - filename ----------------#
        else:
            for member in format_types:
                df[member] = df[member].replace(DataLoader.strange_characters, "", regex=True)
            df = df.dropna(subset=format_types.keys())
            df = df.astype(format_types)

        print("converting finished")
        print(df.dtypes)
        return df

    """
        load csv files or xlsx file to the database
        the table name would be the same as filename without extension .csv and .xlsx
        
        steps taken: 
            1. read df
            2. rename columns
            3. reformat columns
            4. write to the database
    """
    def load(self, absolute_path: str):
        print("reading file from " + absolute_path)
        if absolute_path.endswith(".csv"):
            df = pd.read_csv(filepath_or_buffer=absolute_path, delimiter=",")
        elif absolute_path.endswith(".xlsx"):
            df = pd.read_excel(absolute_path)
        else:
            raise Exception("file type not supported, it should be csv or excel file")
        print("reading finished")

        df = self.format_column_names(df)
        print(df.head(5))

        filename = self.get_filename_from_path(absolute_path)
        print("get the filename: " + filename)
        df = self.format_column_types(df, filename)

        print("Writing to the database... table name " + filename)
        write_to_db(df, filename, min(int(len(df) / 5000), 100))
        print("Finished!")


data_loader = DataLoader()
