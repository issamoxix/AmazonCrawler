class Crawler:
    def __init__(self):
        self.title = []
        self.price = []
        self.link = []
        self.data = []

    def Start(self, test=2, debugg=False):
        self.maxPage = 33
        self.Bag = []
        self.testPage = test
        self.Debugg = debugg
        if self.Debugg:
            return self.ParseAll(self.testPage)
        else:
            return self.ParseAll(self.maxPage)

    def CheckVariable(self, item, xpath):
        try:
            return item.xpath(xpath)
        except:
            return ["No Data"]

    def CheckElement(self, item, label):
        try:
            return item[0].attrs[label]
        except:
            return "No Data"

    def CheckText(self, item):
        try:
            return item[0].text
        except:
            return "No Data"

    def GetData(self, items):
        # data = []
        for i in items:
            try:
                # select by xpath the items
                price = self.CheckVariable(i, "//div/div[2]/div/div/div[3]/div[1]/span")
                image = self.CheckVariable(i, '//*[@id="dealImage"]/div/div/div[1]/img')
                title = self.CheckVariable(i, '//*[@id="dealTitle"]/span')
                href = self.CheckVariable(i, '//*[@id="dealTitle"]')

                # check if items empty
                try:
                    if "100_dealView" not in i.attrs["id"]:
                        continue
                except:
                    if (
                        len(price) == 0
                        or len(image) == 0
                        or len(title) == 0
                        or len(href) == 0
                    ):
                        continue

                # get the raw data aka innerHTML/TEXT
                r_href = self.CheckElement(href, "href")
                r_image = self.CheckElement(image, "src")
                r_title = self.CheckText(title)
                r_price = self.CheckText(price)

                # append objects to the data array
                if r_title in self.title:
                    continue
                self.data.append(
                    {
                        "title": r_title,
                        "price": r_price,
                        "image": r_image,
                        "link": r_href,
                    }
                )
                self.title.append(r_title)
                self.price.append(r_price)
                self.link.append(r_href)
            except:
                print("Error")
                continue
        return self.data

        # uncomment bellow to save in a .csv file
        return self.Bag


from requests_html import AsyncHTMLSession
import asyncio


async def get_response(url):
    requests = AsyncHTMLSession()
    response = await requests.get(url, timeout=15)
    await response.html.arender(sleep=1)
    return response


def get_attr(elem, attr, default_val=None):
    return elem.attrs.get(attr, default_val)

# TODO docker[db,server]
# TODO def save_image(image_url, file_name):
# TODO def save_data_to_db




def main():
    url = "https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_1?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:1,sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:60&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"
    response = asyncio.run(get_response(url))

    items = response.html.find('div[data-testid="grid-deals-container"] > div')
    for item in items:
        image_elem = item.find("img")[0]
        image_url = get_attr(image_elem, "src")
        title = get_attr(image_elem, "alt")
        item_url = get_attr(item.find("a")[1], "href")



if __name__ == "__main__":
    main()
