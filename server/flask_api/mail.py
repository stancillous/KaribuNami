# import smtplib, ssl

# # twoo lcvm faos mgkd

# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = "stancillousray@gmail.com"  # Enter your address
# receiver_email = "stancillousr@gmail.com"  # Enter receiver address
# password = input("Type your password and press enter: ")
# message = """\
# Subject: Hi there

# This message is sent from Python."""

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)


import secrets

token = secrets.token_urlsafe(32)
print(token)