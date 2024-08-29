from typing import Dict
from pandas import DataFrame
from sqlalchemy.engine.base import Engine

def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
        database (Engine): The database engine.
    """


    with database.connect() as connection:
        for table_name, df in data_frames.items():
            print(table_name)
            df.to_sql(table_name, con=connection.connection, index=False, if_exists='replace')
            print(table_name,"  cargada")
            print("__________________________________________")

# Ejemplo de uso:
# Asegúrate de tener los siguientes paquetes instalados:
# pip install pandas sqlalchemy

# Supongamos que tienes un diccionario de DataFrames llamado csv_dataframes y un motor de base de datos llamado ENGINE

# from sqlalchemy import create_engine
# ENGINE = create_engine('sqlite:///example.db')

# csv_dataframes = {
#     'table1': DataFrame(data1),
#     'table2': DataFrame(data2)
# }

# load(data_frames=csv_dataframes, database=ENGINE)
