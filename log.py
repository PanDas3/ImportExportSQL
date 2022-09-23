from logging import getLogger
from logging import basicConfig
from logging import error
from logging import info
from logging import warning
from logging import ERROR
from logging import INFO
from logging import WARNING
from logging import DEBUG
from logging import exception
from time import strftime
from os import chdir, mkdir, path, getcwd
from re import compile, finditer

class Log():
    def __init__(self) -> None:
        self.root_path = getcwd()
        self.currentdate = strftime("%Y%m%d")
        self.log = getLogger("Logger")
        if(path.isdir("Logs") == False):
            mkdir("Logs")
        self.log_name = f"Logs\\ImportExportSQL_{self.currentdate}.log"

    def error(self, msg):
        self.log.setLevel(ERROR)
        basicConfig(filename=self.log_name, level=ERROR, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        error(msg)

    def info(self, msg):
        self.log.setLevel(INFO)
        basicConfig(filename=self.log_name, level=INFO, format="%(asctime)s \t %(levelname)s: \t\t %(message)s")
        info(msg)

    def warning(self, msg):
        self.log.setLevel(WARNING)
        basicConfig(filename=self.log_name, level=WARNING, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        warning(msg)

    def exception(self, msg):
        self.log.setLevel(DEBUG)
        basicConfig(filename=self.log_name, level=DEBUG, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        exception(msg)

    def search_error(self):
        chdir(self.root_path)
        pattern = compile("^.*(ERROR).*$")
        errors = []

        for i, line in enumerate(open(self.log_name, mode="r")):
            for match in finditer(pattern, line):
                errors.append("Line: %s - %s" % (i+1, match.group()))

            if(len(errors) == 0):
                return None

            else:
                string = """"""
                for error in errors:
                    string = f"""{string} <br /> {error}"""

                return string

    def __del__(self):
        del self.log
        del self.currentdate
        del self.root_path
        del self.currentdate