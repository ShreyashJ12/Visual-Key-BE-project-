import random
import string
import smtplib
import email.message

# ---------------------- Generate a OTP ---------------------
def rand_pass(size):
    # Takes random choices from
    # ascii_letters and digits
    generate_pass = ''.join([random.choice(string.ascii_uppercase +
                                           string.ascii_lowercase +
                                           string.digits)
                             for n in range(size)])

    return generate_pass


# Driver Code
OTP = rand_pass(8)
msg = "The OTP to change your password is: " + OTP
print(msg)


# ---------------------- Sending OTP via Email ---------------------

sender_add='no.reply.visualkey@gmail.com' # storing the sender's mail id
receiver_add='shreyash2jadhav1212@gmail.com' # storing the receiver's mail id
password='istujslyrbfnkrxe' # storing the password to log in

# creating the SMTP server object by giving SMPT server address and port number
smtp_server=smtplib.SMTP("smtp.gmail.com",587)
smtp_server.ehlo() # setting the ESMTP protocol

smtp_server.starttls() # setting up to TLS connection
smtp_server.ehlo() # calling the ehlo() again as encryption happens on calling startttls()

smtp_server.login(sender_add,password) # logging into out email id

# writing the message in HTML
html_msg="""From: ABC
To: XYZ
MIME-Version: 1.0
Content-type: text/html
Subject:Greetings
Hello! <br/><p align="center">Welcome to PythonGeeks.</p><hr/>"""

m = email.message.Message()
m['From'] = "no.reply.visualkey@gmail.com"
m['To'] = "shreyash2jadhav1212@gmail.com"
m['Subject'] = "Send mail from python!!"

m.set_payload(msg);


# sending the mail by specifying the from and to address and the message
smtp_server.sendmail(sender_add,receiver_add,m.as_string())
print('Successfully the mail is sent') # printing a message on sending the mail

smtp_server.quit()# terminating the server


a = input("Enter Your OTP >>: ")
if a == OTP:
    print("Verified")
else:
    print("Please Check your OTP again")