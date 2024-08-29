def main_transform_dag():
    from src import config
    from sqlalchemy import create_engine
    from src.transform import QueryEnum
    from src import config
    from src.transform import run_queries
    from typing import Dict
    from pathlib import Path
    from pandas import DataFrame

    ENGINE = create_engine(rf"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}", echo=False)
    query_results: Dict[str, DataFrame] = run_queries(database=ENGINE)
    
    revenue_by_month_year = query_results[QueryEnum.REVENUE_BY_MONTH_YEAR.value]
    top_10_revenue_categories = query_results[QueryEnum.TOP_10_REVENUE_CATEGORIES.value]
    top_10_least_revenue_categories = query_results[QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value]
    revenue_per_state = query_results[QueryEnum.REVENUE_PER_STATE.value]
    delivery_date_difference = query_results[QueryEnum.DELIVERY_DATE_DIFFERECE.value]
    real_vs_estimated_delivered_time = query_results[QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value]
    global_ammount_order_status = query_results[QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value]
    orders_per_day_and_holidays = query_results[QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value]
    freight_value_weight_relationship = query_results[QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value]
    
    print(freight_value_weight_relationship.head(5))
    
    
    
    
    print("Transformación de datos completa.")

if __name__ == "__main__":
    main_transform_dag()