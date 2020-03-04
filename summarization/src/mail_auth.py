import smtplib
import time
import imaplib
import email
import csv


FROM_EMAIL = ""    # "pranjal.rai125@gmail.com"
FROM_PWD = ""   # "pgqtsvscwsfchzci"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail(email_id, password, no_of_mails):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(email_id, password)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        email_list = []
        cnt = 0

        for i in range(latest_email_id, first_email_id, -1):
            if cnt >= no_of_mails:
                break
            typ, data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    try:
                        msg = email.message_from_string(response_part[1].decode('utf-8'))
                    except Exception as e:
                        continue
                    email_subject = msg['subject']
                    email_from = msg['from']
                    current_email = []
                    current_email.append(email_subject)
                    current_email.append(email_from)
                    try:
                        email_message = msg.get_payload()
                        if isinstance(email_message, str):
                            current_email.append(email_message)
                            email_list.append(current_email)
                            cnt += 1
                            continue
                        entire_message = ""
                        for em in email_message:
                            entire_message += em
                        current_email.append(entire_message)
                        email_list.append(current_email)
                        cnt += 1
                    except Exception as e:
                        pass
        with open('mail_file.csv', mode='w') as mail_file:
            mail_writer = csv.writer(mail_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            mail_writer.writerow(['Subject', 'From', 'Message'])
            mail_writer.writerows(email_list)
            return mail_file


    except Exception as e:
        # pass
        print(str(e))


def get_mail_details(email_id, password, no_of_mails):
    read_email_from_gmail(email_id, password, no_of_mails)
