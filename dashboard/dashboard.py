import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

day_hour_df = pd.read_csv("all_data.csv")
day_hour_df['date'] = pd.to_datetime(day_hour_df['dteday'])

def plot_monthly_rentals(year):
    monthly_rentals = day_hour_df[day_hour_df['date'].dt.year == year].groupby(pd.Grouper(key='date', freq='M'))['cnt_x'].sum()
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_rentals.index, monthly_rentals.values, marker='o', linewidth=2, color="#72BCD4")
    plt.title("Number of Orders per Month", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    st.pyplot(plt)
    plt.clf()  

def plot_seasonal_rentals():
    seasonal_rentals = day_hour_df.groupby('season_x')['cnt_x'].mean()
    plt.figure(figsize=(10, 6))
    plt.bar(seasonal_rentals.index, seasonal_rentals.values, color='skyblue')
    plt.title('Average Rentals by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Rentals')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()

def plot_daily_rentals(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_data = day_hour_df[(day_hour_df['date'] >= start_date) & (day_hour_df['date'] <= end_date)]
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_data['date'], filtered_data['cnt_x'])
    plt.title('Daily Bike Rentals')
    plt.xlabel('Date')
    plt.ylabel('Number of Rentals')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.clf()

def plot_yearly_rentals():
    yearly_rentals = day_hour_df.groupby(day_hour_df['date'].dt.year)['cnt_x'].sum()
    plt.figure(figsize=(12, 6))
    plt.bar(yearly_rentals.index, yearly_rentals.values)
    plt.title('Yearly Bike Rentals')
    plt.xlabel('Year')
    plt.ylabel('Number of Rentals')
    st.pyplot(plt)
    plt.clf()

def plot_weekday_weekend_rentals():
    weekday_rentals = day_hour_df[day_hour_df['workingday_x'] == 1]['cnt_x'].mean()
    weekend_rentals = day_hour_df[day_hour_df['workingday_x'] == 0]['cnt_x'].mean()
    plt.figure(figsize=(6, 6))
    plt.bar(['Weekday', 'Weekend'], [weekday_rentals, weekend_rentals])
    plt.title('Weekday vs. Weekend Rentals')
    plt.xlabel('Day')
    plt.ylabel('Average Rentals')
    st.pyplot(plt)
    plt.clf()

def plot_casual_vs_registered():
    plt.figure(figsize=(12, 6))
    plt.plot(day_hour_df['date'], day_hour_df['casual_x'], label='Casual')
    plt.plot(day_hour_df['date'], day_hour_df['registered_x'], label='Registered')
    plt.title('Casual vs. Registered Rentals')
    plt.xlabel('Date')
    plt.ylabel('Number of Rentals')
    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.clf()

st.title("Bike Rental Dashboard")
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a dashboard", 
                             ("Monthly Rentals", "Seasonal Rentals", 
                              "Daily Rentals", "Yearly Rentals", 
                              "Weekday vs Weekend Rentals", 
                              "Casual vs Registered Rentals"))

if options == "Monthly Rentals":
    year = st.sidebar.selectbox("Select Year", sorted(day_hour_df['date'].dt.year.unique()))
    plot_monthly_rentals(year)

elif options == "Seasonal Rentals":
    plot_seasonal_rentals()

elif options == "Daily Rentals":
    start_date = st.sidebar.date_input("Start Date", day_hour_df['date'].min())
    end_date = st.sidebar.date_input("End Date", day_hour_df['date'].max())
    plot_daily_rentals(start_date, end_date)

elif options == "Yearly Rentals":
    plot_yearly_rentals()

elif options == "Weekday vs Weekend Rentals":
    plot_weekday_weekend_rentals()

elif options == "Casual vs Registered Rentals":
    plot_casual_vs_registered()