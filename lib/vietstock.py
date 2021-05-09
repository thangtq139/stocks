import requests
import random
import json
import time


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
    #  with open("output/list_stocks.json", "w") as fp:
    #      fp.write(json.dumps(list_corp).encode("utf-8"))

    #  print("data_len = %s" % len(list_corp))
