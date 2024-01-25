import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
class Mail:
    def __init__(self, email_address, spassword, ssubject, csv_path, message):
        self.email_a = email_address
        self.password = spassword
        self.subject = ssubject
        self.csv_path = csv_path
        self.message = message
        self.df = pd.read_csv(self.csv_path)
    
    def Send(self):
        for index, row in self.df.iterrows():
            msg = self.message.format(name=row[1])
            SendMail(row[0], self.subject, msg, self.email_a, self.password)

def SendMail(recipient_e, mail_subject, message_template, gmail_u, gmail_a):
        # Compose the email
        message = MIMEMultipart()
        message['From'] = gmail_u
        message['To'] = recipient_e
        message['Subject'] = mail_subject

        # Replace the placeholder in the message template with the recipient's name
        body = message_template
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server with a secure connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # Start TLS for security
            server.starttls()

            # Login to your Gmail account
            server.login(gmail_u, gmail_a)
            
            # Send the email
            server.sendmail(gmail_u, recipient_e, message.as_string())
