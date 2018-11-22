from selenium import webdriver
from urllib.request import urlretrieve
import time
import urllib
import demjson
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import spider.ticket.data
class confirm:
    def wrong_return (self,browser):
        try:
            error="none"
            try:
                wait=WebDriverWait(browser,0.5)
                input=wait.until(expected_conditions.presence_of_all_elements_located((By.ID,'popup_container')))
                error=(browser.find_element_by_xpath('//*[@id="popup_message"]').text)
                browser.find_element_by_xpath('//*[@id="popup_ok"]').click()
            except:
                pass
            return error
        except:
            return "error"
    def send_yz(self,browser,number):
        try:
            pagesource = "None"
            error="None"
            yz=browser.find_element_by_xpath('//*[@id="yzm"]')
            yz.clear()
            yz.send_keys(number)
            wait=WebDriverWait(browser,0.5)
            A=False
            try:
                input=wait.until(expected_conditions.presence_of_all_elements_located((By.ID,'checkfp')))
                browser.find_element_by_xpath('//*[@id="checkfp"]').click()
            except:
                pass
            try:
                time.sleep(2)
                browser.switch_to_frame("dialog-body")
                A=True
            except:
                pass
            if A:
                if(wait.until(expected_conditions.presence_of_all_elements_located((By.ID,'cyjg')))):
                    tips=browser.find_element_by_id('cyjg').text
                    dict_tips={}
                    dict_tips["error"]=tips
                    exits_jsons = demjson.encode(dict_tips)
                    return exits_jsons
                else:
                    browser.maximize_window()
                    browser.get_screenshot_as_file('E:/baidu1.png')
                    pagesource=browser.page_source
                    data_temp=data.data(str(pagesource))
                    dict_later=data_temp.info
                    dict_later['error']=error
                    later_jsons = demjson.encode(dict_later)
                    return later_jsons
            else:
                error=self.wrong_return(browser)
                dict_error={}
                dict_error['error']=error
                error_jsons = demjson.encode(dict_tips)
                return error_jsons
        except:
            return {"error":"查验出错"}
