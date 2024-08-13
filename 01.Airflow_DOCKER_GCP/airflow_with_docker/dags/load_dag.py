# src/load.py

def main_load_dag():
    import pandas as pd
    from pandas import DataFrame
    from sqlalchemy import create_engine
    from typing import Dict
    from pathlib import Path

    from src.transform import QueryEnum
    from src import config
    from src.transform import run_queries
    from src.extract import extract
    from src.load import load
    # Create the database sql file
    Path(config.SQLITE_BD_ABSOLUTE_PATH).touch()

    # Create the database connectionp
    ENGINE = create_engine(rf"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}", echo=False)


    csv_folder = config.DATASET_ROOT_PATH
    public_holidays_url = config.PUBLIC_HOLIDAYS_URL

    print("csv_folder",csv_folder)
    print("public_holidays_url",public_holidays_url)
    # 1. Get the mapping of the csv files to the table names.
    csv_table_mapping = config.get_csv_to_table_mapping()
    print("csv_table_mapping",csv_table_mapping)



    # 2. Extract the data from the csv files, holidays and load them into the dataframes.
    csv_dataframes = extract(csv_folder, csv_table_mapping, public_holidays_url)
    print("------------------------")
    print(csv_dataframes)

    load(data_frames=csv_dataframes, database=ENGINE)

    print("final")
    
    

if __name__ == "__main__":
    main_load_dag()
