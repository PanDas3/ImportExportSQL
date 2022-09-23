from sys import exc_info
from requests import get

from log import Log

class SMS():
    def __init__(self) -> None:
        self.log = Log()

    def send_sms(self, params, ok):
        sms = params["sms"]
        sms_tel = params["sms_tel"]
        sms_api = params["sms_api"]
        sms_ok = params["sms_ok"]
        sms_not_ok = params["sms_not_ok"]

        try:
            if(sms == True):
                if(ok == False):
                    for tel in sms_tel:
                        get(sms_api.format(number=tel, message=sms_ok))
                        self.log.info(f"Send SMS OK to {tel}")

                elif(ok != False):
                    for tel in sms_tel:
                        get(sms_api.format(number=tel, message=sms_not_ok))
                        self.log.info(f"Send SMS NOT OK to {tel}")

        except:
            self.log.error(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log