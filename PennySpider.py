__author__ = 'orian'


from selenium import webdriver
import xml.etree.cElementTree as ET
from random import randint

import time

class PennySpider():

    __driver = webdriver.Firefox()


    def loginToPenny(self):

            self.__driver.maximize_window()
            self.__driver.get("https://forums.penny-arcade.com/")

            buttonSignInClass = "SignInPopup"
            buttonSignInElement = self.__driver.find_element_by_class_name(buttonSignInClass)
            buttonSignInElement.click()


            time.sleep(2)

            penny_username   = "avner"
            penny_password   = "avner123"

            emailFieldID     = "Form_Email"
            passFieldID      = "Form_Password"
            loginButtonID    = "Form_SignIn"

            emailFieldElement   = self.__driver.find_element_by_id(emailFieldID)
            passFieldElement    = self.__driver.find_element_by_id(passFieldID)
            loginButtonElement  = self.__driver.find_element_by_id(loginButtonID)

            emailFieldElement.clear()
            emailFieldElement.send_keys(penny_username)
            passFieldElement.clear()
            passFieldElement.send_keys(penny_password)

            loginButtonElement.click()

    def afterLogin(self):

        time.sleep(3)
        print("after Login")

        OnTopicCategoriesXpath = '//*[@id="CategoryGroup-on-topic-forums"]/div/table/tbody/tr/td[1]/div/h3/a'
        linkElement = self.__driver.find_element_by_xpath(OnTopicCategoriesXpath)
        linkElement.click()


        #go to specific topic
        time.sleep(2)
        TeslagradTopic = '//*[@id="Discussion_202278"]/td[1]/div/a'
        linkElement = self.__driver.find_element_by_xpath(TeslagradTopic)
        linkElement.click()

    def createXML(self):
        # output all comments to topic

        root = ET.Element("Comments")

        counter = 1
        xmlTag = ""

        time.sleep(2)
        comments = []
        comments = self.__driver.find_elements_by_class_name('Item-BodyWrap')
        for comment in comments:
            text = comment.find_element_by_class_name('Message').text
            xmlTag = "user "+ str(counter)
            doc = ET.SubElement(root, "Comment")
            ET.SubElement(doc, xmlTag).text = text
            counter += 1



        tree = ET.ElementTree(root)
        tree.write("penny.xml")

    def postToTopic(self):

        optionalPosts = ["I Love Teslagrad",
                        "Animation looks great",
                        "Can't wait to play this"]


        postField = self.__driver.find_element_by_id('Form_Body')
        postField.clear()
        postField.send_keys(optionalPosts[randint(0,2)])


        submitPost = self.__driver.find_element_by_id('Form_PostComment')
        submitPost.click()



def main():
    spider = PennySpider()
    spider.loginToPenny()
    spider.afterLogin()
    spider.createXML()
    spider.postToTopic()

if __name__=='__main__':
    main()


