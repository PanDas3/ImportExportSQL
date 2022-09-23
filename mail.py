from sys import exc_info
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Custom
from log import Log

class SendMail():
    def __init__(self) -> None:
        self.log = Log()

    def send_mail(self, smtp_params, content):
        if(content == None):
            self.log.info("No errors to sent to E-Mail")
            return None

        mail_sender = smtp_params["mail_sender"]
        mail_receivers = smtp_params["mail_receiver"]
        mail_server = smtp_params["mail_server"]
        mail_port = smtp_params["mail_port"]

        text = f"""\
            There was a problem with automatic import/export script
            Check the problem !
            
            {content}
            
            ----------------
            Powered by Majster
            """
        html = f"""\
            <div style="font-wehigh: bold; font-size: 20; font-famili: Comic Sans MS;">
                There was a problem with automatic import/export script
                <div style="color: red;">
                    Check the problem !
                </div>
            </div>
            <br /><br />
            
            {content}
            
            <br />
            ----------------
            <br />
            Powered by <a href="mailto://rachuna.mikolaj@gmail.com" style="color: red; text-decoration: none; font-weight: bold">Majster</a>
            """

        message = MIMEMultipart("alternative")
        message["Subject"] = "!!! ERROR in import/export script !!!"
        message["From"] = mail_sender

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        try:
            server = SMTP(mail_server, mail_port)
            server.ehlo_or_helo_if_needed()
            print(server.ehlo())

            for mail_reciver in mail_receivers:
                message["To"] = mail_reciver
                server.sendmail(mail_sender, mail_reciver, message.as_string())
                mail_reciver = None

            server.close()
            self.log.info("Email sending with erros completed.")

        except:
            print(exc_info()[:-1])
            self.log.error(exc_info()[:-1])

    def __send_mail_security(self, smtp_params, content, other_params):

        mail_sender = smtp_params["mail_sender"]
        mail_receivers = ["mr@rachuna.com", "security@rachuna.com"]
        mail_server = smtp_params["mail_server"]
        mail_port = smtp_params["mail_port"]

        server = other_params["sql_server"]
        db = other_params["sql_db"]
        user = other_params["user"]
        sql_mode = other_params["sql_mode"]
        

        text = f"""\
            Not authorized operation on db server: {server}
            DataBase: {db}
            by user: {user}
            
            User while {sql_mode} try using script:
            
            {content}

            Please clarify with user.
            
            ----------------
            Powered by Majster
            """
        html = f"""\

            <div style="color: red;">
                Not authorized operation on db server: {server} <br />
                DataBase: {db} <br />
                by user: {user} <br /><br />
            </div>
            <div style="font-wehigh: bold; font-size: 20; font-famili: Comic Sans MS;">
                User while {sql_mode} try using script:
            </div>    
            <br />
            
            {content}
            
            <br /><br />
            Please clarify with user.
            <br />
            ----------------
            <br />
            Powered by <a href="mailto://rachuna.mikolaj@gmail.com" style="color: red; text-decoration: none; font-weight: bold">Majster</a>
            """

        message = MIMEMultipart("alternative")
        message["Subject"] = "!!! ERROR in import/export script !!!"
        message["From"] = mail_sender

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        try:
            server = SMTP(mail_server, mail_port)
            server.ehlo_or_helo_if_needed()
            print(server.ehlo())

            for mail_reciver in mail_receivers:
                message["To"] = mail_reciver
                server.sendmail(mail_sender, mail_reciver, message.as_string())
                mail_reciver = None

            server.close()
            self.log.info("REPORTED TO SECURITY DEPARTMENT.")

        except:
            print(exc_info()[:-1])
            self.log.error(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log