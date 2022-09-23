from configparser import ConfigParser, MissingSectionHeaderError
from sys import exc_info, exit
from shutil import rmtree
from os import path, getlogin
from configupdater import ConfigUpdater

# Custom
from log import Log
from mail import SendMail

class Configuration():
    def __init__(self) -> None:
        self.log = Log()
        self.smtp = SendMail()

    def read_config(self, config_name):
        try:
            config = ConfigParser()
            config.read(config_name)
            self.log.info("Read config.ini")

            # Read SQL
            self.sql_odbc = config["SQL"]["SQL_ODBC"]
            self.sql_server = config["SQL"]["SQL_Server"]
            self.sql_port = int(config["SQL"]["SQL_Port"])
            self.sql_db = config["SQL"]["SQL_DB"]
            self.sql_conn_trusted = config["SQL"]["SQL_Conn_Trusted"].lower()
            self.sql_user = config["SQL"]["SQL_User"]
            self.sql_pass = config["SQL"]["SQL_Pass"]
            self.sql_mode = config["SQL"]["SQL_Mode"].lower()

            # Read Export
            self.sql_table_export = config["Export"]["SQL_table_Name"]
            self.sql_script_export = config["Export"]["SQL_Script_File"]
            self.excel_output = config["Export"]["Excel_Output_File"]

            # Read Import
            self.import_mode = config["Import"]["Import_Mode"].lower()
            self.sql_table_override = config["Import"]["SQL_Tabke_Override"]
            self.sql_file_excel_override = config["Import"]["SQL_File_Excel_Override"]
            self.sql_table_append = config["Import"]["SQL_Table_Append"]
            self.sql_file_excel_append = config["Import"]["SQL_File_Excel_Append"]
            self.sql_file_append = config["Import"]["SQL_File_Append"]

            # Read Info
            self.sms = config["Info"]["SMS"].lower()
            self.sms_tel = config["Info"]["SMS_Tel"]
            self.sms_api = config["Info"]["SMS_API"]
            self.sms_ok = config["Info"]["SMS_OK"]
            self.sms_not_ok = config["Info"]["SMS_NOT_OK"]

            # Read Mail
            self.send_error = config["SMTP"]["Send_Errors"].lower()
            self.mail_sender = config["SMTP"]["Mail_Sender"]
            self.mail_receivers = config["SMTP"]["Mail_Receivers"].lower()
            self.mail_server = config["SMTP"]["Mail_Server"].lower()
            self.mail_port = int(config["SMTP"]["Mail_Port"])

        except AttributeError as err:
            self.log.error(f"Config Error: {err}")
        
        except UnicodeDecodeError as err:
            self.log.error(f"Config Error: {err}")
            self.log.warning(f"Config Error: Change file encode to ANSI")

        except MissingSectionHeaderError as err:
            self.log.error(f"Config Error: {err}")
        
        except KeyError as err:
            self.log.error(f"Config Error: {err}")

        except UnboundLocalError as err:
            self.log.error(f"Config Error: {err}")

        except ValueError as err:
            self.log.error(f"Config Error: {err}")
            self.log.warning(f"Complete the port numbers")
        
        except:
            print(exc_info())
            self.log.exception(exc_info()[:-1])
            exit(1)

    def validation_config(self):
        def str_to_bool(string):
            if(string == 'false'):
                string = bool(string)
                string = False

            elif(string == 'true'):
                string = bool(string)
                string = True
            
            else:
                string = bool(string)
                string = False

            return string

        self.log.info("Validation config.ini")

        # Change string to bool
        self.sql_conn_trusted = str_to_bool(self.sql_conn_trusted)
        self.sms = str_to_bool(self.sms)
        self.send_error = str_to_bool(self.send_error)

        self.mail_receivers = self.mail_receivers.replace(",", ", ").replace("  ", " ")
        self.mail_receivers = list(self.mail_receivers.split(", "))

        ok = True
        if((self.sql_server == "") or (self.sql_db == "")):
            self.log.error("LOGIC Error: Server name or database name is empty")
            ok = False

        if((self.sql_conn_trusted == False) and (self.sql_user == "" or self.sql_pass == "")):
            self.log.error("LOGIC Error: SQL User and/or password is empty")
            ok = False

        elif((self.sql_mode not in ['import', 'export']) == True):
            self.log.error(f"LOGIC Error: Incorect SQL_Mode: {self.sql_mode}")
            print((f"LOGIC Error: Incorect SQL_Mode: {self.sql_mode}"))
            self.log.warning(f"You have to choose type: Import or Export")
            print(f"You have to choose type: Import or Export")
            ok = False

        if(self.sql_mode == 'import'):
            if((self.import_mode not in ['replace','append','both']) == True):
                self.log.error(f"LOGIC Error: Incorect Import_Mode: {self.import_mode}")
                print((f"LOGIC Error: Incorect Import_Mode: {self.import_mode}"))
                self.log.warning(f"You have to choose type: Replace, Append or Both")
                print(f"You have to choose type: Replace, Append or Both")
                ok = False

            if((self.import_mode == 'replace' and self.sql_file_excel_override == "") or (self.sql_file_excel_append != "" and self.sql_file_append != "")):
                self.log.error("LOGIC Error: You cannot replace/append table by excel file and script sql")
                self.log.warning("You have to choose only one. The next one leave empty")
                self.log.warning("Problem are with params: SQL_File_Excel_Override, SQL_File_Excel_Append, SQL_File_Append")
                ok = False


            if((self.import_mode == 'replace' and self.sql_table_override == "") or (self.import_mode == 'append' and self.sql_table_append == "")):
                self.log.error("LOGIC Error: Table name is empty")
                self.log.warning("Complete correctly params: SQL_Table_Override/Append")
                ok = False

            if((self.import_mode == 'append') and (self.sql_file_excel_append == "" and self.sql_file_append == "")):
                self.log.error("LOGIC Error: The file to import is empty")
                self.log.warning("Complete correctly params: SQL_File_Excel_Append, SQL_File_Append")
                ok = False

            if(ok != False):
                self.log.info(f"SQL Mode: {self.sql_mode}")
                self.log.info(f"Import Mode: {self.import_mode}")

        elif(self.sql_mode == 'export'):
            if((self.sql_script_export == "" and self.sql_table_export == "") or (self.sql_script_export != "" and self.sql_table_export != "")):
                self.log.error("LOGIC Error: You cannot export table by excel file and script sql")
                self.log.warning("You have to choose only one. The next one leave empty")
                self.log.warning("Problem are with params: SQL_Script_File, SQL_Table_Name")
                ok = False
            
            if(self.excel_output == ""):
                self.log.error("LOGIC Error: Empty output file")
                self.log.warning("Complete correctly params: Excel_Output_File")
                ok = False

            if(ok != False):
                self.log.info(f"SQL Mode: {self.sql_mode}")

        if(ok == False):
            exit(1)

    def check_sql(self, file, not_alowed):
        self.log.info("Checking SQL file")
        other_params = {
            "user":f"{getlogin()}@rachuna.com",
            "sql_mode":self.sql_mode,
            "sql_server":self.sql_server,
            "sql_db":self.sql_db
        }

        try:
            with open(file, mode="r") as file:
                script = file.read().lower()
                file.close()

            ok = True
            for string in not_alowed:
                string = string.lower()
                if((string in script) == True):
                    ok = False

            if(ok == False):
                self.log.error("NOT ALOWED COMMAND IN SQL !")
                self.smtp.__send_mail_security(self.smtp_params, script, other_params)
                exit(1)

            else:
                self.log.info("SQL file is ok")
                # eliminate SQLAlchemy library problem when someone wrote "use [db]" in sql file
                script = script.replace("use ", "--use ")
                return script

        except SystemExit:
            exit(1)

        except FileNotFoundError as err:
            self.log.error(err)
            exit(1)

        except:
            self.log.error(exc_info()[:-1])
            exit(1)


    def get_sql_params(self):
        key = "WvZ-GMMj-6zDAGuemaPBLGcX9cDyNQwwpoulToBLGaQ="
        return {
                "sql_odbc":self.sql_odbc,
                "sql_server":self.sql_server,
                "sql_port":self.sql_port,
                "sql_db":self.sql_db,
                "sql_conn_trusted":self.sql_conn_trusted,
                "sql_user":self.sql_user,
                "sql_pass":self.sql_pass,
                "sql_mode":self.sql_mode,
                "key":key
                    }

    def get_export_params(self):
        params = {
            "excel_output":self.excel_output
        }

        if(self.sql_script_export == ""):
            params["sql_table_export"] = self.sql_table_export
            params["sql_export_type"] = "table"

        elif(self.sql_table_export == ""):
            not_alowed = ['insert', 'update', 'drop', 'delete', 'alter']
            try:
                result = self.check_sql(self.sql_script_export, not_alowed)
            
            except SystemExit:
                exit(1)

            except:
                self.log.error(exc_info()[:-1])

            params["sql_script_export"] = result
            params["sql_export_type"] = "script"

        return params

    def get_import_params(self):
        import_mode = None

        if(self.import_mode == 'both'):
            import_mode = 'replace'

        if(self.import_mode == 'replace' or import_mode == 'replace'):
            params_replace = {
                "import_mode":'replace',
                "sql_table":self.sql_table_override,
                "sql_file":self.sql_file_excel_override,
                "sql_file_type":"excel"
            }

            if(self.import_mode == "both"):
                import_mode = 'append'

            elif(self.import_mode == 'replace'):
                return params_replace

        if(self.import_mode == 'append' or import_mode == 'append'):

            params_append = {
                "import_mode":"append",
                "sql_table":self.sql_table_append
            }

            if(self.sql_file_excel_append != "" and self.sql_file_append == ""):
                params_append["sql_file"] = self.sql_file_excel_append
                params_append["sql_file_type"] = "excel"

            else:
                params_append["sql_file"] = self.sql_file_append
                params_append["sql_file_type"] = "sql"

            if(params_append["sql_file_type"] == "sql"):
                not_alowed = ["drop", "delete", "alter"]
                try:
                    result = self.check_sql(self.sql_file_append, not_alowed)
                    params_append["sql_script"] = result

                except SystemExit:
                    exit(1)

                except:
                    self.log.error(exc_info()[:-1])
                    exit(1)

            if(self.import_mode == 'both'):
                import_mode = 'both'

            elif(self.import_mode == 'append'):
                return params_append

        if(import_mode == 'both'):
            return params_append, params_replace

    def get_sms_params(self):
        return {
            "sms":self.sms,
            "sms_tel":self.sms_tel,
            "sms_api":self.sms_api,
            "sms_ok":self.sms_ok,
            "sms_not_ok":self.sms_not_ok
        }

    def get_SMTP_params(self):
        self.smtp_params = {
            "send_error":self.send_error,
            "mail_sender":self.mail_sender,
            "mail_receiver":self.mail_receivers,
            "mail_server":self.mail_server,
            "mail_port":self.mail_port,
        }

        return self.smtp_params
            
    def secure_pass(self, file_config, sql_params):
        if(self.sql_conn_trusted == False):
            sql_pass = sql_params["FTP_pass"]
            
            #
            # TOP SECRET
            #

            self.log.info("Checking SQL password")
            if((len_sql_pass > 0) and (len_sql_pass < 99)):

                update_config = ConfigUpdater()
                update_config.read(file_config)

                #
                # TOP SECRET
                #

                update_config["SQL"]["SQL_Pass"].value = sql_encrypt_pass
                update_config.update_file()
                self.log.info("Updated password in config.ini")

        return sql_params

    def decrypt_pass(self, sql_params):
        if(self.sql_conn_trusted == False):
            sql_pass = sql_params["sql_pass"]
            #
            # TOP SECRET
            #
                sql_params["sql_pass"] = sql_pass_decrypt

        return sql_params

    def check_config(self, file_config):

        default_cfg = """##############################################
############# POWERED BY MAJSTER #############
#### Automat do importu / exportu danych #####
##############################################

[SQL]
# Sterownik ODBC
SQL_ODBC = ODBC Driver 17 for SQL Server
# Instancja bazodanowa
SQL_Server = localhost
# Port
SQL_Port = 1433
# Baza
SQL_DB = 
# Poswiadczenia osoby wykonywujacej
SQL_Conn_Trusted = True
# Jezeli wyzej false to login i pass do uzytkownika SQL
SQL_User = 
SQL_Pass =
# Tryb pracy SQL: Import/Export
SQL_Mode = Export

[Export]
# Albo nazwa tabeli albo skrypt ./*.sql
# Nazwa tabeli
SQL_Table_Name =
# Skrypt z SELECT
SQL_Script_File = E:\Projekty\Python\ImportExportSQL\sql.sql
# Plik wynikowy
Excel_Output_File = E:\Projekty\Python\ImportExportSQL\output.xlsx

[Import]
# Tryb importowania (Replace/Append/Both)
Import_Mode = Append

# Nadpisanie (DROP AND APPEND DATA)
# Nazwa tabeli
SQL_Table_Override = 
# Plik Excel
SQL_File_Excel_Override =

# Dodanie (APPEND DATA)
# Albo plik Excel albo skrypt SQL
# Nazwa tabeli
SQL_Table_Append = 
# Plik Excel
SQL_File_Excel_Append =
# Skrypt SQL
SQL_File_Append =

[Info]
# Czy wyslac SMS o wykonaniu?
SMS = True
# Nr tel
SMS_Tel = 123456789, 987654321
# API SMS
SMS_API = http://rachuna.com/sms.php?tel_number=48{number}&message={message}
# Tresc SMS OK
SMS_OK = Automat MR: Skrypt wykonany prawidlowo
# Tresc SMS NIE OK
SMS_NOT_OK = Automat MR: BLAD !!! Skrypt potrzebuje recznej interwencji !!!!!

[SMTP]
# Czy wyslac maila o bledzie?
Send_Error = False
# Nadawca
Mail_Sender = Automat_MR@rachuna.com
# Odbiorcy
Mail_Receivers = mr@rachuna.com, security@rachuna.com
# Host SMTP
Mail_Server = smtp.rachuna.com
# Port SMTP
Mail_Port = 25"""

        try:
            open(file_config)

        except IOError:
            err = "Config Error: Not found config.ini or is demaged !"
            print(err)
            self.log.error(f"{err}")

            if(path.isfile(file_config)):
                rmtree(file_config)
                self.log.warning("Removed config.ini")
 
            with open(file_config, mode="w", encoding="ANSI") as default_config:
                default_config.write(default_cfg)
                default_config.close()
                
            self.log.warning("Created default config.ini")
            self.log.warning("Complete the config.ini")    

        except KeyError as err:
            print(err)
            self.log.error(f"Config Error: {err}")
            exit(1)

        except:
            print(exc_info())
            self.log.error(exc_info()[:-1])
            exit(1)

    def __del__(self) -> None:
        del self.log
        del self.smtp