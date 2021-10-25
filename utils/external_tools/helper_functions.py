import csv
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Helper Functions 
def send_log_reports(logger):
		try:
			fileName = "utils/discord/last_tweets.csv"
			msg = EmailMessage()
			msg['Subject'] = "Log report for AllSeeBot bot - {0}".format(datetime.now())
			msg['From'] = os.getenv('BOT_MAIL')
			msg['To'] = "alberto.cruz6@upr.edu"
			msg.set_content('Body content')
			logs = ['searchbot.log', 'allSeeBot.log']
			
			# Attachments
			for log_file in logs:
				with open(log_file, 'rb') as f1:
					file_data = f1.read()
					file_name = f1.name
				msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)
			with open(fileName, 'rb') as csvfile:
				msg.add_attachment(csvfile.read(), maintype='application', subtype="octet-stream", filename='last_tweets.csv')

			# send
			with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
				smtp.login(os.getenv('BOT_MAIL'), os.getenv('BOT_MAIL_PASS'))
				smtp.send_message(msg)
		except Exception as e:
			print(e)
			print("Error! Couldn't send log report...- {0}".format(datetime.now()))
			logger.error(e)
			logger.error("Error! Couldn't send log report...- {0}".format(datetime.now()))