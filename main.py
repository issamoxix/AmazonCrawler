import asyncio
import threading
from helpers import *


# TODO refactor the code

async def main():
    ITEMS_DICT = {}
    extracting_name = extracting_meta()

    url = "https://www.amazon.com/international-sales-offers/b/ref=gbps_ftr_m-9_475e_page_1?node=15529609011&nocache=1626714612342/&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:1,sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:60&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6D45Q7N5YJREGC19R32Z&ie=UTF8#next"
    response = await get_response(url)
    items = response.html.find('div[data-testid="grid-deals-container"] > div')
    not_product = ["/deal/", "/b?"]

    for key, item in enumerate(items):
        image_elem = item.find("img")[0]
        image_url = get_attr(image_elem, "src")
        title = get_attr(image_elem, "alt")
        print("[EXTRACTING] ", title)
        threading.Thread(await download_image(extracting_name, title, image_url, key))
        item_url = get_attr(item.find("a")[1], "href")
        product_checker = [int(pattern in item_url) for pattern in not_product]
        product_checker = list(set(product_checker))
        ITEMS_DICT[key] = {"title": title, "image_url": image_url, "url": item_url}
        if product_checker[0] == 0 and len(product_checker) == 1:
            threading.Thread(await get_item_details(key, item_url, ITEMS_DICT)).start()


if __name__ == "__main__":
    asyncio.run(main())
