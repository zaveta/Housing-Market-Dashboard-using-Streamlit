import streamlit as st
import pandas as pd
import numpy as np
import datetime

import download_data as dd
import plotting as pl

city_codes_df = pd.read_csv('city_codes.csv')

columns = ['City', 'Townhouse-Condo Attached', 'Single-Family Detached',
           'New Listings', 'Pending Sales',
           'Closed Sales', 'Days on Market Until Sale', 'Median Sales Price',
           'Average Sales Price', 'Percent of Original List Price Received',
           'Inventory of Homes for Sale', 'Year', 'Month', 'Month_num']

df = pd.DataFrame(columns=columns)

num_to_month = {
    '01': "January",
    '02': "February",
    '03': "March",
    '04': "April",
    '05': "May",
    '06': "June",
    '07': "July",
    '08': "August",
    '09': "September",
    '10': "October",
    '11': "November",
    '12': "December"
}

month_to_num = {
    "January": '01',
    "February": '02',
    "March": '03',
    "April": '04',
    "May": '05',
    "June": '06',
    "July": '07',
    "August": '08',
    "September": '09',
    "October": '10',
    "November": '11',
    "December": '12'
}

# lists of cities, years and months
curr_year = datetime.datetime.now().today().year
cities_list = city_codes_df['city'].to_list()
years_list = list(range(2011, curr_year+1))
month_list = list(num_to_month.values())

st.sidebar.header('Options')

# coosen cities, years list and months
choosen_city = st.sidebar.selectbox("Choose city", (cities_list))
choosen_years = st.sidebar.multiselect("Choose year", years_list, default=years_list[-1])
choosen_months = st.sidebar.multiselect("Choose month", month_list, default="January")

house_type = st.sidebar.selectbox("Chose House Type", ("Single-Family Detached", "Townhouse-Condo Attached"))

st.title(choosen_city)

st.write('''This app shows the history of property price changes on the East Bay. 
            Data from [Market Statistics Monthly Stat Reports](https://ccartoday.com/market-statistics/)''')
try:
    for year in choosen_years:
        for mon_name in choosen_months:
            df = dd.loadYearAndMonthData(choosen_city, city_codes_df, month_to_num[mon_name], year, df)

    choosen_df = df[df["Year"].isin(choosen_years) &
                    df["Month"].isin(choosen_months) &
                    df["City"].isin([choosen_city]) &
                    df[house_type] == 1]


    choosen_df = choosen_df.sort_values("Year")

    st.table(choosen_df[['Year', 'Month', 'New Listings', 'Closed Sales',
                        'Days on Market Until Sale', 'Median Sales Price',
                        'Average Sales Price', 'Percent of Original List Price Received',
                        'Inventory of Homes for Sale']].transpose())

    avg_price_fig = pl.avg_price_fig(choosen_df)
    st.write(avg_price_fig)

    diff_price_fig = pl.diff_price_fig(choosen_df)
    st.write(diff_price_fig)

    new_listing_fig = pl.new_listing_fig(choosen_df)
    st.write(new_listing_fig)
except ValueError:
    st.write("Please choose year and month")


