import pandas as pd
import numpy as np

import streamlit as st

months = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


@st.cache(show_spinner=True, allow_output_mutation=True, suppress_st_warning=True)
def loadCityData(city, city_codes_df, month, year):
    """
    Download data from https://ccartoday.com/market-statistics/
    INPUT:
    city - srting
    city_codes_df - pandas DataFrame
    month - int, 1-12
    year - int, 2011-2021
    house_type - 0 if Single-Family Detached
                 1 if Townhouse-Condo Attached

    OUTPUT:
    single_df - pandas DataFrame

    """
    city_code = city_codes_df[city_codes_df["city"] == city].iloc[0, 1]
    page_type = city_codes_df[city_codes_df["city"] == city].iloc[0, 2]

    central_stat_url = f"http://main.ccartoday.com/index.php/{page_type}/area/{month}/{year}/{city_code}"

    table_df = pd.read_html(central_stat_url)
    single_df = table_df[0][1:].transpose()[:3]

    single_df = single_df.rename(columns=single_df.iloc[0]).drop(single_df.index[0])

    single_df["Single-Family Detached"] = 1
    single_df["Townhouse-Condo Attached"] = 0

    condo_df = table_df[1][1:].transpose()[:3]

    condo_df = condo_df.rename(columns=condo_df.iloc[0]).drop(condo_df.index[0])

    condo_df["Single-Family Detached"] = 0
    condo_df["Townhouse-Condo Attached"] = 1

    single_df = single_df[1:]
    condo_df = condo_df[1:]

    single_df = pd.concat([single_df, condo_df], ignore_index=True)

    single_df["City"] = city
    single_df["Month_num"] = month
    single_df["Month"] = months[month]
    single_df["Year"] = year
    single_df["Median"] = (
        single_df["Median Sales Price"]
        .apply(lambda x: x.replace("$", "").replace(",", ""))
        .astype("int32")
    )
    single_df["Average"] = (
        single_df["Average Sales Price"]
        .apply(lambda x: x.replace("$", "").replace(",", ""))
        .astype("int32")
    )
    cols = [
        "New Listings",
        "Closed Sales",
        "Days on Market Until Sale",
        "Inventory of Homes for Sale",
    ]
    single_df[cols] = single_df[cols].apply(pd.to_numeric, errors="coerce")
    single_df["Percent of Original List Price Received"] = single_df[
        "Percent of Original List Price Received"
    ].apply(pd.to_numeric, errors="coerce")
    single_df = single_df.fillna(0)
    return single_df


@st.cache(show_spinner=True, allow_output_mutation=True, suppress_st_warning=True)
def loadYearAndMonthData(city, city_codes_df, month, year, df):
    """
    Checking if city, month, year and house type combination exists in DataFrame.
    If yes, return df without changing.
    If no, add new row and return df.

    INPUT:
    city - srting
    city_codes_df - pandas DataFrame
    month - int, 1-12
    year - int, 2011-2021
    house_type - 0 if Single-Family Detached
                 1 if Townhouse-Condo Attached

    OUTPUT:
    df - pandas DataFrame

    """
    a = np.array([city, month, year])
    matches = df[(df[["City", "Month_num", "Year"]] == a).all(axis=1)]
    if matches.empty:
        new_df = loadCityData(city, city_codes_df, month, year)
        df = pd.concat([df, new_df], ignore_index=True)
    return df
