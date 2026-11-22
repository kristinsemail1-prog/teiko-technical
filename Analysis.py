import sqlite3
import pandas as pd

DB = "teiko_analysis.db"

# Part 2: What is the frequency of each cell type in each sample?
Cell_Populations = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte"
]


def Summary():
    con = sqlite3.connect(DB)
    samples = pd.read_sql_query("select * from samples", con)
    summary_rows = []
    for _, row in samples.iterrows():
        total_count = sum(row[population] for population in Cell_Populations)
        for population in Cell_Populations:
            count = row[population]
            summary_rows.append({
                "sample": row["sample"],
                "total_count": total_count,
                "population": population,
                "count": count,
                "percentage": (count / total_count) * 100
            })
    summary = pd.DataFrame(summary_rows)
    summary.to_sql(
        "cell_frequency_summary",
        con,
        if_exists="replace",
        index=False
    )
    print(summary.head())
    con.commit()
    con.close()


Summary()

# Part 3
from scipy.stats import ttest_ind


def responder_analysis():
    con = sqlite3.connect(DB)
    samples = pd.read_sql_query("select * from samples", con)
    frequencies = pd.read_sql_query("select * from cell_frequency_summary", con)
    merged_data = samples.merge(frequencies, on="sample")
    merged_data = merged_data[
        (merged_data["condition"] == "melanoma") &
        (merged_data["treatment"] == "miraclib") &
        (merged_data["sample_type"] == "PBMC") &
        (merged_data["response"].isin(["yes", "no"]))
        ]  # since we only want to look at patients with a melanoma diagnosis, receiving miraclib, only looking at PBMC sample types
    statistics = []
    for population in Cell_Populations:
        responders = merged_data[(merged_data["population"] == population) &
                                 (merged_data["response"] == "yes")]["percentage"]
        nonresponders = merged_data[(merged_data["population"] == population) &
                                    (merged_data["response"] == "no")]["percentage"]

        responder_mean = responders.mean()
        non_responder_mean = nonresponders.mean()

        test_statistic, p_value = ttest_ind(
            responders,
            nonresponders,
            equal_var=False
        )

        statistics.append({
            "population": population,
            "responder_mean": responder_mean,
            "non_responder_mean": non_responder_mean,
            "p_value": p_value,
            "significant": p_value < 0.05
        })

    statistics_table = pd.DataFrame(statistics)

    merged_data.to_sql(
        "responder_comparison_data",
        con,
        if_exists="replace",
        index=False
    )

    statistics_table.to_sql(
        "responder_statistics",
        con,
        if_exists="replace",
        index=False
    )

    print(statistics_table)
    con.commit()
    con.close()

responder_analysis()

# Part 4
def subset_analysis():
    con = sqlite3.connect(DB)

    treatment_time_zero = pd.read_sql_query("""
        select * from samples
        where condition = "melanoma"
        and sample_type = "PBMC"
        and treatment = "miraclib"
        and time_from_treatment_start = 0
    """, con)

    project_counts = treatment_time_zero.groupby("project")["sample"].count().reset_index()
    project_counts.columns = ["project", "number_of_samples"]

    subjects = treatment_time_zero.drop_duplicates("subject")

    response_counts = subjects.groupby("response")["subject"].count().reset_index()
    response_counts.columns = ["response", "number_of_subjects"]

    sex_counts = subjects.groupby("sex")["subject"].count().reset_index()
    sex_counts.columns = ["sex", "number_of_subjects"]

    treatment_time_zero.to_sql(
        "treatment_time_zero",
        con,
        if_exists="replace",
        index=False
    )

    project_counts.to_sql(
        "project_counts",
        con,
        if_exists="replace",
        index=False
    )

    response_counts.to_sql(
        "response_counts",
        con,
        if_exists="replace",
        index=False
    )

    sex_counts.to_sql(
        "sex_counts",
        con,
        if_exists="replace",
        index=False
    )

    print(project_counts)
    print(response_counts)
    print(sex_counts)
    con.commit()
    con.close()

subset_analysis()