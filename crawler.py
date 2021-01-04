import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
base_headers = {
    "accept": "*/*",
    "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}


def get_all_product():
    result = []

    phone_category = requests.get('https://www.dienmayxanh.com/dien-thoai', headers=base_headers)

    if phone_category.status_code == 200:
        try:
            soup = BeautifulSoup(phone_category.text, 'html.parser')
            total = int(soup.select_one('#total').get('value'))
            remain_count = int(soup.select_one('#remaincount').get('value'))

            for product in soup.select('#product-list > div.prdItem.prdItemGetDelStt'):
                result.append({
                    'id': product.get('data-id'),
                    'link': f"https://www.dienmayxanh.com/{product.get('data-href')}"

                })

            print(f'gotten {len(result)} product in phone category')

            page_cnt = 1
            # get in next page
            while remain_count > 0 and total > len(result):
                payload = {"catid": "42",
                           "manufactureUrl": "",
                           "catname": "Điện thoại",
                           "caturl": "dien-thoai",
                           "caturlOriginal": "dien-thoai",
                           "pagesize": "25",
                           "pageidx": str(page_cnt),
                           "isFilter": "0",
                           "sortby": "0",
                           "dong-may": "Chọn theo dòng", "manu_80": "0", "manu_2": "0", "manu_1971": "0",
                           "manu_2235": "0",
                           "manu_2236": "0", "manu_17201": "0", "manu_2326": "0", "manu_17566": "0", "manu_1": "0",
                           "manu_104": "0",
                           "manu_19": "0", "manu_5332": "0", "manu_4832": "0", "manu_20673": "0", "pri_7": "0",
                           "pri_9": "0",
                           "pri_289": "0", "pri_562": "0", "pri_252": "0", "pri_253": "0", "new": "0",
                           "installment0": "0",
                           "docquyen": "0", "onlineonly": "0", "pro_39237": "0", "pro_39238": "0", "pro_62879": "0",
                           "pro_163466": "0",
                           "pro_163467": "0", "pro_172937": "0", "pro_172938": "0", "pro_172939": "0",
                           "pro_172941": "0",
                           "pro_172942": "0", "pro_172943": "0", "pro_172944": "0", "pro_163409": "0",
                           "pro_140894": "0",
                           "pro_140895": "0", "pro_140896": "0", "pro_176504": "0", "pro_173170": "0",
                           "pro_173171": "0",
                           "pro_173172": "0", "pro_173173": "0", "pro_173174": "0", "pro_140891": "0",
                           "pro_140890": "0",
                           "pro_163351": "0", "pro_40435": "0", "pro_57311": "0", "pro_57279": "0"}
                headers = base_headers
                headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                headers['x-requested-with'] = 'XMLHttpRequest'
                headers = {
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "accept": "*/*",
                    "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5"
                }
                print(f'page {page_cnt}: getting data')
                next_page = requests.post('https://www.dienmayxanh.com/aj/TeleCommunication/ProductBox', data=payload,
                                          headers=headers)
                if next_page.status_code == 200:
                    soup_in_page = BeautifulSoup(next_page.text, 'html.parser')
                    product_in_page = [
                        {
                            'id': product.get('data-id'),
                            'link': f"https://www.dienmayxanh.com/{product.get('data-href')}"
                        }
                        for product in soup_in_page.select('div.prdItem.prdItemGetDelStt')]
                    print(f'page {page_cnt}: gotten {len(product_in_page)} product')
                    if len(product_in_page) > 0:
                        for product in product_in_page:
                            result.append(product)
                        remain_count -= len(product_in_page)
                        page_cnt += 1
                        print(f'remain count: {remain_count}, next page: {page_cnt}')
                    else:
                        break
        except ValueError:
            print('cant convert str to int')
    return result


def get_product_info(product):
    print(f"id {product.get('id')}: get product info")
    product_response = requests.get(product.get('link'), headers=base_headers)
    if product_response.status_code == 200:
        soup = BeautifulSoup(product_response.text, 'html.parser')
        #params = {"productId":  {product.get('id'), "siteId": "1", }
        link = 'https://www.dienmayxanh.com/aj/ProductV3/ProductRatingStar/'
        params = {"productId":  {product.get('id')}, "siteId": "1", "gpa": "1", "totalCount": "1"}
        rating = requests.post(link, params = params)

        parser_ = BeautifulSoup(rating.text, 'html.parser')
        #print("_")
        bTags = []
        star_ave = ''
        for i in parser_.findAll('b'):
            bTags.append(i.text)
        star_sum = 0
        star = 5
        num_of_rating = 0
        for i in bTags:
            star_sum += int(i) * star
            num_of_rating += int(i)
            star -= 1
        if num_of_rating != 0:
            star_ave = star_sum/num_of_rating
        else:
            star_ave = 0
    
        price = soup.select_one(
            'strong.prPrice')
        #print(price)
        ram = soup.select_one(
            'span.specval.prop-50')
        rom = soup.select_one(
            'span.specval.prop-49')
        cpu = soup.select_one(
            'span.specval.prop-6059')
        screen = soup.select_one(
            'span.specval.prop-6459')
        rear_cam = soup.select_one(
            'span.specval.prop-27')
        front_cam = soup.select_one(
            'span.specval.prop-29')
        os = soup.select_one(
            'spen.specval.prop-72')
        size = soup.select_one(
            'span.specval.prop-88')
        pin_capacity = soup.select_one(
            'spen.specval.prop-84')
        record = soup.select_one(
            'span.specval.prop-36')
        radio = soup.select_one(
            'span.specval.prop-34')
        time = soup.select_one(
            'span.specval.prop-13045')
        if price:
            product['gia_tien'] = price.get_text()
        if ram:
            product['RAM'] = ram.get_text()
        if rom:
            product['ROM'] = rom.get_text()
        if cpu:
            product['CPU'] = cpu.get_text()
        if screen:
            product['Man_hinh'] = screen.get_text()
        if rear_cam:
            product['camera_sau'] = rear_cam.get_text()
        if front_cam:
            product['camera_truoc'] = front_cam.get_text()
        if os:
            product['he_dieu_hanh'] = os.get_text()
        if size:
            product['kich_thuoc'] = size.get_text()
        if pin_capacity:
            product['dung_luong_pin'] = pin_capacity.get_text()
        if record:
            product['ghi_am'] = record.get_text()
        if radio:
            product['radio'] = radio.get_text()
        if time:
            product['thoi_diem ra mat'] = time.get_text()

        product['rating'] = star_ave
        print(f'gotten: {product}')
    return product


if __name__ == '__main__':
    all_products = get_all_product()
    print(f'gotten total {len(all_products)} product')
    #product_info = get_product_info(all_products[0])
    product_info = [get_product_info(product) for product in all_products]
    data = pd.DataFrame(product_info)
    data.to_csv("data.csv", encoding = 'utf-8-sig')
    print("Done")