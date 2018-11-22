from lxml import etree
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import os

class data():
    #传入网页文档，提取信息
    def __init__(self,html):
        info={}
        t=etree.HTML(html)
        info['查验次数']=t.xpath('//span[@id="cycs"]/text()')
        info['查验时间']=t.xpath('//span[contains(@id,"cysj")]/text()')
        info['发票头']=t.xpath('//h1[contains(@id,"fpcc_dzfp")]/text()')
        info['发票代码']=t.xpath('//span[contains(@id,"fpdm_dzfp")]/text()')
        info['发票号码']=t.xpath('//span[contains(@id,"fphm_dzfp")]/text()')
        info['开票日期']=t.xpath('//span[contains(@id,"kprq_dzfp")]/text()')
        info['校验码']=t.xpath('//span[contains(@id,"jym_dzfp")]/text()')
        info['机器编号']=t.xpath('//span[contains(@id,"sbbh_dzfp")]/text()')
        info['购买方名称']=t.xpath('//span[contains(@id,"gfmc_dzfp")]/text()')
        info['密码区']=t.xpath('//td[contains(@id,"password_dzfp")]/text()')
        info['购买方纳税人识别号']=t.xpath('//span[contains(@id,"gfsbh_dzfp")]/text()')
        info['购买方地址、电话']=t.xpath('//span[contains(@id,"gfdzdh_dzfp")]/text()')
        info['购买方开户行及账号']=t.xpath('//span[contains(@id,"gfyhzh_dzfp")]/text()')
        #以下项目有多个匹配结果
        service_name=[]
        model=[]
        unit=[]
        items=t.xpath('//td[@class="align_left borderRight"]/span/text()')
        i=1
        for item in items:
            if i%3==1:
                service_name.append(item)
            elif i%3==2:
                model.append(item)
            elif i%3==0:
                unit.append(item)
            i=i+1
        info['货物或应税劳务、服务名称']=service_name
        info['规格型号']=model
        info['单位']=unit
        items=t.xpath('//td[@class="align_right borderRight"]/span[@class="content_td_blue"]/text()')
        #以下项目有多个匹配结果
        nums=[]
        price=[]
        money=[]
        rate=[]
        i=1
        for item in items:
            if i%4==1:
                nums.append(item)
            elif i%4==2:
                price.append(item)
            elif i%4==3:
                money.append(item)
            elif i%4==0:
                rate.append(item)
            i=i+1
        nums.pop()
        info['数量']=nums
        info['单价']=price
        info['金额']=money
        info['税率']=rate
        items=t.xpath('//td[@class="align_right"]/span[@class="content_td_blue"]/text()')
        tax=[]
        for item in items:
            tax.append(item)
        tax.pop()
        info['税额']=tax
        info['合计金额']=t.xpath('//span[contains(@id,"je_dzfp")]/text()')
        info['合计税额']=t.xpath('//span[contains(@id,"se_dzfp")]/text()')
        info['价税合计（大写）']=t.xpath('//span[contains(@id,"jshjdx_dzfp")]/text()')
        info['价税合计（小写）']=t.xpath('//span[contains(@id,"jshjxx_dzfp")]/text()')
        info['销售方名称']=t.xpath('//span[contains(@id,"xfmc_dzfp")]/text()')
        info['备注']=t.xpath('//span[contains(@id,"bz_dzfp")]/p/text()')
        info['销售方纳税人识别号']=t.xpath('//span[contains(@id,"xfsbh_dzfp")]/text()')
        info['销售方地址、电话']=t.xpath('//span[contains(@id,"xfdzdh_dzfp")]/text()')
        info['销售方开户行及账号']=t.xpath('//span[contains(@id,"xfyhzh_dzfp")]/text()')
        self.fphm=info['发票号码'][0]
        self.info=info
    #保存json文件
    def savejson(self):
        with open('json\\'+self.fphm+'.json',"w",encoding='utf-8') as f:
            json.dump(self.info,f)

    #将html文件写出
    def write(self):
        with open('Mould\\temp.html','w',encoding='utf-8') as f:
            f.write(str(self.soup))

    #查找节点
    def findnode(self,nodename):
        if nodename=='查验次数':
            return self.soup.find(id="cycs")
        elif nodename=='查验时间':
            return self.soup.find(id="cysj")
        elif nodename=='发票头':
            return self.soup.find(id="fpcc_dzfp")
        elif nodename=='发票代码':
            return self.soup.find(id="fpdm_dzfp")
        elif nodename=='发票号码':
            return self.soup.find(id="fphm_dzfp")
        elif nodename=='开票日期':
            return self.soup.find(id="kprq_dzfp")
        elif nodename=='校验码':
            return self.soup.find(id="jym_dzfp")
        elif nodename=='机器编号':
            return self.soup.find(id="sbbh_dzfp")
        elif nodename=='购买方名称':
            return self.soup.find(id="gfmc_dzfp")
        elif nodename=='密码区':
            return self.soup.find(id="password_dzfp")
        elif nodename=='购买方纳税人识别号':
            return self.soup.find(id="gfsbh_dzfp")
        elif nodename=='购买方地址、电话':
            return self.soup.find(id="gfdzdh_dzfp")
        elif nodename=='购买方开户行及账号':
            return self.soup.find(id="gfyhzh_dzfp")
        elif nodename=='合计金额':
            return self.soup.find(id="je_dzfp")
        elif nodename=='合计税额':
            return self.soup.find(id="se_dzfp")
        elif nodename=='价税合计（大写）':
            return self.soup.find(id="jshjdx_dzfp")
        elif nodename=='价税合计（小写）':
            return self.soup.find(id="jshjxx_dzfp")
        elif nodename=='销售方名称':
            return self.soup.find(id="xfmc_dzfp")
        elif nodename=='备注':
            return self.soup.find(id="bz_dzfp").p
        elif nodename=='销售方纳税人识别号':
            return self.soup.find(id="xfsbh_dzfp").p
        elif nodename=='销售方地址、电话':
            return self.soup.find(id="xfdzdh_dzfp")
        elif nodename=='销售方开户行及账号':
            return self.soup.find(id="xfyhzh_dzfp")

    #将信息写入html
    def writeinfo(self,filename):
        #打开模板文件
        with open('Mould\\Mould.html',encoding='utf-8') as f:
            html=f.read()
        self.soup=BeautifulSoup(html,'lxml')
        #读取数据库传来的json
        with open(filename) as f:
            info=json.load(f)
        n=1
        for k,i in info.items():
            if n>=14 and n<=21:
                continue
            self.findnode(k).string=i[0]
            n=n+1
        self.soup.find(id='mf').string=''
        for i in range(0,len(info['货物或应税劳务、服务名称'])):
            new_tr=self.soup.new_tag('tr')#新建一个tr标签

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_left borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['货物或应税劳务、服务名称'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_left borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['规格型号'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_left borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['单位'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_right borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['数量'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_right borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['单价'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_right borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['金额'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_right borderRight"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['税率'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td=self.soup.new_tag('td')
            new_td.attrs={'class':"align_right"}
            new_span=self.soup.new_tag('span')
            new_span.attrs={'class':"content_td_blue"}
            new_span.string=info['税额'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            self.soup.find(id='mf').append(new_tr)
        self.write()

    #通过浏览器渲染后返回截图
    def getpic(self):
        b=webdriver.Chrome()
        b.set_window_size(1920,1080)
        current_path = os.path.abspath(__file__)
        b.get(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")+'\\Mould\\temp.html')
        b.save_screenshot('pics\\temp.png')
        b.close()
        os.remove('Mould\\temp.html')
