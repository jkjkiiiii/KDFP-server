from lxml import etree
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from API.compress import size


class Data():
    # 传入网页文档，提取信息
    def __init__(self, html):
        info = {}
        t = etree.HTML(html)
        info['cycs'] = t.xpath('//span[@id="cycs"]/text()')[0]
        info['time'] = t.xpath('//span[contains(@id,"cysj")]/text()')[0]
        name_to_id = {'fplx': 'fpcc_',
                      'fpdm': 'fpdm_',
                      'fphm': 'fphm_',
                      'kprq': 'kprq_',
                      'code': 'jym_',
                      'num': 'sbbh_',
                      'gfMc': 'gfmc_',  # 官方名称
                      'mmq': 'password_',
                      'gfNsrsbh': 'gfsbh_',
                      'gfContact': 'gfdzdh_',
                      'gfBank': 'gfyhzh_',
                      'goodsamount': 'je_',
                      'taxamount': 'se_',
                      'SUMAMOUNT': 'jshjdx_',
                      'sumamount': 'jshjxx_',
                      'xfMc': 'xfmc_',
                      'xfNsrsbh': "xfsbh_",
                      'xfContact': "xfdzdh_",
                      'xfBank': "xfyhzh_"}
        for name in name_to_id:
            if name not in ['fplx', 'mmq']:
                dzfp = t.xpath(
                    '//h1[contains(@id,"{}")]/text()'.format(name_to_id[name] + 'dzfp'))
                if dzfp:
                    info[name] = dzfp[0]
                else:
                    info[name] = t.xpath(
                        '//h1[contains(@id,"{}")]/text()'.format(name_to_id[name] + 'pp'))[0]
            elif name == 'fplx':
                dzfp = t.xpath('//h1[contains(@id,"fpcc_dzfp")]/text()')
                if dzfp:
                    info['fplx'] = dzfp[0]
                else:
                    info['fplx'] = t.xpath(
                        '//h1[contains(@id,"fpcc_pp")]/text()')[0]
            elif name == 'mmq':
                dzfp = t.xpath('//td[contains(@id,"password_dzfp")]/text()')
                if dzfp:
                    info['mmq'] = dzfp[0]
                else:
                    info['mmq'] = t.xpath(
                        '//td[contains(@id,"password_pp")]/text()')[0]
#         info['fpdm']=t.xpath('//span[contains(@id,"fpdm_dzfp")]/text()')[0]
#         info['fphm']=t.xpath('//span[contains(@id,"fphm_dzfp")]/text()')[0]
#         info['kprq']=t.xpath('//span[contains(@id,"kprq_dzfp")]/text()')[0]
#         info['code']=t.xpath('//span[contains(@id,"jym_dzfp")]/text()')[0]
#         info['num']=t.xpath('//span[contains(@id,"sbbh_dzfp")]/text()')[0]
#         info['gfMc']=t.xpath('//span[contains(@id,"gfmc_dzfp")]/text()')[0]
#         info['mmq']=t.xpath('//td[contains(@id,"password_dzfp")]/text()')[0]
#         info['gfNsrsbh']=t.xpath('//span[contains(@id,"gfsbh_dzfp")]/text()')[0]
#         info['gfContact']=t.xpath('//span[contains(@id,"gfdzdh_dzfp")]/text()')[0]
#         info['gfBank']=t.xpath('//span[contains(@id,"gfyhzh_dzfp")]/text()')[0]
        # 以下项目有多个匹配结果
        service_name = []
        model = []
        unit = []
        nums = []
        price = []
        money = []
        rate = []
        tax = []

        for i in range(2, len(t.xpath('//*[@class="fppy_table_box"]/tbody/tr')) - 1):
            try:
                service_name.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[1]//text()')[0])
            except:
                service_name.append(' ')
            try:
                model.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[2]//text()')[0])
            except:
                model.append(' ')
            try:
                unit.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[3]//text()')[0])
            except:
                unit.append(' ')
            try:
                nums.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[4]//text()')[0])
            except:
                nums.append(' ')
            try:
                price.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[5]//text()')[0])
            except:
                price.append(' ')
            try:
                money.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[6]//text()')[0])
            except:
                money.append(' ')
            try:
                rate.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[7]//text()')[0])
            except:
                rate.append(' ')
            try:
                tax.append(t.xpath(
                    '//*[@class="fppy_table_box"]/tbody/tr[' + str(i) + ']/td[8]//text()')[0])
            except:
                tax.append(' ')

        info['mc'] = service_name
        info['gg'] = model
        info['dw'] = unit
        info['sl'] = nums
        info['dj'] = price
        info['je'] = money
        info['shuilv'] = rate
        info['shuie'] = tax
#         info['goodsamount']=t.xpath('//span[contains(@id,"je_dzfp")]/text()')[0]
#         info['taxamount']=t.xpath('//span[contains(@id,"se_dzfp")]/text()')[0]
#         info['SUMAMOUNT']=t.xpath('//span[contains(@id,"jshjdx_dzfp")]/text()')[0]
#         info['sumamount']=t.xpath('//span[contains(@id,"jshjxx_dzfp")]/text()')[0]
#         info['xfMc']=t.xpath('//span[contains(@id,"xfmc_dzfp")]/text()')[0]
        # 大概率为空
        info['remark'] = t.xpath('//span[contains(@id,"bz_dzfp")]/p/text()')
        try:
            info['remark'] = info['remark'][0]
        except:
            info['remark'] = ' '
#         info['xfNsrsbh']=t.xpath('//span[contains(@id,"xfsbh_dzfp")]/text()')[0]
#         info['xfContact']=t.xpath('//span[contains(@id,"xfdzdh_dzfp")]/text()')[0]
#         info['xfBank']=t.xpath('//span[contains(@id,"xfyhzh_dzfp")]/text()')[0]
        self.info = info

    # 将html文件写出
    def write(self):
        with open(r'C:\Users\Administrator\Desktop\invoice\API\Mould' + '\\' + self.info['fpdm'] + self.info['fphm'] + '.html', 'w', encoding='utf-8') as f:
            f.write(str(self.soup))

    # 查找节点
    def findnode(self, nodename):
        if nodename == 'cycs':
            return self.soup.find(id="cycs")
        elif nodename == 'time':
            return self.soup.find(id="cysj")
        elif nodename == 'fplx':
            if self.soup.find(id="fpcc_dzfp")
                return self.soup.find(id="fpcc_dzfp")
            return self.soup.find(id="fpcc_pp")
        elif nodename == 'fpdm':
            if self.soup.find(id="fpdm_dzfp")
                return self.soup.find(id="fpdm_dzfp")
            return self.soup.find(id="fpdm_pp")
        elif nodename == 'fphm':
            if self.soup.find(id="fphm_dzfp")
                return self.soup.find(id="fphm_dzfp")
            return self.soup.find(id="fphm_pp")
        elif nodename == 'kprq':
            if self.soup.find(id="kprq_dzfp")
                return self.soup.find(id="kprq_dzfp")
            return self.soup.find(id="kprq_pp")
        elif nodename == 'code':
            if self.soup.find(id="jym_dzfp")
                return self.soup.find(id="jym_dzfp")
            return self.soup.find(id="jym_pp")
        elif nodename == 'num':
            if self.soup.find(id="sbbh_dzfp")
                return self.soup.find(id="sbbh_dzfp")
            return self.soup.find(id="sbbh_pp")
        elif nodename == 'gfMc':
            if self.soup.find(id="gfmc_dzfp")
                return self.soup.find(id="gfmc_dzfp")
            return self.soup.find(id="gfmc_pp")
        elif nodename == 'mmq':
            if self.soup.find(id="password_dzfp")
                return self.soup.find(id="password_dzfp")
            return self.soup.find(id="password_pp")
        elif nodename == 'gfNsrsbh':
            if self.soup.find(id="gfsbh_dzfp")
                return self.soup.find(id="gfsbh_dzfp")
            return self.soup.find(id="gfsbh_pp")
        elif nodename == 'gfContact':
            if self.soup.find(id="gfdzdh_dzfp")
                return self.soup.find(id="gfdzdh_dzfp")
            return self.soup.find(id="gfdzdh_pp")
        elif nodename == 'gfBank':
            if self.soup.find(id="gfyhzh_dzfp")
                return self.soup.find(id="gfyhzh_dzfp")
            return self.soup.find(id="gfyhzh_pp")
        elif nodename == 'goodsamount':
            if self.soup.find(id="je_dzfp")
                return self.soup.find(id="je_dzfp")
            return self.soup.find(id="je_pp")
        elif nodename == 'taxamount':
            if self.soup.find(id="se_dzfp")
                return self.soup.find(id="se_dzfp")
            return self.soup.find(id="se_pp")
        elif nodename == 'SUMAMOUNT':
            if self.soup.find(id="jshjdx_dzfp")
                return self.soup.find(id="jshjdx_dzfp")
            return self.soup.find(id="jshjdx_pp")
        elif nodename == 'sumamount':
            if self.soup.find(id="jshjxx_dzfp")
                return self.soup.find(id="jshjxx_dzfp")
            return self.soup.find(id="jshjxx_pp")
        elif nodename == 'xfMc':
            if self.soup.find(id="xfmc_dzfp")
                return self.soup.find(id="xfmc_dzfp")
            return self.soup.find(id="xfmc_pp")
        elif nodename == 'remark':
            if self.soup.find(id="bz_dzfp").p
                return self.soup.find(id="bz_dzfp").p
            return self.soup.find(id="bz_pp").p
        elif nodename == 'xfNsrsbh':
            if self.soup.find(id="xfsbh_dzfp")
                return self.soup.find(id="xfsbh_dzfp")
            return self.soup.find(id="xfsbh_pp")
        elif nodename == 'xfContact':
            if self.soup.find(id="xfdzdh_dzfp")
                return self.soup.find(id="xfdzdh_dzfp")
            return self.soup.find(id="xfdzdh_pp")
        elif nodename == 'xfBank':
            if self.soup.find(id="xfyhzh_dzfp")
                return self.soup.find(id="xfyhzh_dzfp")
            return self.soup.find(id="xfyhzh_pp")

    # 将信息写入html
    def writeinfo(self):
        # 打开模板文件
        with open(r'C:\Users\Administrator\Desktop\invoice\API\Mould\Mould.html', encoding='utf-8') as f:
            html = f.read()
        self.soup = BeautifulSoup(html, 'lxml')
        info = self.info
        wrongkeys = ['mc', 'gg', 'dw', 'sl', 'dj', 'je', 'shuilv', 'shuie']
        for k, i in info.items():
            if k in wrongkeys:
                continue
            self.findnode(k).string = i
        self.soup.find(id='mf').string = ''
        for i in range(0, len(info['mc'])):
            new_tr = self.soup.new_tag('tr')  # 新建一个tr标签

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_left borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['mc'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_left borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['gg'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_left borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['dw'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_right borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['sl'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_right borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['dj'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_right borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['je'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_right borderRight"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['shuilv'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            new_td = self.soup.new_tag('td')
            new_td.attrs = {'class': "align_right"}
            new_span = self.soup.new_tag('span')
            new_span.attrs = {'class': "content_td_blue"}
            new_span.string = info['shuie'][i]
            new_td.append(new_span)
            new_tr.append(new_td)

            self.soup.find(id='mf').append(new_tr)
        self.write()

    # 使用渲染其获取图片
    def getpic(self):
        """生成html文件并截图"""
        self.writeinfo()
        os.system('wkhtmltoimage.exe ' + r'C:\Users\Administrator\Desktop\invoice\API\Mould' + '\\' +
                  self.info['fpdm'] + self.info['fphm'] + '.html' + ' C:\\Users\\Administrator\\Desktop\\invoice\\spider\\images\\' + self.info['fpdm'] + self.info['fphm'] + '.png')
        size('C:\\Users\\Administrator\\Desktop\\invoice\\spider\\images\\' +
             self.info['fpdm'] + self.info['fphm'] + '.png', 1100)
        os.remove(r'C:\Users\Administrator\Desktop\invoice\API\Mould' +
                  '\\' + self.info['fpdm'] + self.info['fphm'] + '.html')

    def getdata(self):
        info = self.info
        invoice = zip(info['mc'], info['gg'], info['dw'], info['sl'],
                      info['dj'], info['je'], info['shuilv'], info['shuie'])
        info.pop('mc')
        info.pop('gg')
        info.pop('dw')
        info.pop('sl')
        info.pop('dj')
        info.pop('je')
        info.pop('shuilv')
        info.pop('shuie')
        info['goodsData'] = []
        for i in invoice:
            temp = {}
            temp['name'] = i[0]
            temp['apec'] = i[1]
            temp['unit'] = i[2]
            temp['amount'] = i[3]
            temp['priceUnit'] = i[4]
            temp['priceSum'] = i[5]
            temp['taxRate'] = i[6]
            temp['taxSum'] = i[7]
            info['goodsData'].append(temp)
        return info
