import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import DataFrame
import matplotlib
import plotly.express as px

# Asegúrate de que las configuraciones por defecto de matplotlib estén cargadas
matplotlib.rc_file_defaults()
sns.set_style(style=None, rc=None)

def plot_revenue_by_month_year(df: DataFrame, year: int):
    """Plot revenue by month in a given year

    Args:
        df (DataFrame): Dataframe with revenue by month and year query result
        year (int): It could be 2016, 2017 or 2018
    """
    # Restaurar configuraciones predeterminadas de matplotlib
    matplotlib.rc_file_defaults()
    
    # Establecer el estilo de seaborn a su valor predeterminado
    sns.set_style(style=None, rc=None)

    # Crear la figura y los ejes
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Crear una línea de tiempo para los ingresos del año especificado
    sns.lineplot(data=df, x='month_no', y=f'Year{year}', marker="o", sort=False, ax=ax1)
    ax2 = ax1.twinx()

    # Crear un gráfico de barras para los ingresos del año especificado
    sns.barplot(data=df, x='month_no', y=f'Year{year}', alpha=0.5, ax=ax2)

    # Configurar el título y las etiquetas de los ejes
    ax1.set_title(f"Revenue by month in {year}")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue (Line Plot)")
    ax2.set_ylabel("Revenue (Bar Plot)")

    # Mostrar los nombres de los meses en el eje x
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df['month'], rotation=45)

    # Mostrar el gráfico
    plt.show()


def plot_real_vs_predicted_delivered_time(df: DataFrame, year: int):
    """Plot real vs predicted delivered time by month in a given year

    Args:
        df (DataFrame): Dataframe with real vs predicted delivered time by month and
                        year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1)
    ax1.twinx()
    g = sns.lineplot(
        data=df[f"Year{year}_estimated_time"], marker="o", sort=False, ax=ax1
    )
    g.set_xticks(range(len(df)))
    g.set_xticklabels(df.month.values)
    g.set(xlabel="month", ylabel="Average days delivery time", title="some title")
    ax1.set_title(f"Average days delivery time by month in {year}")
    ax1.legend(["Real time", "Estimated time"])

    plt.show()


def plot_global_amount_order_status(df: DataFrame):
    """Plot global amount of order status

    Args:
        df (DataFrame): Dataframe with global amount of order status query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["order_status"]]

    wedges, autotexts = ax.pie(df["Ammount"], textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Order Status",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Order Status Total")

    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.show()


def plot_revenue_per_state(df: DataFrame):
    """Plot revenue per state

    Args:
        df (DataFrame): Dataframe with revenue per state query result
    """
    fig = px.treemap(
        df, path=["customer_state"], values="Revenue", width=800, height=400
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_top_10_least_revenue_categories(df: DataFrame):
    """Plot top 10 least revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 least revenue categories query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Least Revenue Categories amount")

    plt.show()


def plot_top_10_revenue_categories_ammount(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    # Plotting the top 10 revenue categories amount
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Revenue Categories amount")

    plt.show()


def plot_top_10_revenue_categories(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    fig = px.treemap(df, path=["Category"], values="Num_order", width=800, height=400)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_freight_value_weight_relationship(df: DataFrame):
    """Plot freight value weight relationship

    Args:
        df (DataFrame): Dataframe with freight value weight relationship query result
    """
    # Scatterplot de la relación entre el valor del flete y el peso
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='total_weight', y='total_freight_value')
    plt.title('Relationship between Freight Value and Weight')
    plt.xlabel('Weight')
    plt.ylabel('Freight Value')
    plt.show()


def plot_delivery_date_difference(df: DataFrame):
    """Plot delivery date difference

    Args:
        df (DataFrame): Dataframe with delivery date difference query result
    """
    sns.barplot(data=df, x="Delivery_Difference", y="customer_state").set(
        title="Difference Between Delivery Estimate Date and Delivery Date"
    )


def plot_order_amount_per_day_with_holidays(df: DataFrame, holidays: list):
    """Plot order amount per day with holidays

    Args:
        df (DataFrame): Dataframe with order amount per day with holidays query result
        holidays (list): List of holiday dates
    """
    # Convertir las fechas a datetime si no lo están
    df['date'] = pd.to_datetime(df['date'])
    holidays = pd.to_datetime(holidays)

    # Gráfico de la cantidad de órdenes por día con festivos marcados
    plt.figure(figsize=(14, 7))
    plt.plot(df['date'], df['order_count'], label='Order Amount')
    
    for holiday in holidays:
        plt.axvline(x=holiday, color='red', linestyle='--', label='Holiday' if holiday == holidays[0] else "")

    plt.title('Order Amount per Day with Holidays')
    plt.xlabel('Date')
    plt.ylabel('Order Amount')
    plt.legend()
    plt.show()
