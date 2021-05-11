import requests
import random
import json
import time
from os import path
from lib import common


REPORT_TYPE = ["BCTT", "CDKT", "KQKD", "LC", "CSTC"]
MAP_REPORT_TERM_TYPE_TO_TEXT = {
    "1": "YEARLY",
    "2": "QUARTERLY",
}
REPORT_TERM_TYPE = list(MAP_REPORT_TERM_TYPE_TO_TEXT.keys())


def crawl_finance_info():
    stock_symbols = filter_mandatory_stocks()
    for report_term_type in REPORT_TERM_TYPE:
        for stock_symbol in stock_symbols:
            crawl_stock_finance_info(stock_symbol.upper(), report_term_type)


def crawl_stock_finance_info(stock_symbol, report_term_type):
    for report_type in REPORT_TYPE:
        page_num = 0
        while True:
            page_num += 1
            file_sign = "%s-%s-%s-%s" % (
                stock_symbol,
                report_type,
                MAP_REPORT_TERM_TYPE_TO_TEXT[report_term_type],
                page_num
            )
            print("Crawling [%s]" % file_sign)
            output_file = "output/vietstock/%s.json" % file_sign
            if path.isfile(output_file):
                with open(output_file, "r") as fp:
                    data = json.load(fp)
                print("File [%s] exists! Skipping..." % output_file)
                if not data[0]:
                    print("Null response, breaking")
                    break
                continue
            response = get_finance_info(stock_symbol, report_type, report_term_type, page_num)
            if not response:
                print("Empty response, breaking")
                break
            with open(output_file, "w") as fp:
                fp.write(response.content.decode("utf-8"))
            if not response.json()[0]:
                print("Null response, breaking")
                break
            if report_term_type == "2" and page_num == 2:
                print("Enough, breaking")
                break


def get_finance_info(symbol, report_type, report_term_type, page_num=1):
    cookies = {
        '_ga': 'GA1.2.230422991.1584951565',
        '__gads': 'ID=939e805c60e089ad-2211167027c40000:T=1602823376:S=ALNI_MbmHz_jz3CcyAmEXmjj-7OlO-7Tqg',
        'cto_bundle': 'KoIj5F9CTmJiTTFxZUpxbWJHVDFvVExtU2pVdzdabnkyT1ZVRkJXdnBVTUVLVlFlSXNxY1pBak1laU1oV1RZUUgzQm4lMkZDc1JzYlVMQVBUVGRtakVnSmc1SUVmQnk2VzVSa00lMkZsYW9kZ3gwNUM2SEJsMTJndEo4amolMkZLRCUyRmVHYzZMbWNKamk0b0JxVTV2NVNhMVElMkZGQkttdVV5dWFTMm1LQ2tKT2o5T0s1YzBaNjNBJTNE',
        'language': 'vi-VN',
        'Theme': 'Light',
        'AnonymousNotification': '',
        'ASP.NET_SessionId': 'rn4nv21u4sqxyz2mzdkrupwd',
        '__RequestVerificationToken': 'RPM1MuHm3PzP_ZStJwUaUHTTaCOLJhRncrWfeqkLbufN7j2e70L-uem2o8-zCd7R26wtpqBSc1atcln-A8O-e9MKiGMV82FhMYhkLfQf5s01',
        'vts_usr_lg': '43D7922B75A7DBC23BDF9D77E0D52F7BBF8A4085BABB95CB28616CD78AC9FB8DAD4018BF7A0C096BAF8B6EB39B0FAD51A5B7184052CE9FDE768E9482FFA2EFA8F434E4B40084F3EBD2A9BEF1BE10EF4F054F4C9CAE57D69C651FEFB2E0A2946153AE199A91D33BB82E52A097E2EE334D2B07E348B11D5C3EB2F56D5C53AFC2DD',
        'vst_usr_lg_token': 'nRxbtV3U2E2raN2Sggdb9w==',
        'fileDownload': 'true',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://finance.vietstock.vn',
        'Connection': 'keep-alive',
        'Referer': 'https://finance.vietstock.vn/%s/tai-chinh.htm' % symbol,
    }

    data = {
        'Code': symbol,
        'ReportType': report_type,
        'ReportTermType': report_term_type,
        'Unit': '1000000',
        'Page': str(page_num),
        'PageSize': '4',
        '__RequestVerificationToken': 'LnWe3GUGQ0btDUJciI8CFUo9ghx5oBxuWV82zeqYNbRjLblDW6ULuVK74T10jZwpyYkiPMR-y1JbMOFWaaPpuVe4ztBeLjW2QbP7OIiqhh_0-r74UQ85Wdvqlc_tSw-00'
    }
    response = common.wrap_request_post('https://finance.vietstock.vn/data/financeinfo', headers=headers, cookies=cookies, data=data)
    return response


def get_list_stock_symbols():
    cookies = {
        '_ga': 'GA1.2.230422991.1584951565',
        '__gads': 'ID=939e805c60e089ad-2211167027c40000:T=1602823376:S=ALNI_MbmHz_jz3CcyAmEXmjj-7OlO-7Tqg',
        'cto_bundle': 'KoIj5F9CTmJiTTFxZUpxbWJHVDFvVExtU2pVdzdabnkyT1ZVRkJXdnBVTUVLVlFlSXNxY1pBak1laU1oV1RZUUgzQm4lMkZDc1JzYlVMQVBUVGRtakVnSmc1SUVmQnk2VzVSa00lMkZsYW9kZ3gwNUM2SEJsMTJndEo4amolMkZLRCUyRmVHYzZMbWNKamk0b0JxVTV2NVNhMVElMkZGQkttdVV5dWFTMm1LQ2tKT2o5T0s1YzBaNjNBJTNE',
        'language': 'vi-VN',
        'Theme': 'Light',
        'AnonymousNotification': '',
        'ASP.NET_SessionId': 'rn4nv21u4sqxyz2mzdkrupwd',
        '__RequestVerificationToken': 'RPM1MuHm3PzP_ZStJwUaUHTTaCOLJhRncrWfeqkLbufN7j2e70L-uem2o8-zCd7R26wtpqBSc1atcln-A8O-e9MKiGMV82FhMYhkLfQf5s01',
        'vts_usr_lg': '43D7922B75A7DBC23BDF9D77E0D52F7BBF8A4085BABB95CB28616CD78AC9FB8DAD4018BF7A0C096BAF8B6EB39B0FAD51A5B7184052CE9FDE768E9482FFA2EFA8F434E4B40084F3EBD2A9BEF1BE10EF4F054F4C9CAE57D69C651FEFB2E0A2946153AE199A91D33BB82E52A097E2EE334D2B07E348B11D5C3EB2F56D5C53AFC2DD',
        'vst_usr_lg_token': 'nRxbtV3U2E2raN2Sggdb9w==',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://finance.vietstock.vn',
        'Connection': 'keep-alive',
        'Referer': 'https://finance.vietstock.vn/doanh-nghiep-a-z?page=1',
    }

    data = {
        'catID': '0',
        'industryID': '0',
        'page': '1',
        'pageSize': '50',
        'type': '0',
        'code': '',
        'businessTypeID': '0',
        'orderBy': 'Code',
        'orderDir': 'ASC'
    }
    list_corp = []
    for page_num in range(1, 65):
        data['page'] = page_num
        response = requests.post(
            'https://finance.vietstock.vn/data/corporateaz',
            headers=headers,
            cookies=cookies,
            data=data
        )
        print(response.content)
        # response_list = json.loads(response.content, encoding=)
        list_corp.extend(response.json(encoding='utf-8'))
        sleep_time = random.randint(1000, 3000)
        time.sleep(sleep_time * 1.0 / 1000)

    return list_corp


def crawl_list_stock_symbols():
    list_corp = get_list_stock_symbols()
    with open("output/list_stocks.json", "w") as fp:
        fp.write(json.dumps(list_corp))


_local_raw_list_corp = None


def load_local_list_stock_raw():
    global _local_raw_list_corp
    if _local_raw_list_corp is not None:
        return _local_raw_list_corp
    with open("output/list_stocks.json", "r") as fp:
        _local_raw_list_corp = json.load(fp)
    return _local_raw_list_corp


def filter_mandatory_stocks():
    list_corp = load_local_list_stock_raw()
    mandatory_exchange = {"HOSE", "UPCoM", "HNX"}
    return [corp["Code"] for corp in list_corp if corp["Exchange"] in mandatory_exchange]
