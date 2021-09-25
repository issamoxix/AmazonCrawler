#to save in a .csv file just create data frame and append the lists like the snippet bellow
# pd.DataFrame({'Title':self.title,'Price':self.price,'Link':self.link}).to_csv('data.csv',index_label=False)


class Crawler:    
    def __init__(self):
        self.title = []
        self.price = []
        self.link = []
        self.data = []

    def Start(self,test=2,debugg=False):
        self.maxPage = 33
        self.Bag = []
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
        # data = []
        for i in items:
            try:
                #select by xpath the items
                price = self.CheckVariable(i,'//div/div[2]/div/div/div[3]/div[1]/span')
                image = self.CheckVariable(i,'//*[@id="dealImage"]/div/div/div[1]/img')
                title = self.CheckVariable(i,'//*[@id="dealTitle"]/span')
                href = self.CheckVariable(i,'//*[@id="dealTitle"]')
                
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

                #append objects to the data array 
                if r_title in self.title:
                    continue
                self.data.append({'title':r_title,'price':r_price, 'image':r_image,'link':r_href})
                self.title.append(r_title)
                self.price.append(r_price)
                self.link.append(r_href)
            except:
                print('Error')
                continue
        return self.data

        #uncomment bellow to save in a .csv file 
        return self.Bag

