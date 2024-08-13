# src/load.py
import matplotlib

def main_plots_dag():

    
    import matplotlib.pyplot as plt
    from src import config
    import seaborn as sns
    import pandas as pd
    from pandas import DataFrame 
    import plotly.express as px
    from src import config
    from src.transform import QueryEnum
    from sqlalchemy import create_engine
    from typing import Dict
    from pathlib import Path
    from src.transform import run_queries

    from src.plots import (
    plot_freight_value_weight_relationship,
    plot_global_amount_order_status,
    plot_real_vs_predicted_delivered_time,
    plot_revenue_by_month_year,
    plot_revenue_per_state,
    plot_top_10_least_revenue_categories,
    plot_top_10_revenue_categories,
    plot_top_10_revenue_categories_ammount,
    plot_delivery_date_difference,
    plot_order_amount_per_day_with_holidays,
    )

    pd.options.display.float_format = '{:,.2f}'.format

    
    ENGINE = create_engine(rf"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}", echo=False)
    query_results: Dict[str, DataFrame] = run_queries(database=ENGINE)


    # Asegúrate de que las configuraciones por defecto de matplotlib estén cargadas
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    revenue_by_month_year = query_results[QueryEnum.REVENUE_BY_MONTH_YEAR.value]
    top_10_revenue_categories = query_results[QueryEnum.TOP_10_REVENUE_CATEGORIES.value]
    top_10_least_revenue_categories = query_results[QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value]
    revenue_per_state = query_results[QueryEnum.REVENUE_PER_STATE.value]
    delivery_date_difference = query_results[QueryEnum.DELIVERY_DATE_DIFFERECE.value]
    real_vs_estimated_delivered_time = query_results[QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value]
    global_ammount_order_status = query_results[QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value]
    orders_per_day_and_holidays = query_results[QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value]
    freight_value_weight_relationship = query_results[QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value]
    



    # Generación de gráficos
    plot_revenue_by_month_year(revenue_by_month_year, 2017)
    plot_top_10_revenue_categories(top_10_revenue_categories)
    plot_top_10_revenue_categories_ammount(top_10_revenue_categories)
    plot_top_10_least_revenue_categories(top_10_least_revenue_categories)
    plot_revenue_per_state(revenue_per_state)
    plot_delivery_date_difference(delivery_date_difference)
    plot_real_vs_predicted_delivered_time(real_vs_estimated_delivered_time, year=2017)
    plot_global_amount_order_status(global_ammount_order_status)
    holidays = list(orders_per_day_and_holidays["date"][orders_per_day_and_holidays["holiday"] == True])
    plot_order_amount_per_day_with_holidays(orders_per_day_and_holidays, holidays)
    plot_freight_value_weight_relationship(freight_value_weight_relationship)

    print("Generación de gráficos completa.")

if __name__ == "__main__":
    main_plots_dag()