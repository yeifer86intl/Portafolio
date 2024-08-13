from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy import text
from sqlalchemy.engine.base import Engine

from src.config import QUERIES_ROOT_PATH

QueryResult = namedtuple("QueryResult", ["query", "result"])


class QueryEnum(Enum):
    """This class enumerates all the queries that are available"""

    DELIVERY_DATE_DIFFERECE = "delivery_date_difference"
    GLOBAL_AMMOUNT_ORDER_STATUS = "global_ammount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"


def read_query(query_name: str) -> str:
    """Read the query from the file.

    Args:
        query_name (str): The name of the file.

    Returns:
        str: The query.
    """
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql_file = f.read()
    return sql_file


def execute_query(query: str, database: Engine) -> DataFrame:
    """Execute a SQL query and return the result as a DataFrame.

    Args:
        query (str): The SQL query to execute.
        database (Engine): The database connection.

    Returns:
        DataFrame: The result of the query.
    """
    with database.connect() as connection:
        result = pd.read_sql(query, con=connection.connection)
    return result


def query_delivery_date_difference(database: Engine) -> QueryResult:
    query_name = QueryEnum.DELIVERY_DATE_DIFFERECE.value
    print(query_name)

    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)


def query_global_ammount_order_status(database: Engine) -> QueryResult:
    query_name = QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value
    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)


def query_revenue_by_month_year(database: Engine) -> QueryResult:
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)


def query_revenue_per_state(database: Engine) -> QueryResult:
    query_name = QueryEnum.REVENUE_PER_STATE.value
    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)


def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    query_name = QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value
    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)


def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    query_name = QueryEnum.TOP_10_REVENUE_CATEGORIES.value
    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)


def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    query_name = QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value
    query = read_query(query_name)
    result = execute_query(query, database)
    return QueryResult(query=query_name, result=result)

def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    """Obtiene la relación entre el valor del flete y el peso para órdenes entregadas.

    En esta consulta, queremos evaluar si existe una correlación entre
    el peso del producto y el valor pagado por la entrega.

    Utilizaremos las tablas olist_orders, olist_order_items y olist_products junto
    con algunas funciones de Pandas para producir la salida deseada: una tabla que
    nos permita comparar el peso total de la orden y el valor total del flete.

    Args:
        database (Engine): Conexión a la base de datos.

    Returns:
        QueryResult: La consulta de datos de valor del flete vs peso.
    """
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value
    # query_name = "GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP"

    # Obtener órdenes de la tabla olist_orders
    orders_query = "SELECT * FROM olist_orders"
    orders = execute_query(orders_query, database)

    # Obtener ítems de la tabla olist_order_items
    items_query = "SELECT * FROM olist_order_items"
    items = execute_query(items_query, database)

    # Obtener productos de la tabla olist_products
    products_query = "SELECT * FROM olist_products"
    products = execute_query(products_query, database)

    # Obtener pagos de la tabla olist_order_payments
    payments_query = "SELECT * FROM olist_order_payments"
    payments = execute_query(payments_query, database)

    # Obtener feriados de la tabla public_holidays
    holidays_query = "SELECT * FROM public_holidays"
    holidays = execute_query(holidays_query, database)

    # Combinar las tablas items, orders y products
    data = pd.merge(items, orders, on='order_id')
    data = pd.merge(data, products, on='product_id')

    # Filtrar solo órdenes entregadas
    delivered = data[data['order_status'] == 'delivered']

    # Agrupar por order_id y sumar freight_value y product_weight_g
    aggregations = delivered.groupby('order_id').agg(
        total_freight_value=('freight_value', 'sum'),
        total_weight=('product_weight_g', 'sum')
    ).reset_index()

    # Devolver el resultado
    return QueryResult(query=query_name, result=aggregations)

def query_orders_per_day_and_holidays_2017(database: Engine) -> QueryResult:
    """Obtiene la consulta de órdenes por día y feriados en 2017.

    En esta consulta, queremos obtener una tabla con la relación entre el número
    de órdenes hechas cada día y también información que indique si ese día fue
    un feriado.

    Args:
        database (Engine): Conexión a la base de datos.

    Returns:
        QueryResult: La consulta de órdenes por día y feriados en 2017.
    """
    query_name = QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value
    # query_name = "ORDERS_PER_DAY_AND_HOLIDAYS_2017"

    # Leer los feriados de la tabla public_holidays
    holidays_query = "SELECT * FROM public_holidays"
    holidays = execute_query(holidays_query, database)

    # Leer las órdenes de la tabla olist_orders
    orders_query = "SELECT * FROM olist_orders"
    orders = execute_query(orders_query, database)

    # Convertir la columna order_purchase_timestamp a datetime
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

    # Filtrar solo las órdenes del año 2017
    filtered_dates = orders[orders["order_purchase_timestamp"].dt.year == 2017]

    # Contar las órdenes por día
    order_purchase_amount_per_date = filtered_dates["order_purchase_timestamp"].dt.date.value_counts().sort_index()

    # Crear un DataFrame con el resultado
    result_df = pd.DataFrame({
        "date": order_purchase_amount_per_date.index,
        "order_count": order_purchase_amount_per_date.values
    })

    # Añadir la columna de feriado
    holidays["date"] = pd.to_datetime(holidays["date"]).dt.date
    result_df["holiday"] = result_df["date"].isin(holidays["date"])

    # Devolver el resultado
    return QueryResult(query=query_name, result=result_df)



def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    return [
        query_delivery_date_difference,
        query_global_ammount_order_status,
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]


def run_queries(database: Engine) -> Dict[str, DataFrame]:
    query_results = {}
    for query in get_all_queries():
        query_result = query(database)
        query_results[query_result.query] = query_result.result
    return query_results


# Ejemplo de uso:
# query_results: Dict[str, DataFrame] = run_queries(database=ENGINE)
