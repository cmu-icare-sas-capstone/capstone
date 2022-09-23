import pandas
import pandas as pd

from ..Constants import FILEPATH
from ..Constants import DTYPES
from .ETLIO import write_to_db

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

    def format_column_names(self, df: DataFrame) -> DataFrame:
        columns = df.columns
        mapper = {}
        for i in range(0, len(columns)):
            dash_column = columns[i].lower().strip()
            dash_column = re.sub(DataLoader.strange_characters, "_", dash_column)
            dash_column = re.sub(r"(_)\1+", "_", dash_column)
            mapper[columns[i]] = dash_column

        df = df.rename(columns=mapper)
        return df

    def get_filename_from_path(self, absolute_path: str) -> str:
        path_tokens = re.split(r"[/\\]", absolute_path)
        filename = path_tokens[len(path_tokens)-1].replace(r".csv", "").replace(r".xlsx", "")
        return filename

    def format_column_types(self, df: DataFrame, filename: str) -> DataFrame:
        df = df.convert_dtypes()
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

        return df

    def load(self, absolute_path: str):
        print("reading file from " + absolute_path)
        if absolute_path.endswith(".csv"):
            df = pd.read_csv(filepath_or_buffer=absolute_path, delimiter=",")
        elif absolute_path.endswith(".xlsx"):
            df = pandas.read_excel(absolute_path)
        else:
            raise Exception("file type not supported, it should be csv or excel file")

        df = self.format_column_names(df)
        print("get dataframe with head")
        print(df.columns)
        print(df.head(5))

        filename = self.get_filename_from_path(absolute_path)
        df = self.format_column_types(df, filename)

        print("Writing to the database... table name " + filename)
        write_to_db(df, filename, 100)
        print("Finished!")


data_loader = DataLoader()


