import smtplib
from email.message import EmailMessage

def email_msg(subject=None, body=None, to=None):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        msg['from'] = 'DADDDYYYY'


        user = 'jarvis.prototype.V.1.0@gmail.com'
        password = 'rambjnqteladfllr'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        server.quit()
        return True
    except:
        return False




#email_msg(subject='PYTHON EMAIL', body='The python works brooo', to='adrianporteros24@gmail.com')

