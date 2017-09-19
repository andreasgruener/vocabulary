#!/usr/local/bin/python3

import sys 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Config import NOTIFICATION_SMTP_RCPT,NOTIFICATION_SMTP_SERVER,NOTIFICATION_SMTP_USER,NOTIFICATION_SMTP_PWD,NOTIFICATION_SMTP_FROM



def send_email_multipart(subject, body):

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



	html = "EMPTY"
	#part1 = MIMEText(html, "html")
	part2 = MIMEText(body, "plain")

	#msg.attach(part1)    
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
		# print("##### INFO END")

	richtigeFragenText = ""
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
		# print("##### INFO END")

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

	print(info)
	asciimail = info # info.encode('ascii')
	#send_email("Vokabeltrainer :: Note %s ( %s / %s )" % (note, gesamt,falsch), asciimail)
	send_email_multipart("Vokabeltrainer :: Note %s ( %s / %s )" % (note, gesamt,falsch), info)

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