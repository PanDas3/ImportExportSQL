from sys import exc_info, exit
from urllib import parse
from sqlalchemy import create_engine, text
from datetime import datetime
from time import sleep
import sqlalchemy.sql.default_comparator
import pyodbc

from log import Log

class Database():
    def __init__(self) -> None:
        self.log = Log()

    def connect(self, params):
        odbc = params["sql_odbc"]
        server = params["sql_server"]
        port = params["sql_port"]
        db = params["sql_db"]
        trusted = params["sql_conn_trusted"]
        user = params["sql_user"]
        passwd = params["sql_pass"]

        try:
            if(trusted == True):
                connection_string = parse.quote_plus(f"DRIVER={odbc}; SERVER={server}; PORT={port}; Database={db}; Trusted_Connection=yes")
            elif(trusted == False):
                connection_string = parse.quote_plus(f"DRIVER={odbc}; SERVER={server}; PORT={port}; Database={db}; UID={user}; PWD={passwd}")

            db_conn = create_engine("mssql+pyodbc:///?odbc_connect={}".format(connection_string))
            conn = db_conn.connect()

            self.log.info(f"Connected to {server}")
            print(f"Connected to {server}")

            return conn, db_conn

        except:
            self.log.error(exc_info()[:-1])
            exit(1)

    def sql_backup(self, conn, params):
        table = params["sql_table"]
        today = datetime.now().strftime("%Y%m%d")
        table_backup = f"{table}-{today}"
        table_to_check = [table, table_backup]

        try:
            for table_check in table_to_check:
                sql_check_table = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME like N'%{table_check}%'"
                self.log.info("Checking SQL Table")
                result = conn.execute(text(sql_check_table))

                tab = []
                for row in result:
                    tab.append(row[0])

                count = len(tab)

                if((count == 0) and (table_to_check[0] == table_check)):
                    self.log.warning(f"Not found table {table_check} to backup")
                    self.log.warning("Next operation will be aborted")
                    exit(1)

                elif(table_to_check[1] == table_check):

                    if(count == 0):
                        self.log.info("No found table backup")

                    elif(count == 1):
                        self.log.info(f"Backup table {tab[0]} exists")
                        table_backup = f"{table_backup}_v{count}"

                    elif(count >= 2):
                        self.log.info(f"Backup table {tab[count-1]} exists")
                        table_backup = f"{table_backup}_v{count+1}"

            sql_query = f"""SELECT * INTO [dbo].[{table_backup}
            FROM [dbo].[{table}]
            COMMIT"""

            conn.execute(text(sql_query))
            self.log.info(f"Created new backup table {table_backup} from {table}")

        except SystemExit:
            exit(1)

        except:
            self.log.error(exc_info()[:-1])
            exit(1)

    def import_sql(self, conn, params):
        sql_type = params["sql_file_type"]
        try:
            if(sql_type == "sql"):
                sql_script = params["sql_script"]
                self.log.info("Import: Executing import from SQL file")
                print("Importing...")
                conn.execute(text(sql_script))
                print("Import completed")
                self.log.info("Import completed")

        except:
            self.log.error(exc_info()[:-1])
            exit(1)

    def disconnect(self, conn, db_conn):
        try:
            conn.close()
            db_conn.dispose()

            print("Closed connection with database...")
            self.log.info("Close connection with database")
            sleep(1.5)

        except:
            self.log.error(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log