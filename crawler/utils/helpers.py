import datetime
from requests_html import AsyncHTMLSession
import os


async def get_response(url, sleep=1):
    requests = AsyncHTMLSession()
    response = await requests.get(url, timeout=15)
    await response.html.arender(sleep=sleep)
    return response


def get_attr(elem, attr, default_val=None):
    return elem.attrs.get(attr, default_val)


def selector(elem, css_selector, all=0):
    if not elem:
        return None
    if all != 0:
        return elem.find(css_selector) or None
    return elem.find(css_selector)[0] if elem.find(css_selector) else None


def get_text(elem, default_val=""):
    return elem.text if elem else default_val


async def get_item_details(id, url, ITEMS_DICT):
    response = await get_response(url, sleep=0)
    dom = response.html
    item_name = get_text(selector(dom, "h1#title"))
    feature_bullets = get_text(
        selector(dom, "div#feature-bullets ul.a-unordered-list ")
    )
    saving_percentage = get_text(selector(dom, "span.savingsPercentage"))
    deal_price = get_text(
        selector(dom, "div#apex_desktop span.a-price span.a-offscreen")
    )
    original_price = get_text(
        selector(dom, "div#apex_desktop span.basisPrice span.a-offscreen")
    )
    ITEMS_DICT[id] = {
        "item_name": item_name,
        "deal_price": deal_price,
        "saving_percentage": saving_percentage,
        "original_price": original_price,
        "feature_bullets": feature_bullets,
    }


def extracting_meta():
    now = datetime.datetime.now()
    extracting_detail = f"extracting_{now.strftime('%H_%M_%d_%m_%y')}"
    os.mkdir(extracting_detail)
    return extracting_detail


async def download_image(folder, file_name, url, id):
    response = await get_response(url, sleep=0)
    file_name = file_name.replace('"', "")
    file_name = f"{file_name.replace('/','_')}_id=[{id}]"
    with open(f"{folder}/{file_name}.jpg", "wb") as image:
        image.write(response.content)

async def save_data_to_db(items_dict):
    # TODO: Implement saving items_dict to a database
    pass
