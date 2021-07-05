import smtplib
from email.message import EmailMessage

def email_msg(subject=None, body=None, to=None):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = 'DADDDYYYY'


    user = 'adrianporteros24@gmail.com'
    password = 'fqfqfmsvrysecdan'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

email_msg(subject='PYTHON EMAIL', body='The python works brooo', to='adrianporteros24@gmail.com')

