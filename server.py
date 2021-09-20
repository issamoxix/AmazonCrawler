from main import Crawler
from fastapi import FastAPI
from requests_html import AsyncHTMLSession
from typing import Optional
import json

app = FastAPI()

#get requests will scrape the data from the amazon daily 
#will return json response
#/?pages = 1 how many page want to scrape 
#keep it empty just (/) for the first page only
@app.get('/')
async def ScrapeData(pages:Optional[int]= 1):
    crawle = Crawler()
    for page in range(1,pages+1):
        url = f"https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_{page}?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:{page},sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:60&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"
        asession = AsyncHTMLSession()
        r = await asession.get(url)
        await r.html.arender(sleep=1)
        widget = r.html.xpath('//*[@id="widgetContent"]')[0]
        items = widget.find('div')
        crawle.GetData(items)
    return crawle.data


@app.get('/test')
def TestFunc():
    return {'Hi there':'keep testing !!'}
