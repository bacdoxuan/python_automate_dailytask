import sqlite3
import os
import time
import datetime
import logging

# Configure logging
log_folder = os.path.dirname(__file__)
log_file = os.path.join(log_folder, "run_daily_report_with_log.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Database files
db_3G_cell = "c:\\Bac.DX\\SQLite\\DataBase\\2025_3G Cell HS USER TP.db3"
db_3G_site = "c:\\Bac.DX\\SQLite\\DataBase\\2025_3G Site traffic Utilization.db3"
db_4G_cell = "c:\\Bac.DX\\SQLite\\DataBase\\2025_4G Cell User Throughput.db3"
db_4G_site = "c:\\Bac.DX\\SQLite\\DataBase\\2025_4G site traffic Utilization.db3"

# Database - SQL - CSV
database_sql_csv = [
    # 3G cell
    (db_3G_cell, "3G_User_TP_Nation.sql", "3G_User_TP_Nation.csv"),
    (db_3G_cell, "3G_User_TP_Zone.sql", "3G_User_TP_Zone.csv"),
    (db_3G_cell, "3G_CS_Traffic.sql", "3G_CS_Traffic.csv"),
    (db_3G_cell, "3G_Traffic_By_Layer.sql", "3G_Traffic_By_Layer.csv"),
    # 3G Site
    (db_3G_site, "3G_Utilization_Province.sql", "3G_Utilization_Province.csv"),
    (db_3G_site, "3G_Utilization_Region.sql", "3G_Utilization_Region.csv"),
    (db_3G_site, "3G_Utilization_Zone.sql", "3G_Utilization_Zone.csv"),
    (db_3G_site, "3G_Utilization_Nation.sql", "3G_Utilization_Nation.csv"),
    (db_3G_site, "3G_Traffic_Cap.sql", "3G_Traffic_Cap.csv"),
    (db_3G_site, "3G_Traffic_Compare.sql", "3G_Traffic_Compare.csv"),
    (db_3G_site, "3G_Check_No_Carrier.sql", "3G_Check_No_Carrier.csv"),
    # 4G Cell
    (db_4G_cell, "4G_Traffic_By_Layer.sql", "4G_Traffic_By_Layer.csv"),
    (db_4G_cell, "4G_User_TP_Nation.sql", "4G_User_TP_Nation.csv"),
    (db_4G_cell, "4G_User_TP_Zone.sql", "4G_User_TP_Zone.csv"),
    # 4G Site
    (db_4G_site, "4G_Utilization_Nation.sql", "4G_Utilization_Nation.csv"),
    (db_4G_site, "4G_Utilization_Province.sql", "4G_Utilization_Province.csv"),
    (db_4G_site, "4G_Utilization_Region.sql", "4G_Utilization_Region.csv"),
    (db_4G_site, "4G_Utilization_Zone.sql", "4G_Utilization_Zone.csv"),
    (db_4G_site, "4G_Traffic_Compare.sql", "4G_Traffic_Compare.csv"),
    (db_4G_site, "4G_Traffic_Cap.sql", "4G_Traffic_Cap.csv"),
    (db_4G_site, "4G_Check_No_Carrier.sql", "4G_Check_No_Carrier.csv"),
    # Add more information about physical site by frequency layers - Province and Zone level
    (db_3G_cell, "3G_Physical_Site_by_Province.sql", "3G_Physical_Site_by_Province.csv"),
    (db_3G_cell, "3G_Physical_Site_by_Zone.sql", "3G_Physical_Site_by_Zone.csv"),
    (db_4G_cell, "4G_Physical_Site_by_Province.sql", "4G_Physical_Site_by_Province.csv"),
    (db_4G_cell, "4G_Physical_Site_by_Zone.sql", "4G_Physical_Site_by_Zone.csv"),
    # Add more information about 3G and 4G carrier configuration
    (db_3G_cell, "3G_carrier_config.sql", "3G_carrier_config.csv"),
    (db_4G_cell, "4G_carrier_config.sql", "4G_carrier_config.csv"),
    # 3G and 4G site configuration
    (db_3G_cell, "3G_Site_config.sql", "3G_Site_config.csv"),
    (db_4G_cell, "4G_Site_config.sql", "4G_Site_config.csv"),
    # 3G and 4G User and Throughput by Province
    (db_3G_cell, "3G_User_TP_Province.sql", "3G_User_TP_Province.csv"),
    (db_4G_cell, "4G_User_TP_Province.sql", "4G_User_TP_Province.csv"),
]


# Function to import SQL query
def get_sql_query(file_name):
    logging.info("Trying to open file to get SQL query: %s", file_name)
    sql_text = ""
    try:
        with open(file_name, "r") as fo:
            sql_text = fo.read()
    except Exception as e:
        logging.error("Error reading SQL file: %s", e)
    finally:
        logging.info("Finished opening file")
    return sql_text


# Function to connect to SQLite database and return a cursor
def connect_sqlite_db(db_name):
    logging.info("Trying to connect to database: %s", db_name)
    db_cursor = None
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
    except Exception as e:
        logging.error("Error connecting to database: %s", e)
    finally:
        logging.info("Finished connecting to database.")
    return db_cursor


# Function to save query result to a CSV file
def save_csv(query_result, file_name):
    logging.info("Saving query result to CSV file: %s", file_name)
    try:
        with open(file_name, "w") as fo:
            for line in query_result:
                fo.write(",".join(str(txt) for txt in line) + "\n")
    except Exception as e:
        logging.error("Error saving CSV file: %s", e)
    finally:
        logging.info("Finished saving CSV file.")


# A decorator to calculate time to run the program
def calculate_time(func):
    def inner():
        logging.info(
            "Program started at %s",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        start_time = time.time()
        func()
        end_time = time.time()
        logging.info(
            "Program ended at %s",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        run_time = round(end_time - start_time, 2)
        logging.info("Run time: %s seconds", run_time)

    return inner


# Main function, execute SQL with related database and save query result to a file
@calculate_time
def main() -> None:
    sql_folder = os.path.dirname(__file__)

    for item in database_sql_csv:
        # For each item in database_sql_csv, execute SQL query item[1] with database item[0] and save to CSV item[2]

        # Get path to SQL file
        sql_file = os.path.join(sql_folder, item[1])

        # Get path to save CSV file
        csv_file = os.path.join(sql_folder, item[2])

        logging.info("1 -- Connect to database --")
        cur = connect_sqlite_db(item[0])
        logging.info("-- Done --")

        logging.info("2 -- Get SQL text --")
        sql_text = get_sql_query(sql_file)
        logging.info("-- Done --")

        logging.info("3 -- Execute query --")
        query_result = cur.execute(sql_text).fetchall()
        logging.info("-- Done --")

        logging.info("4 -- Save CSV file --")
        save_csv(query_result, csv_file)
        logging.info("-- Done --")

        logging.info("5 -- Summary --")
        logging.info(
            "--> Database: %s\n--> Query: %s\n--> CSV: %s\n-- Finished --",
            item[0],
            item[1],
            item[2],
        )
        logging.info("*" * 100)


if __name__ == "__main__":
    main()