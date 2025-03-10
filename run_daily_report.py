import sqlite3
import os
import time
import datetime

# Database files
db_3G_cell = "c:\\Bac.DX\\SQLite\\DataBase\\2025_3G Cell HS USER TP.db3"
db_3G_site = "c:\\Bac.DX\\SQLite\\DataBase\\2025_3G Site traffic Utilization.db3"
db_4G_cell = "c:\\Bac.DX\\SQLite\\DataBase\\2025_4G Cell User Throughput.db3"
db_4G_site = "c:\\Bac.DX\\SQLite\\DataBase\\2025_4G site traffic Utilization.db3"

# Database - SQL - CSV
# A list of tuples contains 3 factors: database - sql to excecute - csv file to save query result
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
    # add more information about physical site by frequency layers - Province and Zone level
    (db_3G_cell, "3G_Physical_Site_by_Province.sql", "3G_Physical_Site_by_Province.csv"),
    (db_3G_cell, "3G_Physical_Site_by_Zone.sql", "3G_Physical_Site_by_Zone.csv"),
    (db_4G_cell, "4G_Physical_Site_by_Province.sql", "4G_Physical_Site_by_Province.csv"),
    (db_4G_cell, "4G_Physical_Site_by_Zone.sql", "4G_Physical_Site_by_Zone.csv"),
    # add more information about 3G and 4G carrier configuration
    (db_3G_cell, "3G_carrier_config.sql", "3G_carrier_config.csv"),
    (db_4G_cell, "4G_carrier_config.sql", "4G_carrier_config.csv"),
    # 3G and 4G site configuration
    (db_3G_cell, "3G_Site_config.sql", "3G_Site_config.csv"),
    (db_4G_cell, "4G_Site_config.sql", "4G_Site_config.csv"),
    # 3G and 4G User and Throughput by Province
    (db_3G_cell, "3G_User_TP_Province.sql", "3G_User_TP_Province.csv"),
    (db_4G_cell, "4G_User_TP_Province.sql", "4G_User_TP_Province.csv"),
]


# Function to import sql query
def get_sql_query(file_name):
    print("Try to open file to get sql query: {}".format(file_name))
    sql_text = ""
    try:
        fo = open(file_name, "r")
        sql_text = fo.read()
    except Exception as e:
        print(e)
    finally:
        print("End of opening file")
        fo.close()
    return sql_text


# Function to connect to sqlite database and return a cursor
def connect_sqlite_db(db_name):
    print("Try to connect to database {}".format(db_name))
    db_cursor = None
    try:
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
    except Exception as e:
        print(e)
    finally:
        print("Finish connecting.")
        # db_connection.close()
    return db_cursor


# function to save query result to a csv file
def save_csv(query_result, file_name):
    try:
        fo = open(file_name, "w")
        for line in query_result:
            fo.write(",".join(str(txt) for txt in line) + "\n")
    except Exception as e:
        print(e)
    finally:
        fo.close()


# a decorator to calculate time to run program
def calculate_time(func):
    def inner():
        print(
            "Program started at {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        start_time = time.time()
        func()
        end_time = time.time()
        print(
            "Program ended at {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        run_time = round(end_time - start_time, 2)
        print("Run time: {} seconds".format(run_time))
    return inner


# main function, excecute sql with related database and save query result to a file, in database_sql_csv list.
@calculate_time
def main() -> None:
    sql_folder = os.path.dirname(__file__)

    for item in database_sql_csv:
        # For each item in database_sql_csv, execute sql query item[1] with database item[0] and save to csv item[2]

        # Get path to sql file
        sql_file = os.path.join(sql_folder, item[1])

        # Get path to save csv file
        csv_file = os.path.join(sql_folder, item[2])

        print("1 -- Connect to database --")
        cur = connect_sqlite_db(item[0])
        print("-- Done --")

        print("2 -- Get sql text --")
        sql_text = get_sql_query(sql_file)
        print("-- Done --")

        print("3 -- Execute query --")
        query_result = cur.execute(sql_text).fetchall()
        print("-- Done --")

        print("4 -- Save csv file--")
        save_csv(query_result, csv_file)
        print("-- Done --")

        print("5 --Summary--")
        print(
            "--> Database:{}\n--> Query:{}\n--> Csv:{}\n-- Finished --".format(
                item[0], item[1], item[2]
            )
        )
        print("*" * 100)

    # for line in query_result:
    #     print(line)


if __name__ == "__main__":
    main()
