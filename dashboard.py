import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine

database_filepath = './Monthly_Stat_Reports.db'
engine = create_engine('sqlite:///{}'.format(database_filepath))
sqlite_connection = engine.connect()

cities_list = pd.read_sql_query('''
                                SELECT DISTINCT City FROM Monthly_Stat_Reports_Cities
                                ''', engine)['City'].to_list()

years_list = pd.read_sql_query('''
                                SELECT DISTINCT Year FROM Monthly_Stat_Reports_Cities
                                ''', engine)['Year'].to_list()
month_list = pd.read_sql_query('''
                                SELECT DISTINCT Month FROM Monthly_Stat_Reports_Cities
                                ''', engine)['Month'].to_list()


years_list.sort()
st.sidebar.header('Options')

city = st.sidebar.selectbox("Choose city", (cities_list))

years = st.sidebar.multiselect("Choose year", years_list, default=years_list[-1])

months = st.sidebar.multiselect("Choose month", month_list, default="January")

house_type = st.sidebar.selectbox("Chose House Type", ("Single-Family Detached", "Townhouse-Condo Attached"))

st.title(city)

table = pd.read_sql_query(f'''SELECT *
                              FROM Monthly_Stat_Reports_Cities
                              WHERE City = "{city}" 
                              AND "{house_type}" = 1
                              ORDER BY Year ASC, Month DESC
                              ''', engine)


choosen_df = table[table["Year"].isin(years) & table["Month"].isin(months)]

choosen_df["Date"] = choosen_df["Year"].apply(str) + " " + choosen_df["Month"]
choosen_df = choosen_df.sort_values("Month num")

st.table(choosen_df[['Date', 'New Listings', 'Closed Sales',
       'Days on Market Until Sale', 'Median Sales Price',
       'Average Sales Price', 'Percent of Original List Price Received',
       'Inventory of Homes for Sale']].transpose())

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=choosen_df, x='Date', y='New Listings', ax=ax, palette='OrRd')
plt.title("New Listings")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=choosen_df, x='Date', y='Median Sales Price', ax=ax, palette='OrRd')
plt.title("Median Sales Price")
plt.xticks(rotation=45)
st.pyplot(fig)

sqlite_connection.close()




