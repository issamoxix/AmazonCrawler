from requests_html import HTMLSession
# url = "https://www.amazon.com/international-sales-offers/b/?ie=UTF8&node=15529609011&ref_=nav_cs_gb_intl_52df97a2eee74206a8343034e85cd058&nocache=1626714612342"
# url2 = f"https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_{page}?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:{page},sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:32&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"

class Crawler:
    def __init__(self):
        self.maxPage = 33
        self.Bag = []
    def Start(self,test,debugg=False):
        self.testPage = test
        self.Debugg = debugg
        if self.Debugg:
            return self.ParseAll(self.testPage)
        else:
            return self.ParseAll(self.maxPage)
        
    def GetData(self,items):
        data = []
        for i in items:
            #select by xpath the items
            price = i.xpath('//div/div[2]/div/div/div[3]/div[1]/span')
            image = i.xpath('//*[@id="dealImage"]/div/div/div[1]/img')
            title = i.xpath('//*[@id="dealTitle"]/span')
            href = i.xpath('//*[@id="dealTitle"]')

            #check if items empty 
            if len(price) ==0 or len(image)==0 or len(title)==0 or len(href)==0:
                continue

            #get the raw data aka innerHTML/TEXT
            r_href = href[0].attrs['href']
            r_title = title[0].text
            r_price = price[0].text
            r_image = image[0].attrs['src']

            #append objects to the data array 
            data.append({'title':r_title,'price':r_price, 'image':r_image,'link':r_href})
        return data

    #Parse Page in the same session
    def ParsePage(self, url):
        session = HTMLSession()
        r =  session.get(url)
        r.html.render(sleep=1)
        products = r.html.xpath('//*[@id="widgetContent"]')[0]
        items = products.find('div')
        return  self.Bag.append(self.GetData(items))

    #going thru the 32 page 
    def ParseAll(self,n):
        for i in range(1,n):
            if self.Debugg:
                print(f'Page n{i}')
            page = i
            url = f"https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_{page}?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:{page},sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:32&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"
            print(url)
            try:
                self.ParsePage(url)
            except:
                pass
        if self.Debugg:
            print(self.Bag)
        return self.Bag
