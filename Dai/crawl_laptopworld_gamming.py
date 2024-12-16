from bs4 import BeautifulSoup
import re
import requests
import logging
import os
import time
import pandas as pd
import asyncio
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

EDGE_DRIVER = "./edgedriver_win64/msedgedriver.exe"

options = webdriver.EdgeOptions()
options.add_argument("--headless")  # Run browser in headless mode (optional)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument(UserAgent().random)
# service = Service(EDGE_DRIVER)
driver = webdriver.Edge(options=options)

# session = requests.Session()
# retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
# session.mount('http://', HTTPAdapter(max_retries=retries))

base_url = "https://laptopworld.vn/"

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

parent_urls= ["https://laptopworld.vn/laptop-games-do-hoa.html", "https://laptopworld.vn/laptop-van-phong.html"]
def getUrlFromHomepage(
    parent_url
    ):
    try:
        # driver.get("http://localhost:50932")
        addition_term = '?page={page_number}'
        urls = []
        for i in range(1,31):
            current_url = parent_url+addition_term.format(page_number=str(i))
            driver.get(current_url)
            time.sleep(5)
            driver.execute_script("return document.readyState") == "complete"
            html_content = BeautifulSoup(driver.page_source, 'html.parser')
            for tag in html_content.find_all(['script', 'style', 'header', 'footer', 'nav', 'aside']):
                tag.decompose()
            try:
                div_containers = html_content.find_all('div', class_='p-container')
                if(len(div_containers)>0):
                    for item in div_containers:
                        anchor_tag = item.find('a', class_='p-img', href=True)
                        if anchor_tag:
                            href = anchor_tag.get('href')
                            urls.append(href)
                else: 
                    print(f"No products found on page {i}. Stopping pagination.")
                    break
                print("Taking list of laptop's urls in page ", str(i))
            except Exception as e:
                print("ERROR: ", e)
        return urls
    finally:
        # Close the browser
        driver.quit()

def wapper_childpage(child_url):
    try:
        cur_url = 'https://laptopworld.vn'+child_url
        # Fetch the page content
        response = requests.get(cur_url, headers=headers_map.get('Windows'))
        response.raise_for_status()
        response.encoding = 'utf-8'
        html_content = BeautifulSoup(response.text, "html.parser")

        # Extract product name
        div_product_name = html_content.find('div', class_="content-top-detail-left")
        product_name = None
        if div_product_name:
            product_name_element = div_product_name.find('h1')
            if product_name_element:
                product_name = product_name_element.get_text(strip=True)

        # Extract brand from product name
        brand = None
        brand_match = re.match(r'Laptop\s(\w+)', product_name)
        if brand_match:
            brand = brand_match.group().strip()
        else:
            brand = re.match(r'\w+', product_name)
            brand = brand.group(00)

        # Extract price
        price = None
        div_price = html_content.find("div", class_="price-chinhhang")
        if div_price:
            price_present = div_price.find('del')
            if price_present:
                price_match = re.search(r'[\d.]+', price_present.get_text(strip=True))
                if price_match:
                    price = int(price_match.group(0).replace('.', ''))
        else:
            price_sale = html_content.find("div", class_='price-khuyemai')
            if price_sale:
                price_match = re.search(r'[\d.]+', price_sale.get_text(strip=True))
                if price_match:
                    price = int(price_match.group(0).replace('.', ''))
                

        # Initialize specifications as None
        cpu, cpu_brand = None, None
        ram_capacity, ram_brand = None, None
        hard_drive_type, hard_drive_capacity = None, None
        card = None
        screen_size, screen_type = None, None
        div_overview = html_content.find('div', class_='product-summary-content')
        # Overview and specifications section
        div_item = div_overview.find_all('div', class_='item')
        for idx, item in enumerate(div_item):
            text = item.get_text(strip=True)
            clean_text = re.sub(r'\(.*?\)', '', text)  # Remove parentheses content
            clean_text = re.sub(r'[^a-zA-Z0-9\s\u0100-\u1EF9\.\:]', '', clean_text)  # Remove non-alphanumeric characters
            # print(f'{idx}: {clean_text}')
            # Extract CPU information
            if 'cpu' in clean_text.lower():
                cpu = re.sub(r'.*\:\s', '', clean_text)
                if 'intel' in cpu.lower():
                    cpu_brand = 'Intel'
                elif 'apple' in cpu.lower():
                    cpu_brand = 'Apple'
                elif 'amd' in cpu.lower():
                    cpu_brand = 'AMD'
                elif 'snapdragon' in cpu.lower():
                    cpu_brand = 'Qualcomm'

            # Extract RAM information
            if 'ram' in clean_text.lower():
                # print(clean_text)
                tmp = re.sub(r'.*\:\s', '', clean_text)                
                ram_capacity_match = re.search(r'\d+GB', tmp)
                if ram_capacity_match:
                    ram_capacity = re.search(r'\d+', ram_capacity_match.group()).group()
                ram_brand_match = re.search(r'(DDR\d|LDDR\d)', tmp)
                if ram_brand_match:
                    ram_brand = ram_brand_match.group(00)

            # Extract Hard Drive information
            if 'ổ cứng' in clean_text.lower():
                # print('okok')
                # print(clean_text)
                tmp = re.sub(r'.*\:\s', '', clean_text)
                hard_drive_capacity_match = re.search(r'\d+(GB|TB)', tmp)
                if hard_drive_capacity_match:
                    hard_drive_capacity = hard_drive_capacity_match.group()
                hard_drive_type_match = re.search(r'(SSD|HDD)', tmp)
                if hard_drive_type_match:
                    hard_drive_type = hard_drive_type_match.group()

            # Extract VGA (Graphics Card) information
            if 'vga' in clean_text.lower():
                tmp = re.sub(r'.*\:\s', '', clean_text)
                card = tmp
                Nvidia_match = r'RTX \d{4}(\sTi)?|GTX \d{3,4}|Jetson \w+|CMP \d{2}HX|Geforce'
                AMD_match = r'(Radeon|Instinct|RX \d{4}|MI\d{3,4})'
                if re.search(Nvidia_match, card, re.IGNORECASE):
                    card_brand = 'Nvidia'
                elif re.search(AMD_match, card, re.IGNORECASE):
                    card_brand = 'AMD'
                elif re.search(r'Intel', card, re.IGNORECASE):
                    card_brand = 'Intel'
                elif re.search(r'Qualcom', card, re.IGNORECASE):
                    card_brand = 'Qualcom'
                else:
                    card_brand = 'Apple'

            # Extract Display information
            if 'display' in clean_text.lower():
                tmp = re.sub(r'.*\:\s', '', clean_text)
                # print(clean_text)
                screen_size_match = re.match(r'\d+(\.\d+)?\s?inch', tmp)
                if screen_size_match:
                    screen_size = screen_size_match.group()
                    screen_size = re.sub(r'inch','', screen_size)
                screen_type_match = re.search(r'(HD|Full HD|Quad HD|Ultra HD|WQHD|SUHD|Retina|Retina HD|2K|4K|8K|OLED|AMOLED|Super AMOLED|LCD|IPS|TFT|Mini-LED|Micro-LED)', tmp, re.IGNORECASE)
                if screen_type_match:
                    screen_type = screen_type_match.group()

        # Return the extracted data
        print(f"Done crawling at {cur_url}")
        return {
            "page": "laptopworld",
            "name": product_name,
            "brand": brand,
            "link": cur_url,
            "price": price,
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
    child_urls = []
    # child_urls.extend(getUrlFromHomepage(parent_urls[0]))
    child_urls.extend(getUrlFromHomepage(parent_urls[0]))

    rows = [wapper_childpage(url) for url in child_urls]
    rows = [r for r in rows if r is not None]
    df = pd.DataFrame(rows)
    df.to_csv("laptopworld_gamming.csv", index=False)
    # print(wapper_childpage("/laptop-msi-stealth-a16-ai-a3xvgg-208vn"))
