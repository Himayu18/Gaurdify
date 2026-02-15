import os
import sys 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import MailGuard_Service.mails as mails

mail = mails.emails("MailGuard_Service\\emails\\Greetings and Best Wishes.eml")
print(mail.detect_email())