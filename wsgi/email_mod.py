#email module for registering users
import smtplib
import string
 


def fire_activate(username, email, oid):
	HOST = "smtp.gmail.com"
	SUBJECT = "Your application username activation"
	smtpuser = "stasiukpaul@gmail.com"
	smtppass = "tplzfbsjmgakigbq"
	TO =  email
	FROM = "newaccts@myapp.com"
	text = "Hi %s, you've signed up for our service. Please click this link: https://authframework-lucresearch.rhcloud.com/activate?oid=%s to activate your account!"%(username,oid)
	BODY = string.join((
        	"From: %s" % FROM,
        	"To: %s" % TO,
        	"Subject: %s" % SUBJECT ,
        	"",
        	text
        	), "\r\n")
	server = smtplib.SMTP(HOST,587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(smtpuser, smtppass)
	server.sendmail(FROM, [TO], BODY)
	server.quit()

def fire_pw_reset(username, email, oid):
        HOST = "smtp.gmail.com"
        SUBJECT = "Your application username activation"
        smtpuser = "stasiukpaul@gmail.com"
        smtppass = "tplzfbsjmgakigbq"
        TO =  email
        FROM = "newaccts@myapp.com"
        text = "Hi %s, you've asked to have your password reset. Please click this link: https://authframework-lucresearch.rhcloud.com/forgot/reset?oid=%s to reset your password account!"%(username,oid)
        BODY = string.join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "Subject: %s" % SUBJECT ,
                "",
                text
                ), "\r\n")
        server = smtplib.SMTP(HOST,587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtpuser, smtppass)
        server.sendmail(FROM, [TO], BODY)
        server.quit()


