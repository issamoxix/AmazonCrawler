from requests_html import HTMLSession
import pandas as pd
import sys

class Crawler:    
    def Start(self,test,debugg=False):
        self.maxPage = 33
        self.Bag = []
        self.title = []
        self.price = []
        self.link = []
        self.testPage = test
        self.Debugg = debugg
        if self.Debugg:
            return self.ParseAll(self.testPage)
        else:
            return self.ParseAll(self.maxPage)
    def CheckVariable(self,item,xpath):
        try:
            return item.xpath(xpath)
        except:
            return ['No Data']
    def CheckElement(self,item,label):
        try:
            return item[0].attrs[label]
        except:
            return 'No Data'
    def CheckText(self,item):
        try:
            return item[0].text
        except:
            return 'No Data'
    def GetData(self,items):
        data = []
        for i in items:
            #select by xpath the items
            price = self.CheckVariable(i,'//div/div[2]/div/div/div[3]/div[1]/span')
            image = self.CheckVariable(i,'//*[@id="dealImage"]/div/div/div[1]/img')
            title = self.CheckVariable(i,'//*[@id="dealTitle"]/span')
            href = self.CheckVariable(i,'//*[@id="dealTitle"]')
            
            # price = i.xpath('//div/div[2]/div/div/div[3]/div[1]/span')
            # image = i.xpath('//*[@id="dealImage"]/div/div/div[1]/img')
            # title = i.xpath('//*[@id="dealTitle"]/span')
            # href = i.xpath('//*[@id="dealTitle"]')

            #check if items empty 
            try:
                if '100_dealView' not in i.attrs['id']:
                    continue
            except:
                if len(price) ==0 or len(image)==0 or len(title)==0 or len(href)==0:
                    continue

            #get the raw data aka innerHTML/TEXT
            r_href = self.CheckElement(href,'href')
            r_image = self.CheckElement(image,'src')
            r_title = self.CheckText(title)
            r_price = self.CheckText(price)
            # r_href = href[0].attrs['href'] if href[0].attrs else 'No Link'
            # r_image = image[0].attrs['src'] if image[0].attrs['src'] else 'No Image'
            # r_title = title[0].text if title[0].text else 'No Title'
            # r_price = price[0].text if price[0].text else 'No Price'

            #append objects to the data array 
            data.append({'title':r_title,'price':r_price, 'image':r_image,'link':r_href})
            self.title.append(r_title)
            self.price.append(r_price)
            self.link.append(r_href)
        return data

    #Parse Page in the same session
    def ParsePage(self, url):
        session = HTMLSession()
        r =  session.get(url)
        r.html.render(sleep=1,scrolldown=3,keep_page=True,wait=1)
        # print('Status Code : ',r.status_code)
        products = r.html.xpath('//*[@id="widgetContent"]')[0]
        items = products.find('div')
        return  self.Bag.append(self.GetData(items))

    #going thru the 32 page 
    def ParseAll(self,n):
        for i in range(1,n):
            if self.Debugg:
                print(f'Page n{i}')
            page = i
            url = f"https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_{page}?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:{page},sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:60&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"
            try:
                self.ParsePage(url)
            except:
                print('[Error] Cant ParsePage')
                pass
        # if self.Debugg:
        #     print('Bag : ',len(self.Bag))
        #     print('Title : ',len(self.title))
        #     print('Price : ',len(self.price))
        pd.DataFrame({'Title':self.title,'Price':self.price,'Link':self.link}).to_csv('data.csv',index_label=False)
        return self.Bag

crw = Crawler()
print('# There is 16 items Per Page')
pages = input('Enter Number of Pages : ')
crw.Start(1+int(pages),True) 
print('Data has been saved in the data.csv file !')