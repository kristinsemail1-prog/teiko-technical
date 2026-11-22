import csv
import sqlite3 #https://docs.python.org/3/library/sqlite3.html this is the resource I used for sqlite

DB = "teiko_analysis.db"
CSV = "cell-count.csv"

def database(): #creates table
    con = sqlite3.connect(DB) #use sqlite to open/create db file
    cur = con.cursor()
    cur.execute("""create table if not exists samples (
        sample TEXT PRIMARY KEY,
        project TEXT,
        subject TEXT,
        condition TEXT,
        age INTEGER,
        sex TEXT,
        treatment TEXT,
        response TEXT,
        sample_type TEXT,
        time_from_treatment_start INTEGER,
        b_cell INTEGER,
        cd8_t_cell INTEGER,
        cd4_t_cell INTEGER,
        nk_cell INTEGER,
        monocyte INTEGER
        )
    """)

    con.commit()
    con.close()

def load_csv():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("delete from samples")
    with open(CSV, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("""
                        insert into samples (
                            project, subject, condition, age, sex, treatment, response,
                            sample, sample_type, time_from_treatment_start, b_cell,
                            cd8_t_cell, cd4_t_cell, nk_cell, monocyte
                        )
                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                row["project"],
                row["subject"],
                row["condition"],
                row["age"],
                row["sex"],
                row["treatment"],
                row["response"],
                row["sample"],
                row["sample_type"],
                row["time_from_treatment_start"],
                row["b_cell"],
                row["cd8_t_cell"],
                row["cd4_t_cell"],
                row["nk_cell"],
                row["monocyte"]
            ))

        con.commit()
        con.close()

database()
load_csv()