# Program Name: Assignment5.py
# Course: IT3883 Course Section: W01 (85546)
# Student Name: Viktoriia Morozova
# Assignment Number: 5
# Due Date: Due on Nov 20, 2026
# Purpose: Load temperature readings into SQLite and display the
# average temperatures for Sunday and Thursday.
# Resources: Assignment 5 instructions, Module 5-2: Software Engineering Steps
import sqlite3
from contextlib import closing
from pathlib import Path


def main():
    input_path = Path(__file__).with_name("Assignment5input.txt")
    database_path = Path(__file__).with_name("Assignment5.db")

    with closing(sqlite3.connect(database_path)) as database:
        # Rebuild the dataset in one transaction so reruns don't duplicate readings.
        with database:
            database.execute("""
                CREATE TABLE IF NOT EXISTS temperatures (
                    ID INTEGER PRIMARY KEY,
                    Day_Of_Week TEXT NOT NULL,
                    Temperature_Value REAL NOT NULL
                )
            """)
            database.execute("DELETE FROM temperatures")

            # Read each temperature and insert it using SQL parameters.
            with input_path.open(encoding="utf-8") as input_file:
                for line in input_file:
                    if not line.strip():
                        continue
                    day, temperature = line.split()
                    database.execute(
                        """INSERT INTO temperatures (Day_Of_Week, Temperature_Value)
                           VALUES (?, ?)""",
                        (day, float(temperature)),
                    )

        # Let SQLite calculate one average per requested day.
        averages = database.execute("""
            SELECT Day_Of_Week, AVG(Temperature_Value)
            FROM temperatures
            WHERE Day_Of_Week IN (?, ?)
            GROUP BY Day_Of_Week
            ORDER BY Day_Of_Week
        """, ("Sunday", "Thursday"))

        for day, average in averages:
            print(f"{day}: {average:.2f}")


if __name__ == "__main__":
    main()
