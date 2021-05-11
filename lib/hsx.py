import time
import json
import bs4
from os import path
from lib import common


def crawl_list_hsx_symbol():
    cookies = {
        '_ga': 'GA1.2.1562126088.1619840860',
        'ASP.NET_SessionId': 'yy53wyr5chjrdwsongpgmrig',
        'TS016df111': '01343ddb6aad893202e195904a27548054df314df54d349ababae5f0d641814941f03b8da8d1726ea01b7a76aa7254498a66106e7eb953855f87c0be5322c25173f0376076',
        '_gid': 'GA1.2.1417918349.1620738442',
        '_gat_gtag_UA_116051872_2': '1',
        'TS0d710d04027': '085cef26a9ab200023596194a51704e753c307f0d9632a40d63f20a342560a3eeca68c5b2409357608fbdf45cb113000522824b6a80e85b16033be6b3bbd3e5207a7734abef5b7f1f821eaee0fd12c6821e85e408d9330cd632e20a874dd4365',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.hsx.vn/Modules/Listed/Web/Symbols?fid=18b12d5d2d554559bf10eeb90304ff2e',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = {
        'pageFieldName1': 'Code',
        'pageFieldValue1': '',
        'pageFieldOperator1': 'eq',
        'pageFieldName2': 'Sectors',
        'pageFieldValue2': '',
        'pageFieldOperator2': '',
        'pageFieldName3': 'Sector',
        'pageFieldValue3': '00000000-0000-0000-0000-000000000000',
        'pageFieldOperator3': '',
        'pageFieldName4': 'StartWith',
        'pageFieldValue4': '',
        'pageFieldOperator4': '',
        'pageCriteriaLength': '4',
        '_search': 'false',
        'nd': '1620738472319',
        'rows': '30',
        'page': '1',
        'sidx': 'id',
        'sord': 'desc',
    }

    list_symbols = []
    for page_num in range(1, 15):
        params['page'] = str(page_num)
        response = common.wrap_request_get(
            'https://www.hsx.vn/Modules/Listed/Web/SymbolList', headers=headers, data=params, cookies=cookies)
        response_json = response.json()
        list_symbols.extend(response_json["rows"])
        print("%s-%s" % (response_json["total"], response_json["records"]))
        time.sleep(1)

    return list_symbols


def write_hsx_symbols(output_path="output/hsx_symbol.json"):
    list_symbols = crawl_list_hsx_symbol()
    with open(output_path, "w") as fp:
        fp.write(json.dumps(list_symbols))
    print("%s records" % len(list_symbols))


_list_symbols = None


def load_hsx_symbols(input_path="output/hsx_symbol.json"):
    global _list_symbols
    if _list_symbols is not None:
        return _list_symbols
    with open(input_path, "r") as fp:
        list_raw_symbols = json.load(fp)
    _list_symbols = []
    for symbol in list_raw_symbols:
        _list_symbols.append({
            "id": symbol["cell"][0],
            "code": symbol["cell"][1],
            "name": symbol["cell"][4],
            "total_issues": symbol["cell"][5],
            "active_issues": symbol["cell"][6],
            "first_day": symbol["cell"][7],
        })
    return _list_symbols


def crawl_classified_hsx_symbol(output_path="output/hsx_symbols_enhance.json"):
    list_symbols = load_hsx_symbols()
    result_list = []
    if path.isfile(output_path):
        # load check point
        with open(output_path, "r") as fp:
            result_list = json.load(fp)
        print("check point found, %s records" % len(result_list))
        set_loaded = {symbol["id"] for symbol in result_list}
        list_symbols = [symbol for symbol in list_symbols if symbol["id"] not in set_loaded]

    for symbol_obj in list_symbols:
        print(symbol_obj["code"])
        crawl_symbol_info(symbol_obj)
        result_list.append(symbol_obj)
        if len(result_list) % 5 == 0:
            print("len = %s; create check point" % len(result_list))
            with open(output_path, "w") as fp:
                fp.write(json.dumps(result_list))


def crawl_symbol_info(symbol_obj):
    cookies = {
        '_ga': 'GA1.2.1562126088.1619840860',
        'ASP.NET_SessionId': 'yy53wyr5chjrdwsongpgmrig',
        '_gid': 'GA1.2.1417918349.1620738442',
        'TS016df111': '01343ddb6aca7b9ed8c216b2dbaedfddd4a18b87dfbee7c721c9e49a47e283c2c8534f24bc09343f63e07a2da30bc84751a36e615fddf7796b9eca3ebd25c56eedd606a2de',
        'TS0d710d04027': '085cef26a9ab20006a2163fe38e879e904630c4fb7801b1f88d33bbfab5db9a0f1009b9970a2a9a508478925a3113000cc14d697c7ad057cd032da424c72c646007243bc48d808e0f5a5c67cb6dfbbb2b8d38023733cd4c109e16fca80d1cafa',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.hsx.vn/Modules/Listed/Web/Symbols?fid=18b12d5d2d554559bf10eeb90304ff2e',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # params = (
    #     ('id', '624'),
    #     ('rid', '2075028479'),
    # )

    # response = requests.get('https://www.hsx.vn/Modules/Listed/Web/SymbolView', headers=headers, params=params,
    #                         cookies=cookies)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    response = common.wrap_request_get(
        'https://www.hsx.vn/Modules/Listed/Web/SymbolView?id=%s&rid=2075028479' % symbol_obj["id"])

    soup = bs4.BeautifulSoup(response.content, "html.parser")
    symbol_history = soup.find("div", {"id": "symbolHistoryOverview"})
    symbol_obj["field_of_business"] = symbol_history.find_all("div")[1].getText().strip()
    for tag in symbol_history.find_all("tr"):
        if tag.find("td", {"class": "left"}).getText().strip() == "Nhóm ngành":
            symbol_obj["class"] = tag.find("td", {"class": "data"}).getText().strip()
    # print("[%s]-[%s]-[%s]" % (symbol_obj["code"], symbol_obj["field_of_business"], symbol_obj["class"]))

