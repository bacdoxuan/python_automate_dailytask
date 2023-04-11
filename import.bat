echo Change Directory to SQLite 3 Folder
cd C:\Bac.DX\SQLite\sqlite-tools-win32-x86-3380200\
echo -------------------------------------------------------------------------

echo 1.Connect to "2023_3G Cell HS USER TP.db3"
sqlite3.exe "c:\Bac.DX\SQLite\DataBase\2023_3G Cell HS USER TP.db3"

echo import daily report data to database
.import --csv c:/Users/bac_dx/Desktop/3G_HS_User.csv DailyData
.quit
echo -------------------------------------------------------------------------

echo 2.Connect to "2023_3G Site traffic Utilization.db3"
sqlite3.exe "c:\Bac.DX\SQLite\DataBase\2023_3G Site traffic Utilization.db3"

echo import daily report data to database
.import --csv c:/Users/bac_dx/Desktop/3G_Site_Utilization.csv DailyData
.quit
echo -------------------------------------------------------------------------

echo 3.Connect to "2023_4G Cell User Throughput.db3"
sqlite3.exe "c:\Bac.DX\SQLite\DataBase\2023_4G Cell User Throughput.db3"

echo import daily report data to database
.import --csv c:/Users/bac_dx/Desktop/4G_Cell_TP.csv DailyData
.quit
echo -------------------------------------------------------------------------

echo 4.Connect to "2023_4G site traffic Utilization.db3"
sqlite3.exe "c:\Bac.DX\SQLite\DataBase\2023_4G site traffic Utilization.db3"

echo import daily report data to database
.import --csv c:/Users/bac_dx/Desktop/4G_Site_Util.csv DailyData
.quit
echo -------------------------------------------------------------------------

echo Finished importing data into databases