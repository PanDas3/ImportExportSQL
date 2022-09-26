from sys import exc_info
from os import getcwd, path
from gc import collect

from log import Log
from config import Configuration
from database import Database
from excel import Excel
from mail import SendMail
from sms import SMS

if(__name__ == "__main__"):
    log = Log()
    cfg = Configuration()
    db = Database()
    excel = Excel()
    smtp = SendMail()
    sms = SMS()

    log.info("##### Start Application #####")

    print("##########################")
    print("### Powered by Majster ###")
    print("##########################")

    file_config = path.join(getcwd(), "config.ini")
    try:
        cfg.check_config(file_config)
        cfg.read_config(file_config)
        cfg.validation_config()

        sql_params = cfg.get_sql_params()
        sql_params = cfg.secure_pass(file_config, sql_params)
        sql_params = cfg.decrypt_pass(sql_params)
        sms_params = cfg.get_sms_params()
        smtp_params = cfg.get_SMTP_params()

        if(sql_params["sql_mode"] == 'export'):
            export_params = cfg.get_export_params()

            conn = db.connect(sql_params) # return tuple (conn, engine)
            excel.export_excel(conn[0], export_params)

        elif(sql_params["sql_mode"] == 'import'):
            import_params = cfg.get_import_params() # if import mode = both return tuple(dict(replace and append) ? return tuple dict(replace or append))

            if(type(import_params) == dict):
                import_params = [import_params]

            elif(type(import_params) == tuple):
                import_params = list(import_params)

            for params in import_params:
                conn = db.connect(sql_params)
                db.sql_backup(conn[0], params)
                db.import_sql(conn[0], params)
                excel.import_excel(conn[0], params)

    except SystemExit:
        log.warning("!!! STOP SCRIPT !!!")

    except:
        log.error(exc_info()[:-1])

    finally:
        try:
            result = log.search_error()
            smtp.send_mail(smtp_params, result)
            sms.send_sms(sms_params, result)
            db.disconnect(conn[0], conn[1])

        except:
            pass

        log.info("##### End Application #####")
        print("##########################")
        print("### Powered by Majster ###")
        print("##########################")

        try:
            del sql_params
            del sms_params
            del smtp_params
            try:
                del conn
                try:
                    del export_params

                except:
                    try:
                        del import_params
                    
                    except:
                        pass
            except:
                pass

            finally:
                try:
                    del result
                
                except:
                    pass
        except:
            pass

        finally:
            del log
            del cfg
            del db
            del excel
            del smtp
            del sms

            collect()