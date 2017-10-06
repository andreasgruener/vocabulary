#!/usr/local/bin/python3

import sys 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..Config import NOTIFICATION_SMTP_RCPT,NOTIFICATION_SMTP_SERVER,NOTIFICATION_SMTP_USER,NOTIFICATION_SMTP_PWD,NOTIFICATION_SMTP_FROM



css = """
<style type="text/css">
body {
	font: normal 11px auto "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
	color: #4f6b72;
	background: #E6EAE9;
}

a {
	color: #c75f3e;
}

#mytable {
	width: 700px;
	padding: 0;
	margin: 0;
}

caption {
	padding: 0 0 5px 0;
	width: 700px;	 
	font: italic 11px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
	text-align: right;
}

th {
	font: bold 11px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
	color: #4f6b72;
	border-right: 1px solid #C1DAD7;
	border-bottom: 1px solid #C1DAD7;
	border-top: 1px solid #C1DAD7;
	letter-spacing: 2px;
	text-transform: uppercase;
	text-align: left;
	padding: 6px 6px 6px 12px;
	background: #CAE8EA url(images/bg_header.jpg) no-repeat;
}

th.nobg {
	border-top: 0;
	border-left: 0;
	border-right: 1px solid #C1DAD7;
	background: none;
}

td {
	border-right: 1px solid #C1DAD7;
	border-bottom: 1px solid #C1DAD7;
	background: #fff;
	padding: 6px 6px 6px 12px;
	color: #4f6b72;
}


td.alt {
	background: #F5FAFA;
	color: #797268;
}

th.spec {
	border-left: 1px solid #C1DAD7;
	border-top: 0;
	background: #fff url(images/bullet1.gif) no-repeat;
	font: bold 10px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
}

th.specalt {
	border-left: 1px solid #C1DAD7;
	border-top: 0;
	background: #f5fafa url(images/bullet2.gif) no-repeat;
	font: bold 10px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif;
	color: #797268;
}
</style>
"""
css1 = """
<style type="text/css">
table a:link {
	color: #666;
	font-weight: bold;
	text-decoration:none;
}
table a:visited {
	color: #999999;
	font-weight:bold;
	text-decoration:none;
}
table a:active,
table a:hover {
	color: #bd5a35;
	text-decoration:underline;
}
table {
	font-family:Arial, Helvetica, sans-serif;
	color:#666;
	font-size:12px;
	text-shadow: 1px 1px 0px #fff;
	background:#eaebec;
	margin:20px;
	border:#ccc 1px solid;

	-moz-border-radius:3px;
	-webkit-border-radius:3px;
	border-radius:3px;

	-moz-box-shadow: 0 1px 2px #d1d1d1;
	-webkit-box-shadow: 0 1px 2px #d1d1d1;
	box-shadow: 0 1px 2px #d1d1d1;
}
table th {
	padding:21px 25px 22px 25px;
	border-top:1px solid #fafafa;
	border-bottom:1px solid #e0e0e0;

	background: #ededed;
	background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#ebebeb));
	background: -moz-linear-gradient(top,  #ededed,  #ebebeb);
}
table th:first-child {
	text-align: left;
	padding-left:20px;
}
table tr:first-child th:first-child {
	-moz-border-radius-topleft:3px;
	-webkit-border-top-left-radius:3px;
	border-top-left-radius:3px;
}
table tr:first-child th:last-child {
	-moz-border-radius-topright:3px;
	-webkit-border-top-right-radius:3px;
	border-top-right-radius:3px;
}
table tr {
	text-align: center;
	padding-left:20px;
}
table td:first-child {
	text-align: left;
	padding-left:20px;
	border-left: 0;
}
table td {
	padding:18px;
	border-top: 1px solid #ffffff;
	border-bottom:1px solid #e0e0e0;
	border-left: 1px solid #e0e0e0;

	background: #fafafa;
	background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
	background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);
}
table tr.even td {
	background: #f6f6f6;
	background: -webkit-gradient(linear, left top, left bottom, from(#f8f8f8), to(#f6f6f6));
	background: -moz-linear-gradient(top,  #f8f8f8,  #f6f6f6);
}
table tr:last-child td {
	border-bottom:0;
}
table tr:last-child td:first-child {
	-moz-border-radius-bottomleft:3px;
	-webkit-border-bottom-left-radius:3px;
	border-bottom-left-radius:3px;
}
table tr:last-child td:last-child {
	-moz-border-radius-bottomright:3px;
	-webkit-border-bottom-right-radius:3px;
	border-bottom-right-radius:3px;
}
table tr:hover td {
	background: #f2f2f2;
	background: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#f0f0f0));
	background: -moz-linear-gradient(top,  #f2f2f2,  #f0f0f0);	
}
</style>
"""


def send_email_multipart(subject, body, htmlBody):

	mail_user = NOTIFICATION_SMTP_USER
	mail_pwd = NOTIFICATION_SMTP_PWD
	FROM = NOTIFICATION_SMTP_FROM
	TO = NOTIFICATION_SMTP_RCPT # if type(NOTIFICATION_SMTP_RCPT) is list else [NOTIFICATION_SMTP_RCPT]
	SUBJECT = subject
	print("Connect to " + NOTIFICATION_SMTP_SERVER)
	# Prepare actual message
	msg = MIMEMultipart("alternative")
	msg.set_charset("utf-8")

	msg["Subject"] = SUBJECT
	msg["From"] = FROM
	msg["To"] = TO

	part1 = MIMEText(body, "plain")
	part2 = MIMEText(htmlBody, "html")

	msg.attach(part1)    
	msg.attach(part2)

	#message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	#""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP_SSL(NOTIFICATION_SMTP_SERVER, 465)
		# server.set_debuglevel(self, True)
		# server.ehlo()
		# print(server.ehlo_resp)
		# server.starttls()
		server.login(mail_user, mail_pwd)
		server.sendmail(FROM, TO, msg.as_string())
		server.close()
		print('successfully sent the mail')
	except:
		print("failed to send mail")
		print(sys.exc_info())


def send_email(subject, body):
	import smtplib

	mail_user = NOTIFICATION_SMTP_USER
	mail_pwd = NOTIFICATION_SMTP_PWD
	FROM = NOTIFICATION_SMTP_FROM
	TO = NOTIFICATION_SMTP_RCPT if type(NOTIFICATION_SMTP_RCPT) is list else [NOTIFICATION_SMTP_RCPT]
	SUBJECT = subject
	TEXT = body
	print("Connect to " + NOTIFICATION_SMTP_SERVER)
	# Prepare actual message
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP_SSL(NOTIFICATION_SMTP_SERVER, 465)
		# server.set_debuglevel(self, True)
		# server.ehlo()
		# print(server.ehlo_resp)
		# server.starttls()
		server.login(mail_user, mail_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
		print('successfully sent the mail')
	except:
		print("failed to send mail")
		print(sys.exc_info())

def sendInfoMail(datum, start, ende, note, dauer, user, gesamt, falsch, frage_art, vokabel_datei, richtigeVokabeln, falscheVokabeln):

	falscheFragenText = ""
	falscheFragenTextHTML = "<table><tr><th>Frage</th><th>Antwort</th><th>Richtige Antwort</th></tr>"
	for frage in falscheVokabeln:
		# print("##### INFO")
		# print(frage["question"]) 
		# print(type(frage["question"]))
		# print(frage["answer"]) 
		# print(type(frage["answer"]))
		# print(frage["correctAnswer"])
		# print(type(frage["correctAnswer"]))
		# print("INFO")
		# print(frage["correctAnswer"])
		# print(type(frage["correctAnswer"][0]))

		frage_txt = frage["question"]
		answer_txt = frage["answer"]
		answer_correct = frage["correctAnswer"][0]

		# print(type(answer_correct))
		# print(answer_correct)
		falscheFragenText = falscheFragenText+"\n" +frage_txt + "\t:\t >" + answer_txt+  "< (Richtig: " + answer_correct + ")"
		falscheFragenTextHTML = falscheFragenTextHTML+"<tr><td>" +frage_txt + "</td><td>" + answer_txt+  "</td><td>" + answer_correct + "</td></tr>"
		
		# print("##### INFO END")

	if len(falscheFragenTextHTML) < 80:
		falscheFragenTextHTML = "<h3><i style=\"color: #00FF00 !important;\">Super - keine Fehler</i></h3>"	
	else:
		falscheFragenTextHTML = falscheFragenTextHTML+"</table>"


	richtigeFragenText = ""
	richtigeFragenTextHTML = "<table><tr><th>Frage</th><th>Antwort</th><th>Richtige Antwort</th></tr>"
	for frage in richtigeVokabeln:
		# print("##### INFO")
		# print(frage["question"]) 
		# print(type(frage["question"]))
		# print(frage["answer"]) 
		# print(type(frage["answer"]))
		# print(frage["correctAnswer"])
		# print(type(frage["correctAnswer"]))
		# print("INFO")
		# print(frage["correctAnswer"])
		# print(type(frage["correctAnswer"][0]))

		frage_txt = frage["question"]
		answer_txt = frage["answer"]
		answer_correct = frage["correctAnswer"][0]

		# print(type(answer_correct))
		# print(answer_correct)
		richtigeFragenText = richtigeFragenText+"\n" +frage_txt + "\t:\t >" + answer_txt+  "< (Richtig: " + answer_correct + ")"
		richtigeFragenTextHTML = richtigeFragenTextHTML+"<tr><td>" +frage_txt + "</td><td>" + answer_txt+  "</td><td>" + answer_correct + "</td></tr>"
		# print("##### INFO END")

	if len(richtigeFragenTextHTML) < 80:
		richtigeFragenTextHTML = "<h3><i style=\"color: #FF0000 !important;\">Leider keine richtigen Antworten</i></h3>"	
	else:
		richtigeFragenTextHTML = richtigeFragenTextHTML+"</table>"



#	print(falscheFragenText)
	info = (
		"Vokabeltrainer\n"
		"\n"
		"Gestartet am:\t"+datum+"\n"
		"Beginn:\t\t"+start+"\n"
		"Ende:\t\t"+ende+"\n"
		"Note:\t\t"+note+"\n"
		"Dauer:\t\t"+dauer+" Sekunden\n"
		"Benutzer:\t\t"+user+"\n"
		"Vokabeln:\t"+gesamt+"\n"
		"Davon Falsch:\t\t"+falsch+"\n"
		"Abfrageart:\t\t"+frage_art+"\n"
		"Vokabeldatei\t\t"+vokabel_datei+"\n"
		"\n"
	)
	info = info + "\nFalsch beantwortet:" + falscheFragenText + "\n\n\nRichtig beantwortet: " + richtigeFragenText

	infoHTML = (
	"<h1>Vokabeltrainer :: " + user + " :: " +frage_art + "</h1>"
	"<table>"
	"<tr><td>Gestartet am:</td><td><b>"+datum+ "</b></td></tr>"
	"<tr><td>Beginn:</td><td><b>"+start+ "</b></td></tr>"
	"<tr><td>Ende:</td><td><b>"+ende+ "</b></td></tr>"
	"<tr><td>Note:</td><td style=\"color: #FF0000 !important;\"><b>"+note+ "</b></td></tr>"
	"<tr><td>Dauer:</td><td><b>"+dauer+ " Sekunde/n</b></td></tr>"
	"<tr><td>Benutzer:</td><td><b>"+user+ "</b></td></tr>"
	"<tr><td>Vokabeln:</td><td><b>"+gesamt+ "</b></td></tr>"
	"<tr><td>Davon Falsch:</td><td><b>"+falsch+ "</b></td></tr>"
	"<tr><td>Abfrageart:</td><td><b>"+frage_art+ "</b></td></tr>"
	"<tr><td>Vokabeldatei</td><td><b>"+vokabel_datei+ "</b></td></tr>"
	"</table>"
	)
	infoHTML = css+ infoHTML + "<h2>Falsch beantwortet:</h2>" + falscheFragenTextHTML + "<h2>Richtig beantwortet:</h2> " + richtigeFragenTextHTML

	#send_email("Vokabeltrainer :: Note %s ( %s / %s )" % (note, gesamt,falsch), asciimail)
	send_email_multipart("Vokabeltrainer :: Note %s ( %s / %s )" % (note, gesamt,falsch), info, infoHTML)

def main(argv):
	richtigeVokabeln = []
	falscheVokabeln = []

	asked = { 'language' : "böse", 'question' :  "Abschluß", 'correctAnswer' : "correctAnswer", 'answer' :  "äüuß" }
	
	falscheVokabeln.append(asked)
	falscheVokabeln.append(asked)
	
	richtigeVokabeln.append(asked)
	
	sendInfoMail("datum", "start", "ende", "6", "1h", "user", "27", "12", "frage_art", "vokabel_datei", richtigeVokabeln, falscheVokabeln)



if __name__ == "__main__":
   main(sys.argv[1:])
   #testRuns()