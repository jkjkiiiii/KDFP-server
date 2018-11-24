from selenium import webdriver
from urllib.request import urlretrieve
import time
import urllib
import demjson
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from spider.ticket.data import data
class confirm:
    def wrong_return (self,browser):
        error="none"
        wait=WebDriverWait(browser,2)
        wait.until(expected_conditions.presence_of_all_elements_located((By.ID,'popup_container')))
        error=(browser.find_element_by_xpath('//*[@id="popup_message"]').text)
        browser.find_element_by_xpath('//*[@id="popup_ok"]').click()
        return error
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
                wait.until(expected_conditions.presence_of_all_elements_located((By.ID,'checkfp')))
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
                try:
                    wait=WebDriverWait(browser,2)
                    wait.until(expected_conditions.presence_of_all_elements_located((By.ID,'cyjg')))
                    tips=browser.find_element_by_id('cyjg').text
                    dict_tips={}
                    dict_tips["error"]=tips
                    exits_jsons = demjson.encode(dict_tips)
                    return exits_jsons
                except:
                    pagesource=browser.page_source
                    data_temp=data(str(pagesource))
                    dict_later=data_temp.info
                    pic_name='%s%s'%(dict_later['开票日期'],dict_later['校验码'])
                    path="C:\\Users\\BBfat\\Desktop\\invoice\\spider\\images\\%s.png"%pic_name
                    browser.get_screenshot_as_file(path)
                    dict_later['error']=error
                    dict_later['pic_name']=pic_name
                    #later_jsons = demjson.encode(dict_later)
                    browser.close()
                    return dict_later
            else:
                error=self.wrong_return(browser)
                dict_error={}
                dict_error['error']=error
                #error_jsons = demjson.encode(dict_error)
                return dict_error
        except:
            return {"error":"查验出错"}
