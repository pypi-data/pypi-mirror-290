from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from re import match
from sqlite3 import connect
from secrets import randbits
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

EMAIL_REGEX = r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}"

def microservice(service_name, service_domain, sendgrid_api_key):
    app = FastAPI()
    sender = f"{service_name} <no-reply@{service_domain}>"

    #
    # Put an email together in MIMEMultipart and send it off.
    #
    def send_email(recipient, subject, html, attachments=[]):
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(html, 'html'))
        for attachment in attachments:
            msg.attach(attachment)
        # Send it off via smtp.sendgrid.net
        with SMTP_SSL("smtp.sendgrid.net", 465) as smtp:
            smtp.login("apikey", sendgrid_api_key)
            smtp.sendmail(sender, recipient, msg.as_string())

    @app.post("/register", response_class=HTMLResponse)
    async def register(email: str = Form()):
        if not match(EMAIL_REGEX, email.upper()):
            return "<!doctype html><center><h1>Invalid email address.</h1></center>"

        check_email_html = f"""
            <!doctype html>
            <meta charset="UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <center>
                <h1>Check your email.</h1>
                <p>A confirmation link has been sent to {email}</p>
                <p>Please check your email and click on the link to confirm your details.</p>
                <p>If you don't see the email within a few minutes, please check your spam or junk folder.</p>
            </center>
        """

        # Set up DB
        connection = connect("registry.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS registry (email VARCHAR, code VARCHAR, confirmed BOOLEAN)")

        # Check if we already sent the confirmation email
        result = cursor.execute("SELECT 1 FROM registry WHERE email = ?", (email,))
        row = result.fetchone()
        if row is not None:
            connection.close()
            return check_email_html

        # We haven't already sent a confirmation email.

        # Create a confirmation code for the specified email address
        code = "%x" % randbits(128)
        cursor.execute("INSERT INTO registry (email, code, confirmed) VALUES (?, ?, FALSE)", (email, code))
        connection.commit()

        # Generate confirmation email
        confirmation_url = f"https://{service_domain}/confirm/{code}"
        mail_html = f"""
            <!doctype html>
            <p>Hi,</p>
            <p>To complete your registration and start using {service_name}
            with your website please confirm your email address by clicking the
            link below:</p>
            <p><a clicktracking="off" href="{confirmation_url}">{confirmation_url}</a></p>
            <p>If you didn't sign up for {service_name}, please ignore this email.</p>
            <p>Thank you!</p>
            <p>&mdash; The {service_name} Team</p>
        """
        subject = f"{service_name}: Please confirm your email address."
        send_email(email, subject, mail_html)

        # Close connection and display check email message
        connection.close()
        return check_email_html

    @app.get("/confirm/{code}", response_class=HTMLResponse)
    async def confirm(code):
        connection = connect("registry.db")
        cursor = connection.cursor()
        result = cursor.execute("UPDATE registry SET confirmed = TRUE WHERE code = ?", (code,))
        connection.commit()
        connection.close()
        if result.rowcount == 1:
            return f"""
                <!doctype html>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <center>
                    <h1>Email address confirmed.</h1>
                    <p>You can now use the {service_name} service.</p>
                </center>
            """
        return "<!doctype html><center><h1>Invalid code.</h1></center>"

    def registrations():
        connection = connect("registry.db")
        cursor = connection.cursor()
        for email in cursor.execute("SELECT email FROM registry WHERE confirmed = TRUE"):
            yield email
        connection.close()

    def is_confirmed(email):
        connection = connect("registry.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT 1 FROM registry WHERE email = ? AND confirmed = TRUE", (email,))
        row = result.fetchone()
        connection.close()
        return row is not None

    app.send_email = send_email
    app.registrations = registrations
    app.is_confirmed = is_confirmed

    return app
