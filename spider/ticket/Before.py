from selenium import webdriver
from urllib.request import urlretrieve
import time
import urllib
import demjson
class invoice:
    def __init__(self):
        try:
            self.browser = webdriver.Chrome()
            website_link="https://inv-veri.chinatax.gov.cn/"
            self.browser.get(website_link)
        except:
            return "browser_error"
    def fill(self,xpaths,nums):
        number=self.browser.find_element_by_id(xpaths)
        number.send_keys(nums)  
    def fill_dm(self,nums):
        try:
            self.fill("fpdm",nums)
        #发票代码
        except:
            return "dm_error"
        
    def fill_hm(self,nums):
        try:
            self.fill("fphm",nums)
        #发票号码
        except:
            return "hm_error"
        
    def fill_kp(self,nums):
        try:
            self.fill("kprq",nums)
        #开票日期
        except:
            return "rq_error"
        
    def fill_jy(self,nums):
        try:
            self.fill("kjje",nums)
        #校验码后六位
        except:
            return "jy_error"
        
    def pic(self):
        try:
            if self.browser.find_element_by_xpath('//*[@id="yzm_img"]').is_displayed():
                self.browser.find_element_by_xpath('//*[@id="yzm_img"]').click()
            time.sleep(2)
            adress=self.browser.find_element_by_xpath('//img[2]')
            link=adress.get_attribute('src')
            urllib.request.urlretrieve(link,'E:\%s.jpg'%'yz')
            print(link)
            return link
        except:
            return "get_yzm_error"
    
    def color_yz(self):
        try:
            try:
                color=self.browser.find_element_by_xpath('//*[@id="yzminfo"]/font')
                color=color.text
                tips=('请输入%s验证码：'%color)
            except:
                tips=('请输入所示验证码：')
            finally:
                print(tips)
                return tips
        except:
            return "get_yzm_color_error"
        
    def main(self,data):
        try:
            jsons=demjson.decode(data)
            fpdm=(jsons['fp_dm'])
            fphm=(jsons['fp_hm'])
            kprq=(jsons['kp_rq'])
            kjje=(jsons['jy'])
            self.fill_dm(fpdm)
            self.fill_hm(fphm)
            self.fill_kp(kprq)
            self.fill_jy(kjje)
            links=self.pic()#导出验证码链接，如果有需要存到本地也可以，代码已经在pic函数中注释
            color=self.color_yz()#显示验证码颜色
            dict_perior={}
            dict_perior['verity_code_link']=links
            dict_perior['verity_code_word']=color
            jsons = demjson.encode(dict_perior)
            return jsons
        except:
            return {"error":"other errors"}


 
