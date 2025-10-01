import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from html_email.password import my_password

class HTMLEmail:
    """Initializes ezgmail"""
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

    def send_html_content(self, to_email, html_content, subject):
        """A method to send html email at the given address"""
        try:
            from_email = 'adityasalian865@gmail.com'    ## my email address
            app_password = my_password           ## my password

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(html_content, 'html'))  ## attaches html content

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()   
                server.login(from_email, app_password)
                server.send_message(msg)
            
            return 'Email sent successfully', None
        except Exception as exc:
            error = f'Failed to send email:\n{exc}'
            return None, error
        
if __name__=='__main__':
    email = HTMLEmail()
    success, error = email.send_html_content('adityasalian06@gmail.com', 'TEST', 'test')
    print(success)
    print(error)