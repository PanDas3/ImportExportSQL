from sys import exc_info
from pandas import read_excel, read_sql_query, read_sql_table, DataFrame, ExcelWriter
from sqlalchemy import text
import xlsxwriter

from log import Log

class Excel():
    def __init__(self) -> None:
        self.log = Log()

    def import_excel(self, conn, params):
        sql_type = params["sql_file_type"]

        try:
            if(sql_type == 'excel'):
                sql_table = params["sql_table"]
                sql_file = params["sql_file"]
                import_mode = params["import_mode"]

                self.log.info("Import: Read excel file to import")
                df = read_excel(sql_file)
                df.drop(df.columns[df.columns.str.contains('unamed', case=False)], axis = 1, inplace=True)
                print(df)

                self.log.info(f"Import: Import excel to SQL with mode: {import_mode}")
                print("Importing...")
                df.to_sql(sql_table, conn, schema="dbo", if_exists=import_mode, index=False, chunksize=800)
                print("Import completed")
                self.log.info("Import completed")

        except:
            self.log.error(exc_info()[:-1])
            exit(1)

    def export_excel(self, conn, params):
        export_type = params["sql_export_type"]
        output = params["excel_output"]

        try:
            if(export_type == 'table'):
                export_table = params["sql_table_export"]

                self.log.info("Export: Getting results from SQL by table")
                query = read_sql_table(export_table, conn)

            elif(export_type == 'script'):
                export_script = params["sql_script_export"]

                self.log.info("Export: Getting results from SQL by SQL")
                query = read_sql_query(export_script, conn)

            out_engine = ExcelWriter(output, engine="xlsxwriter")
            df = DataFrame(query)
            print(df)

            self.log.info(f"Export: Save results to excel - {output}")
            df.to_excel(out_engine, index=False)
            out_engine.close()

        except:
            self.log.error(exc_info()[:-1])
            exit(1)

    def __del__(self) -> None:
        del self.log