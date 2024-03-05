import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


st.title("Proyek Analisis Data: Bike Sharing Dataset")
st.header("Syukri Arif Rafhida M001D4KY2978")

cur_path = os.getcwd()
df_path = os.path.join(cur_path, "hour.csv")

df = pd.read_csv(df_path)
df.head()
df["temp"] = df["temp"]*41  
df["atemp"] = df["atemp"]*50
df["hum"] = df["hum"]*100
df["windspeed"] = df["windspeed"]*67 

for i in range(len(df)):
    jam = int(df.loc[i, "hr"])
    if 9 <= jam <= 17:
        df.loc[i, "hr_class"] = 0 #bekerja
    elif 1 <= jam <= 8:
        df.loc[i, "hr_class"] = 2 #tidur
    else:
        df.loc[i, "hr_class"] = 1 #istirahat


st.subheader("Bagaimana Pengaruh Hari?")
col1, col2 = st.columns([1.6,1])

with col1:
    df_mean_byweek = df.groupby(by="weekday").agg({
        "casual": "mean",
        "registered" : "mean",
        "cnt": 'mean'})

    df_mean_byweek.plot(kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e', '#2ca02c'])

    plt.xlabel('Hari')
    plt.ylabel('Rata-Rata Peminjaman')
    plt.title('Rata-Rata Peminjaman Sepeda per-Hari')
    plt.xticks([0,1,2,3,4,5,6],["Minggu","Senin","Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],rotation=0)
    plt.legend(["Casual", "Registered", "Total"])

    st.pyplot(plt.gcf())

with col2:
    df_prop_workday = df.groupby(by="workingday").agg({
        "cnt": 'sum'
    })

    plt.pie(df_prop_workday["cnt"],autopct='%1.1f%%')

    plt.title('Total Peminjaman Sepeda Di Hari Libur dan Kerja')
    plt.legend(["Hari Libur", "Hari Kerja"])
    st.pyplot(plt.gcf())




st.subheader("Bagaimana Pengaruh Jam?")
col1, col2=st.columns([0.95,1])
with col1:
    df_worktime = df.groupby(by="hr_class").agg({
    "casual": "mean",
    "registered" : "mean",
    "cnt": 'mean'
    })
    df_worktime.plot(kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e', '#2ca02c'])

    plt.xlabel('Hari')
    plt.ylabel('Rata-Rata Peminjaman')
    plt.title('Rata-Rata Peminjaman Sepeda Per-Waktu')
    plt.xticks([0.0,1.0,2.0],["Waktu kerja\n09-16","Waktu istirahat\n17-00","Waktu tidur\n01-08"],rotation=0)
    plt.legend(["Casual", "Registered", "Total"])

    st.pyplot(plt.gcf())

with col2:
    df_sumhourly =  df.groupby(by="hr").agg({
        "cnt": 'sum'
    })

    df_sumhourly["cnt"].plot(kind='bar')
    
    plt.xlabel('Pukul')
    plt.ylabel('Total Peminjaman')
    plt.legend(["Total"])
    plt.title('Total Peminjaman Sepeda Per-Jam')
    st.pyplot(plt.gcf())

st.subheader("Bagaimana Pengaruh Musim?")
col1, col2=st.columns([1.6,1])
with col1:

    df_sumseason = df.groupby(by="season").agg({
        "cnt": 'sum'
    })
    plt.figure(figsize=(4,4))
    plt.pie(df_sumseason["cnt"],autopct='%1.1f%%')

    plt.title('Total Peminjaman Sepeda Di Tiap Musim')
    plt.legend(["Semi", "Panas", "Gugur", "Salju"])


    st.pyplot(plt.gcf())

st.subheader("Bagaimana Performa Per-Tahun?")
# Convert 'dteday' column to datetime format
df['dteday'] = pd.to_datetime(df['dteday'])


# Group data by month and calculate total count
df['month_year'] = df['dteday'].dt.to_period('M')
df_grouped = df.groupby('month_year')['cnt'].sum().reset_index()

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(df_grouped['month_year'].astype(str), df_grouped['cnt'])
plt.title('Total Peminjaman Sepeda Tiap Bulan')
plt.xlabel('Bulan')
plt.ylabel('Total Peminjaman')
plt.xticks(rotation=45)
st.pyplot(plt.gcf())

col1, col2=st.columns([1.6,1])
with col1:
    df_totalyear = df.groupby("yr")["cnt"].sum()

    plt.pie(df_totalyear,autopct='%1.1f%%')

    plt.title('Total Peminjaman Sepeda 2011 dan 2012')
    plt.legend(["2011", "2012"])
    st.pyplot(plt.gcf())
