#!/usr/bin/python3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import time
import imaplib
import email
import email.parser
import email.policy
import html2text
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

IMAP_SERVER = os.environ.get("IMAP_SERVER")
IMAP_LOGIN = os.environ.get("IMAP_LOGIN")
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD")
NIC_MD_EMAIL = os.environ.get("NIC_MD_EMAIL")
NIC_MD_PASSWORD = os.environ.get("NIC_MD_PASSWORD")
NIC_MD_TLD = os.environ.get("NIC_MD_TLD")
NIC_MD_NS3_HOST = os.environ.get("NIC_MD_NS3_HOST")
NIC_MD_NS3_IP = os.environ.get("NIC_MD_NS3_IP")
NIC_MD_NS4_HOST = os.environ.get("NIC_MD_NS4_HOST")
NIC_MD_NS4_IP = os.environ.get("NIC_MD_NS4_IP")
HEADLESS = os.environ.get("HEADLESS")


def search_imap():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(IMAP_LOGIN, IMAP_PASSWORD)
    mail.list()
    mail.select('Inbox')  # specify inbox
    typ, [data] = mail.search(None, "UNSEEN")
    #    typ, [data] = mail.search(None, "(ALL)")

    for num in data.split():
        # fetch whole message as RFC822 format
        result, d = mail.fetch(num, "(RFC822)")
        msg = email2Text(d[0][1])
        text = msg["body"].encode('cp932', 'replace').decode('cp932')

        up_to_word = "torul cod:"
        x = text.find(up_to_word)
        y = text[x:2000].find(":")
        z = text[x + y + 1:2000]
        f = z[0:6]
        # print(f+"$")

    mail.close()
    mail.logout()

    return f


def email2Text(rfc822mail):
    msg_data = email.message_from_bytes(rfc822mail, policy=email.policy.default)

    mail_value = {}

    mail_value["from"] = header_decode(msg_data.get('From'))
    mail_value["date"] = header_decode(msg_data.get('Date'))
    mail_value["subject"] = header_decode(msg_data.get('Subject'))

    mail_value["body"] = ""
    if msg_data.is_multipart():
        for part in msg_data.walk():
            ddd = msg2bodyText(part)
            if ddd is not None:
                mail_value["body"] = mail_value["body"] + ddd
    else:
        ddd = msg2bodyText(msg_data)
        mail_value["body"] = ddd

    return mail_value


def msg2bodyText(msg):
    if msg.get_content_maintype() != "text":
        return None
    ddd = msg.get_content()

    if msg.get_content_subtype() == "html":
        try:
            ddd = html2text.html2text(ddd)
        except:
            print("error in html2text")
    return ddd


def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr

# Infinite loop, at the end of each iteration sleep for 24 hours
# while True:

service = FirefoxService(executable_path="/snap/bin/geckodriver", )
options = webdriver.FirefoxOptions()

if HEADLESS == 'true':
    options.add_argument("-headless")
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"), "Browser Headless mode. Just wait !!!")

browser = webdriver.Firefox(service=service, options=options)
browser.get('https://nic.md/ro/login2/')

time.sleep(6)
myLink = browser.find_element(By.PARTIAL_LINK_TEXT, 'Accept!')
time.sleep(3)
myLink.click()
time.sleep(3)

login = browser.find_element(By.CSS_SELECTOR, '[name="login_email"]')
login.send_keys(NIC_MD_EMAIL)
password = browser.find_element(By.CSS_SELECTOR, '[name="login_password"]')
password.send_keys(NIC_MD_PASSWORD)
time.sleep(1)
iframe = browser.find_element(By.XPATH,
                              '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/form/div[3]/div/div/div/div/iframe')
time.sleep(1)
browser.switch_to.frame(iframe)
time.sleep(1)
capcha = browser.find_element(By.CSS_SELECTOR, '.recaptcha-checkbox-border')
capcha.click()
time.sleep(4)
browser.switch_to.default_content()
time.sleep(1)
submit = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
time.sleep(1)
submit.click()

browser.get('https://nic.md/ro/nameservers/' + NIC_MD_TLD)
time.sleep(4)

ns3 = browser.find_element(By.ID, 'ns3_host')
ns3value = ns3.get_attribute("value")

if not ns3value:
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"), "ns3 empty")
    ns3 = browser.find_element(By.ID, 'ns_more')
    ns3.click()
    time.sleep(3)

    ns3 = browser.find_element(By.ID, 'ns3_host')
    ns3.clear()
    ns3.send_keys(NIC_MD_NS3_HOST)

    ns3ip = browser.find_element(By.ID, 'ns3_ip')
    ns3ip.click()
    ns3ip.clear()
    ns3ip.send_keys(NIC_MD_NS3_IP)

    ns4 = browser.find_element(By.ID, 'ns4_host')
    ns4.clear()
    ns4.send_keys(NIC_MD_NS4_HOST)

    ns4ip = browser.find_element(By.ID, 'ns4_ip')
    ns4ip.click()
    ns4ip.clear()
    ns4ip.send_keys(NIC_MD_NS4_IP)
    time.sleep(2)

    ns4ip = browser.find_element(By.ID, 'submit_button')
    ns4ip.click()
    time.sleep(20)

    input_code = browser.find_element(By.CSS_SELECTOR, 'input.form-control')
    input_code.click()
    cod = search_imap()
    time.sleep(4)
    input_code.send_keys(cod)
    time.sleep(10)

    finish = browser.find_element(By.ID, 'submit_button')
    finish.click()
    print("Update ns3 and ns4 successfully !!!")
    time.sleep(20)
else:
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"), "ns3 value is: " + ns3value)

browser.quit()
now = datetime.now()
print(now.strftime("%d/%m/%Y %H:%M:%S"), "Browser was closed !!!  Sleep for 24 hours  ")

#    time.sleep(86400)
