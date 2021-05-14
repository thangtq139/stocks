from lib import common
from lib import vietstock


def get_finance_info(stock_symbol):
    headers = {
        'authority': 'e.cafef.vn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'origin': 'https://s.cafef.vn',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://s.cafef.vn/',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    }

    # params = (
    #     ('symbol', 'VCB'),
    # )

    # response = requests.get('https://e.cafef.vn/fi.ashx', headers=headers, params=params)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    response = common.wrap_request_get('https://e.cafef.vn/fi.ashx?symbol=%s' % stock_symbol, headers=headers)
    return response


def crawl_finance_info():
    stock_symbols = vietstock.filter_mandatory_stocks()
    for stock_symbol in stock_symbols:
        r = get_finance_info(stock_symbol.upper())
        with open("output/cafef/%s-FINANCE.json" % stock_symbol, "wb") as fp:
            fp.write(r.content)
        print("%s - len [%s]" % (stock_symbol, len(r.content)))
