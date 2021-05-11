import bs4
import json
from lib import common


def get_stock_list(page_num):
    cookies = {
        'language': 'vi-VN',
        '616a3745ee32423b8ef6bed543a12282': 'wugylksd4mjx2xpc0aiec3ew',
        '__RequestVerificationToken': 'PDzDkmqReuWwv3RDNa-_aYuKlYT8eMX6JHeA7Y6vQ5NFEE6TLlaz6xTXo9QzbMlEATaGGCrDab_dzgokP6DbJRbQp_UKSf7JY3XiMpgYTf41',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        '__RequestVerificationToken': 'jVTeKrvTqH6zfM-1SCv62-xEpgAHHGFPm9rrmvKT4MkESg6gi1OU9L6HoIMKYvS2P00_1rsK8QUT_HYTdY1wki718y1jQImVEViUuu51dZQ1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://hnx.vn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://hnx.vn/vi-vn/cophieu-etfs/chung-khoan-ny.html',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    }

    data = {
        'p_issearch': '1',
        'p_keysearch': '0|0',
        'p_market_code': '',
        'p_orderby': 'STOCK_CODE',
        'p_ordertype': 'ASC',
        'p_currentpage': str(page_num),
        'p_record_on_page': '50'
    }

    response = common.wrap_request_get(
        'https://hnx.vn/ModuleIssuer/List/ListSearch_Datas', headers=headers, cookies=cookies, data=data)

    return response


def parse_hnx_list_symbol_response(file_path):
    with open(file_path, "r") as fp:
        r = json.load(fp)
    soup = bs4.BeautifulSoup(r["Content"], "html.parser")
    list_stocks = []
    for tag in soup.find_all("tr"):
        if not tag.find("td", {"class": "tdCenterAlign STOCK_CODE"}):
            continue
        stock_info = {
            "code": tag.find("td", {"class": "tdCenterAlign STOCK_CODE"}).getText().strip(),
            "name": tag.find("td", {"class": "tdLeftAlign NAME"}).getText().strip(),
            "total_issues": tag.find("td", {"class": "tdRightAlign TOTAL_LISTING_QTTY"}).getText().strip(),
            "active_issues": tag.find("td", {"class": "tdRightAlign TOTAL_LISTING_VALUE"}).getText().strip(),
            "first_day": tag.find("td", {"class": "tdCenterAlign START_TRADING_DATE"}).getText().strip(),
        }
        if tag.find("td", {"class": "tdLeftAlign CATEGORIES_NAME"}):
            stock_info["class"] = tag.find("td", {"class": "tdLeftAlign CATEGORIES_NAME"}).getText().strip()
        list_stocks.append(stock_info)

    return list_stocks


def crawl_list_stock(num_page, output_path="output/hnx_symbols.json", input_format="output/hnx/list_stock_%s.json"):
    result_list = []
    for page_num in range(1, num_page + 1):
        result_list.extend(parse_hnx_list_symbol_response(input_format % page_num))
    with open(output_path, "w") as fp:
        json.dump(result_list, fp)
    list_codes = list({stock["code"] for stock in result_list})
    return len(list_codes)
