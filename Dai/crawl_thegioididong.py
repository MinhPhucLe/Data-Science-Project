from bs4 import BeautifulSoup
import re
import requests
import logging
import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EDGE_DRIVER = "./edgedriver_win64/msedgedriver.exe"

service = Service(EDGE_DRIVER)
driver = webdriver.Edge(service=service)


base_url = "https://www.thegioididong.com"

headers_map = {
    'macOS': {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    },
    'Windows': {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
}

def getUrlFromHomepage(
parent_url: str = "https://www.thegioididong.com/laptop#c=44&o=13&pi=16"
):
    
    try:
        # Open a website
        driver.get(parent_url)
        #driver.execute_script("return document.readyState") == "complete"
        # wait = WebDriverWait(driver, 10)
        time.sleep(10)
        driver.execute_script("return document.readyState") == "complete"
        html_content = BeautifulSoup(driver.page_source, 'html.parser')
        href = [a['href'] for a in html_content.find_all('a', href=True)]
        urls = [url for url in href if '/laptop/' in url]
        return urls
    finally:
        # Close the browser
        driver.quit()

def wapper_childpage(child_url):
    cur_url = base_url + child_url
    try:
        # Fetch the page
        response = requests.get(cur_url, headers=headers_map.get('Windows'))
        response.raise_for_status()
        response.encoding = 'utf-8'
        html_content = BeautifulSoup(response.text, "html.parser")

        # Extract product name
        div_product_name = html_content.find('div', class_="product-name")
        product_name, data_url = None, None
        if div_product_name:
            product_name_element = div_product_name.find('h1')
            if product_name_element:
                product_name = product_name_element.get_text(strip=True)
            like_fanpage_div = div_product_name.find('div', class_='like-fanpage')
            if like_fanpage_div:
                data_url = like_fanpage_div.get('data-url')

        # Extract brand from breadcrumb
        brand = None
        breadcrumb = html_content.find('ul', class_='breadcrumb')
        if breadcrumb:
            li_elements = breadcrumb.find_all('li')
            if len(li_elements) > 1:
                brand_element = li_elements[1].find('a')
                if brand_element:
                    brand = brand_element.get_text(strip=True)

        # Extract price
        price, old, new = None, 0, 1
        div_price = html_content.find('div', class_="box-price")
        if div_price:
            price_present = div_price.find('p', class_='box-price-present')
            if price_present:
                price_match = re.search(r'[\d.]+', price_present.get_text(strip=True))
                if price_match:
                    price = price_match.group(0)
                    price = int(price.replace('.', ''))

        # Specifications
        cpu, cpu_brand = None, None
        ram_capacity, ram_brand = None, None
        hard_drive_type, hard_drive_capacity = None, None
        card, card_brand = None, None
        screen_size, screen_type = None, None

        div_box_specifi = html_content.find_all('div', class_='box-specifi')
        for div in div_box_specifi:
            div_title = div.find('h3')
            if div_title:
                div_title = div_title.get_text(strip=True)

            if 'Bộ xử lý' in div_title:
                spans = div.find_all('span')
                if spans:
                    cpu = spans[0].get_text(strip=True)
                    if 'Intel' in cpu:
                        cpu_brand = 'Intel'
                    elif 'Apple' in cpu:
                        cpu_brand = 'Apple'
                    elif 'AMD' in cpu:
                        cpu_brand = 'AMD'
                    elif 'Snapdragon' in cpu:
                        cpu_brand = 'Qualcomm'

            if 'Bộ nhớ RAM, Ổ cứng' in div_title:
                li = div.find_all('li')
                if li:
                    tmp = li[0].find('a') or li[0].find('span')
                    if tmp:
                        ram_capacity_match = re.match(r'\d+', tmp.get_text(strip=True))
                        if ram_capacity_match:
                            ram_capacity = ram_capacity_match.group()

                    tmp = li[1].find('a') or li[0].find('span') or li[1].find('span')
                    if tmp:
                        # print(tmp)
                        ram_type_match = re.match(r'(DDR|LDDR|LPDDR)\d', tmp.get_text(strip=True))
                        if ram_type_match:
                            ram_brand = ram_type_match.group()

                    tmp = li[4].find('a') or li[4].find('span')
                    if tmp:
                        # print(tmp)
                        hard_drive_capacity_match = re.match(r'\d+\s?(GB|TB)', tmp.get_text(strip=True))
                        if hard_drive_capacity_match:
                            hard_drive_capacity = hard_drive_capacity_match.group()
                        hard_drive_type_match = re.search(r'(SSD|HDD)', tmp.get_text(strip=True))
                        if hard_drive_type_match:
                            hard_drive_type = hard_drive_type_match.group()

            if 'Đồ họa và Âm thanh' in div_title:
                li = div.find_all('li')
                if li:
                    tmp =  li[0].find('span')
                    if tmp:
                        card = tmp.get_text(strip=True)
                        #print(card)
                        Nvidia_match = r'RTX \d{4}(\sTi)?|GTX \d{3,4}|Jetson \w+|CMP \d{2}HX|Geforce'
                        AMD_match = r'(Radeon|Instinct|RX \d{4}|MI\d{3,4})'
                        if re.search(Nvidia_match, card):
                            card_brand = 'Nvidia'
                        elif re.search(AMD_match, card):
                            card_brand = 'AMD'
                        elif ('Intel' in card or 'intel' in card):
                            card_brand = 'Intel'
                        else:
                            card_brand = 'Apple'

            if 'Màn hình' in div_title:
                li = div.find_all('li')
                if li:
                    tmp = li[0]
                    # print(tmp)
                    if tmp:
                        tmp_child = tmp.find('span')
                        # print(tmp_child)
                        screen_size_match = re.match(r'\d+(\.\d+)?', tmp_child.get_text(strip=True))
                        if screen_size_match:
                            # print(screen_size_match)
                            screen_size = screen_size_match.group()
                    tmp = li[1]
                    if tmp:
                        screen_type_match = re.search(r'(\dK|\d.\dK|Retina|.*HD|WUXGA)', tmp.get_text(strip=True))
                        if screen_type_match:
                            screen_type = screen_type_match.group()

        # Return extracted data
        print(f"Done crawled at {cur_url}")
        return {
            "page": "thegioididong",
            "name": product_name,
            "brand": brand,
            "link": data_url,
            "price": price,
            "old": old,
            "new": new,
            "cpu": cpu,
            "cpu_brand": cpu_brand,
            "ram_capacity": ram_capacity,
            "ram_brand": ram_brand,
            "hard_drive_type": hard_drive_type,
            "hard_drive_capacity": hard_drive_capacity,
            "card": card,
            "card_brand": card_brand,
            "screen_size": screen_size,
            "screen_type": screen_type,
        }
    except requests.exceptions.Timeout:
        print(f"ERROR at {cur_url}: Request timed out.")
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR at {cur_url}: HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"ERROR at {cur_url}: Request error: {req_err}")
    except Exception as e:
        print(f"ERROR at {cur_url}: {e}")

    return None

if __name__ == "__main__":
    urls = getUrlFromHomepage()
    rows = [wapper_childpage(url) for url in urls]
    rows = [r for r in rows if r is not None]
    #rows = [row for row in rows if row is not None]
    df = pd.DataFrame(rows)
    # Save DataFrame to a CSV file
    df.to_csv("thegioididong.csv", index=False)
    # print(wapper_childpage('/laptop/asus-vivobook-go-15-e1504fa-r5-nj776w?itm_medium=shortcode&itm_content=listing_product_1054839&itm_source=hoidap&sclient=mobile,12490000.0,0,1,AMD'))
