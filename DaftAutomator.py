#----------------------------------------------------------------------------------------------
# Name:        DaftAutomater.py
#
# Purpose:     Periodically checks daft.ie emails to see if a new property has been posted and
#              automatically emails the property contact with a pre-written message specified
#              by the user.
#
# Author:      Daniel Maguire
#
# Created:     20/06/2017
#
# Licence:     MIT License
#
#              Copyright (c) 2017 Daniel Maguire
#
#              Permission is hereby granted, free of charge, to any person obtaining a copy
#              of this software and associated documentation files (the "Software"), to deal
#              in the Software without restriction, including without limitation the rights
#              to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#              copies of the Software, and to permit persons to whom the Software is
#              furnished to do so, subject to the following conditions:
#
#              The above copyright notice and this permission notice shall be included in all
#              copies or substantial portions of the Software.
#
#              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#              SOFTWARE.
#
# Version:     Python 2.7
#-----------------------------------------------------------------------------------------------

from datetime import datetime, timedelta
import imaplib
import email
import time
from selenium import webdriver

#Read emails from last 3 days
no_days_query = 3

server = "imap.gmail.com"
port_num = 993

def read_email(gmail_user, gmail_pwd):

    conn = imaplib.IMAP4_SSL(server, port_num)
    conn.login(gmail_user, gmail_pwd)
    #create folder to archive emails in gmail if it does not exist yet
    archiveFolder = "DaftFolder"
    conn.create(archiveFolder)

    conn.select()

    #Check status for 'OK'
    status, all_folders = conn.list()
    #for items in all_folders:
        #print items
    folder_to_search = 'INBOX'

    #Check status for 'OK'
    status, select_info = conn.select(folder_to_search)

    if status == 'OK':
        today = datetime.today()
        #status, message_ids = conn.search(None, 'X-GM-RAW', search_key)
        status, message_ids = conn.search(None, 'from', '"noreply@daft.ie"')
        count = 0

        listOfLinks = []

        for id in message_ids[0].split():
            count+=1
            status, data = conn.fetch(id, '(RFC822)')
            email_msg = email.message_from_string(data[0][1])
            #print email_msg
            #Print all the Attributes of email message like Subject,
            #print email_msg.keys()
            subject = email_msg['Subject']
            print "------------------- Email",count, "------------------------"
            print subject

            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_content = part.get_payload() # prints the raw text
                    list = CleanText(email_content)
                    link = findLink(list)
                    print "Link to property: ", link
                    listOfLinks.append(link)

                    #Move email to daft archive folder to prevent duplicate emails being sent
                    print("Moving message " + subject + " to " + archiveFolder)
                    conn.store(id, '+X-GM-LABELS', archiveFolder)
                    conn.store(id, '+FLAGS', '\\Deleted')
                    conn.uid('STORE', id, '+FLAGS', '(\Deleted)')
                    conn.expunge()
        return listOfLinks
    else:
        print "Error"


def CleanText(raw_text):
    text_list = raw_text.split()
    tempword = ""
    check = False
    remove_list = []

    for word in range(len(text_list)):
        if check == True:
            #concatenate string
            text_list[word] = tempword + text_list[word]
            check = False
        if text_list[word].endswith('='):
            remove_list.append(text_list[word])
            #remove = from end of string
            tempword = text_list[word][:-1]
            #string needs to be concatenated with next string
            check = True

    for word in remove_list:
        if word in text_list:
            text_list.remove(word)

    return text_list


def findLink(text_list):
    for x in range(len(text_list)):
        if text_list[x] == 'advertiser' and text_list[x+1] == 'directly:':
            return text_list[x+2]


def automator(url, name, email, phone, message):
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.set_page_load_timeout(30)
    print url
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(1) #sleep to check if driver is performing task correctly
    driver.find_element_by_id("your_name").send_keys(name) #your name
    time.sleep(1)
    driver.find_element_by_id("your_email").send_keys(email) #your email
    time.sleep(1)
    driver.find_element_by_id("your_phone").send_keys(phone) #your_phone
    time.sleep(1)
    driver.find_element_by_id("your_message").send_keys(message) #message to landlord
    time.sleep(1)
    driver.find_element_by_id("ad_reply_submit").click()
    time.sleep(1)
    #driver.get_screenshot_as_file("img.png")
    driver.quit()

def main():
    # Gmail Configuration
    gmail_user = raw_input("Enter gmail address: ")
    gmail_pwd = raw_input("Enter password: ")
    print "---------------------Mandatory Info-----------------------------"
    name = raw_input("Name: ")
    phone_number = raw_input("Phone Number: ")
    message = raw_input("Message To Landlord: ")
    print message
    #time_check = raw_input("How often do you want to check for new ad? (1 = every min, 60 = every hour): ")

    while True:
        list = read_email(gmail_user, gmail_pwd)
        print "\n\n-------------------------------------------------------------------"
        print "List of links:"
        #remove null entries from list
        list = filter(None, list)

        for links in range(len(list)):
            print "link: ",list[links]
            automator(str(list[links]), name, email, phone_number, message)
        #sleep for 30 mins before checking again
        time.sleep(1800)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
