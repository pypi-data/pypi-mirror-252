import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
class Mail:
    def __init__(self, email, password, subject, csv_path, message):
        self.email = email
        self.password = password
        self.subject = subject
        self.csv_path = csv_path
        self.message = message
        self.df = pd.read_csv(self.csv_path)
    
    def Send(self):
        for i in range(self.df.shape[0]):
            msg = self.message.format(name=self.df[i][1])
            SendMail(self.df[i][0], self.subject, msg, self.email, self.password)

def SendMail(recipient_email, subject, message, gmail_user, gmail_app_password):
        # Compose the email
        message = MIMEMultipart()
        message['From'] = gmail_user
        message['To'] = recipient_email
        message['Subject'] = subject

        # Replace the placeholder in the message template with the recipient's name
        body = message
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server with a secure connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # Start TLS for security
            server.starttls()

            # Login to your Gmail account
            server.login(gmail_user, gmail_app_password)
            
            # Send the email
            server.sendmail(gmail_user, recipient_email, message.as_string())
            return f"Successfully sent e-mail to {recipient_email}!"