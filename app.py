import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

DB = "teiko_analysis.db"
@st.cache_data
def create_database():
    os.system("python load_data.py")
    os.system("python Analysis.py")

create_database()


def read_table(table_name):
    con = sqlite3.connect(DB)
    data = pd.read_sql_query("select * from " + table_name, con)
    con.close()
    return data


st.title("Teiko Immune Cell Analysis")
st.write("Clinical trial cell population analysis")


# Part 2
st.header("Part 2: Cell Frequency by Sample")

summary = read_table("cell_frequency_summary")

sample_choice = st.selectbox(
    "Choose a sample",
    summary["sample"].unique()
)

selected_sample = summary[summary["sample"] == sample_choice]

st.dataframe(selected_sample)


# Part 3
st.header("Part 3: Miraclib Responders vs. Non-Responders")

comparison_data = read_table("responder_comparison_data")

figure, axis = plt.subplots(figsize=(12, 6))

comparison_data.boxplot(
    column="percentage",
    by=["population", "response"],
    ax=axis
)

axis.set_title("Cell Population Frequencies by Treatment Response")
axis.set_xlabel("Population and Response")
axis.set_ylabel("Relative Frequency (%)")

plt.suptitle("")

st.pyplot(figure)

st.subheader("Statistical Results")

statistics_table = read_table("responder_statistics")

st.dataframe(statistics_table)


# Part 4
st.header("Part 4: Melanoma PBMC Samples at Treatment Time 0")

treatment_time_zero = read_table("treatment_time_zero")

st.subheader("Qualifying Samples")
st.dataframe(treatment_time_zero)

st.subheader("Number of Samples by Project")
project_counts = read_table("project_counts")
st.dataframe(project_counts)

st.subheader("Number of Subjects by Response")
response_counts = read_table("response_counts")
st.dataframe(response_counts)

st.subheader("Number of Subjects by Sex")
sex_counts = read_table("sex_counts")
st.dataframe(sex_counts)