from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime
from email.message import EmailMessage

import smtplib
import requests
import os 

URL = "https://energie.be"
page = requests.get(URL) 

tarifs = []
soup = BeautifulSoup(page.content, "html.parser") 
dom = etree.HTML(str(soup))

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# You can also use the os library to get the env vars from your local machine
# sender = os.getenv("SENDER")
# sender_pwd = os.getenv("SENDER_PWD")
# recipient = os.getenv("recipient")

sender = "sender"
sender_pwd = "password"
recipient = "recipient"


def sendmail(sender, sender_pwd, recipient, email): 
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, sender_pwd)
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()


def main():

    for i in range(3): 
        i += 1
        tarifs.append(dom.xpath('/html/body/app-root/app-public-main/app-page-layout/div/main/div/app-home/div[4]/app-fair-price/app-home-card/div/div[2]/div/div/div/div/app-fair-price-item[{}]/div[3]'.format(i))[0].text.replace(",","."))
        tarifs[i-1] = float(tarifs[i-1]) / 100 
        tarifs[i-1] = str(tarifs[i-1])

    tarifs[1] = float(tarifs[1]) * 10.2
    tarifs[1] = str(tarifs[1])

    print("{}\
        \nDe prijs voor elektriciteit is € {} per kWh\
        \nDe prijs voor gas is € {} per m3\
        \nHet injectietarief is € {} per kWh"\
        .format(dt_string,tarifs[0].strip(),tarifs[1].strip(),tarifs[2].strip()))
    
    message = "{0}\
        \n\nDe prijs voor elektriciteit is € {1} per kWh\
        \nDe prijs voor gas is € {2} per m3\
        \nHet injectietarief is € {3} per kWh"\
        .format(dt_string,tarifs[0].strip(),tarifs[1].strip(),tarifs[2].strip())
    
    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Energie Prijzen"
    email.set_content(message)

    sendmail(sender, sender_pwd, recipient, email)

    

if __name__ == "__main__":
    main()