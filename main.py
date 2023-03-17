from requests_html import AsyncHTMLSession
import asyncio


async def get_response(url):
    requests = AsyncHTMLSession()
    response = await requests.get(url, timeout=15)
    await response.html.arender(sleep=1)
    return response


def get_attr(elem, attr, default_val=None):
    return elem.attrs.get(attr, default_val)


def get_item_details(id, url):
    response =asyncio.run(get_response(url))
    return response


# TODO docker[db,server]
# TODO def save_image(image_url, file_name):
# TODO def save_data_to_db
# TODO saving items in dict and mapping thru an multithread func to get price and more details from url
# TODO Thread get_item_details

def main():
    url = "https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_1?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:1,sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:60&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"
    response = asyncio.run(get_response(url))

    items = response.html.find('div[data-testid="grid-deals-container"] > div')
    items_dict = {}
    for key, item in enumerate(items):
        image_elem = item.find("img")[0]
        image_url = get_attr(image_elem, "src")
        title = get_attr(image_elem, "alt")
        item_url = get_attr(item.find("a")[1], "href")
        if "/deal/" not in item_url:
            get_item_details(key, item_url)


if __name__ == "__main__":
    main()
