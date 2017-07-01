#----------------------------------------------------------------------------------------------
# Name:        DaftAutomater.py
# Purpose:
#
# Author:      Daniel Maguire
#
# Created:     20/06/2016
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
#-----------------------------------------------------------------------------------------------

from datetime import datetime, timedelta
import imaplib
import email
import time
import thread
from selenium import webdriver

# # Read only emails from last 3 days
no_days_query = 3

server = "imap.gmail.com"
port_num = 993


def read_email(gmail_user, gmail_pwd):

    conn = imaplib.IMAP4_SSL(server, port_num)
    conn.login(gmail_user, gmail_pwd)
    conn.select()

    #Check status for 'OK'
    #status, all_folders = conn.list()
    #print all_folders
    folder_to_search = 'test'

    #Check status for 'OK'
    status, select_info = conn.select(folder_to_search)

    if status == 'OK':
        today = datetime.today()
        cutoff = today - timedelta(days=3)
        from_email = gmail_user
        search_key = from_email + " after:" + cutoff.strftime('%Y/%m/%d')
        status, message_ids = conn.search(None, 'X-GM-RAW', search_key)
        count = 0

        listOfLinks = []

        for id in message_ids[0].split():

            count+=1
            status, data = conn.fetch(id, '(RFC822)')
            email_msg = email.message_from_string(data[0][1])
            #Print all the Attributes of email message like Subject,
            #print email_msg.keys()
            subject = email_msg['Subject']
            print "------------------- Email",count, "------------------------"
            print subject

            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_content = part.get_payload() # prints the raw text
                    #TODO :
                    #process_email() #Delete email when link is aquired
                    list = CleanText(email_content)
                    link = findLink(list)
                    print "Link to property: ", link
                    listOfLinks.append(link)
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


def automator(url):
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # driver.set_page_load_timeout(30)
    print url
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(1)
    driver.find_element_by_id("your_name").send_keys("test")
    time.sleep(1)
    driver.find_element_by_id("your_email").send_keys("testtest.com")
    time.sleep(1)
    driver.find_element_by_id("your_phone").send_keys("test")
    time.sleep(1)
    driver.find_element_by_id("your_message").send_keys("test")
    time.sleep(1)
    driver.find_element_by_id("ad_reply_submit").click()
    time.sleep(1)
    #driver.get_screenshot_as_file("img.png")
    driver.quit()

def main():
    # Gmail Configuration

    gmail_user = raw_input("Enter gmail address: ")
    gmail_pwd = raw_input("Enter password: ")

    while True:
        list = read_email(gmail_user, gmail_pwd)
        print "\n\n-------------------------------------------------------------------"
        print "List of links:"
        #remove null entries from list
        list = filter(None, list)

        for links in range(len(list)):
            print "link: ",list[links]
            automator(str(list[links]))
        #sleep for 1 hour
        time.sleep(3600)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
