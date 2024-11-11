import asyncio
import csv
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start_urls = ['https://memoryzone.com.vn/laptop']
base_url = "https://memoryzone.com.vn/laptop?q=collections:2828130&page=" #"&view=grid"
base_link = "#template-collection > section.section.wrap_background > div > div.bg_collection.section > div > div > div.category-products.products > div.products-view.products-view-grid.collection_reponsive.list_hover_pro > div.row.product-list.content-col > div:nth-child(" # 16) > div > form > div.product-info > h3 > a"
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException

for i in range(2, 15):
    url = base_url + str(i) + "&view=grid"
    start_urls.append(url)

async def fetch_page(client, url):
    try:
        response = await client.get(url, timeout=120)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching the page: {e}")
        return None

def handle_name(name):
    open_bracket = name.find("(")
    if open_bracket != -1:
        name = name[:open_bracket - 1]
    return name

def handle_brand(name):
    if name.lower().find("asus") != -1:
        return "Asus"
    if name.lower().find("acer") != -1:
        return "Acer"
    if name.lower().find("dell") != -1:
        return "Dell"
    if name.lower().find("hp") != -1:
        return "HP"
    if name.lower().find("lenovo") != -1:
        return "Lenovo"
    if name.lower().find("msi") != -1:
        return "MSI"
    if name.lower().find("apple") != -1:
        return "Apple"
    if name.lower().find("lg") != -1:
        return "LG"
    if name.lower().find("microsoft") != -1:
        return "Microsoft"
    if name.lower().find("macbook") != -1:
        return "Apple"
    if name.lower().find("thinkpad") != -1:
        return "Lenovo"
    if name.lower().find("ideapad") != -1:
        return "Lenovo"

    brand = name
    space_pos = name.find(" ")
    if space_pos != -1:
        name = name[(space_pos + 1):]
        print(name)
        next_space = name.find(" ")
        if next_space != -1:
            brand = name[:next_space]
        else:
            brand = name
    return brand

def handle_cpu(cpu):
    open_bracket = cpu.find("(")
    if open_bracket != -1:
        cpu = cpu[:(open_bracket - 1)]
    return cpu

def handle_cpu_brand(cpu):
    temp_cpu = cpu[:2]
    brand = cpu
    if temp_cpu.lower() == "i5" or temp_cpu.lower() == "i7" or temp_cpu.lower() == "i3" or temp_cpu.lower() == "i9":
        return "Intel"
    space_pos = cpu.find(" ")
    if space_pos != -1:
        brand = cpu[:space_pos]
    if brand.lower() == "Qualcomm":
        return "Snapdragon"
    return brand

def handle_price(price):
    cleaned_price = price.replace('.', '')
    cleaned_price = cleaned_price[:-2]
    if cleaned_price.find("Liên") != -1:
        return None
    else:
        return int(cleaned_price)

def handle_ram(ram):
    print("RAM: ", ram)
    open_bracket = ram.find("(")
    ram_capacity = ""
    ram_type = ""
    if open_bracket != -1:
        ram_capacity = ram[:(open_bracket - 1)]
    else:
        GB_pos = ram.find("GB")
        if GB_pos != -1:
            ram_capacity = ram[:GB_pos + 3]
            print("HERE:", ram_capacity)
            temp_ram = ram[GB_pos + 3:]
            print("HERE 1: ", temp_ram)
            next_space = temp_ram.find(" ")
            if next_space != -1:
                ram_type = temp_ram[:next_space]
            else:
                ram_type = temp_ram
    return ram_capacity, ram_type

def handle_card(card):
    space_pos = card.find(" ")
    card_type = card
    if space_pos != -1:
        card_type = card[:space_pos]
    return card_type

def handle_hard_drive(hard_drive):
    Gb_index = hard_drive.find('GB')
    if Gb_index != -1:
        hard_drive_capacity = hard_drive[:Gb_index + 2]
    else:
        space_pos = hard_drive.find(" ")
        if space_pos != -1:
            hard_drive_capacity = hard_drive[:space_pos]
        else:
            hard_drive_capacity = hard_drive
    return hard_drive_capacity

def find_resolution(screen):
    if screen.find("Full HD"):
        return "FHD"
    if screen.find("2K"):
        return "2K"
    if screen.find("4K"):
        return "4K"
    if screen.find("3K"):
        return "3K"
    if screen.find("QHD"):
        return "2.5K"

def handle_screen(screen_size, screen_type):
    check_type = 0
    if screen_type != "":
        check_type = 1
    if screen_size.find("inch") != -1:
        screen_size = screen_size.replace("inch", "")
        screen_size = screen_size[:(len(screen_size) - 1)]
    if check_type == 0:
        open_pos = screen_size.find("\"")
        if open_pos != -1:
            screen_type = find_resolution(screen_size)
            screen_size = screen_size[:open_pos]
        else:
            open_pos = screen_size.find("'")
            if open_pos != -1:
                screen_type = find_resolution(screen_size)
                screen_size = screen_size[:open_pos]
    else:
        if screen_type.find("WQXGA") or screen_type.find("QHD"):
            screen_type = "2.5K"
        if screen_type.find("FULL HD"):
            screen_type = "FHD"
        K_pos = screen_type.lower().find("k")
        if K_pos != -1:
            screen_type = screen_type[:(K_pos + 1)]
    return screen_size, screen_type

async def main():
    f = open("memoryzone.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    name_column = ["page", "name", "brand", "link", "image", "price", "old", "new", "cpu", "cpu_brand", "ram_capacity",
                   "ram_brand", "hard_drive_type", "hard_drive_capacity", "card", "card_brand", "screen_size",
                   "screen_type"]
    writer.writerow(name_column)
    async with httpx.AsyncClient() as client:
        for i, url in enumerate(start_urls):
            print(f"Processing URL {i + 1}/{len(start_urls)}: {url}")
            data = await fetch_page(client, url)
            if data is None:
                continue

            html = BeautifulSoup(data, 'html.parser')

            for j in range(1, 21):
                link_selector = f'{base_link}{j}) > div > form > div.product-info > h3 > a'
                image_selector = f'{base_link}{j}) > div > form > div.product-thumbnail.pos-relative > a > img.product-thumbnail__img.product-thumbnail__img--secondary'
                try:
                    product_element = html.select_one(link_selector)
                    selected_link = product_element.get('href') if product_element else None
                except Exception as e:
                    print(f"Error getting link for item {j}: {e}")
                    selected_link = None
                if selected_link:
                    absolute_link = urljoin(url, selected_link)
                else:
                    continue
                print(absolute_link)

                try:
                    image_element = html.select_one(image_selector)
                    selected_image = image_element.get('src') if image_element else None
                except Exception as e:
                    selected_image = ""

                if selected_image:
                    absolute_image = urljoin(url, selected_image)
                # print(absolute_image)

                try:
                    product_name_tmp = html.select_one(link_selector).text
                except:
                    product_name_tmp = ""

                name = handle_name(product_name_tmp)
                print(name)
                brand = handle_brand(name)
                print("name and brand:", name, brand)

                if selected_link:

                    access_link = await fetch_page(client, absolute_link)
                    print(absolute_link)
                    if access_link is None:
                        continue

                    soup = BeautifulSoup(access_link, 'html.parser')

                    # try:
                    #     price_tmp = soup.select_one("#add-to-cart-form > div.ae-flashsale.disabled > div > div.flashsale__product > div.price-box > span.special-price > span")
                    #     price = handle_price(price_tmp)
                    # except Exception as e:
                    #     print(f"Error getting price for item {j}: {e}")
                    #     price = None

                    price_element = soup.select_one(".special-price span")

                    if price_element:
                        price = price_element.get_text(strip=True).replace('$', '').strip()
                        price = handle_price(price)
                        print(price)
                    else:
                        price = ""
                        print("Price not found.")

                    old = 0
                    new = 1
                    parent_element = soup.find("div", class_="product-description") or soup.find("div",
                                                                                                 class_="product-summary")

                    specs = {}
                    if parent_element:
                        ul_element = parent_element.find("ul")
                        if ul_element:
                            li_elements = ul_element.find_all("li")
                            for li in li_elements:
                                # print(li.get_text(strip=True))
                                if ":" in li.text:
                                    key, value = li.text.split(":", 1)
                                    specs[key.strip()] = value.strip()
                            # print(specs)
                        else:
                            print("<ul> element was not found within the parent.")
                    else:
                        print("Parent element with product description class not found.")

                    if specs:
                        cpu = ""
                        card = ""
                        ram = ""
                        ram_capacity = ""
                        ram_type = ""
                        hard_drive = ""
                        screen_type = ""
                        screen_size = ""
                        check = 0
                        for key, value in specs.items():
                            if key == "CPU":
                                cpu = value.replace('®', '').replace('™', '')
                            if key == "Card đồ họa rời" or key == "VGA":
                                if value != "-" and value != "" and value != " ":
                                    card = value
                                    check = 1
                            if key == "Card đồ họa tích hợp":
                                if check == 0:
                                    card = value
                            if key.lower().find("ram") != -1:
                                ram = value
                            if key == "Ổ cứng":
                                hard_drive = value
                            if key == "Kích thước màn hình" or key == "Màn hình":
                                screen_size = value
                            if key == "Độ phân giải":
                                screen_type = value

                        cpu = handle_cpu(cpu)
                        cpu_brand = handle_cpu_brand(cpu)
                        print(cpu)
                        print(cpu_brand)
                        ram_capacity, ram_type = handle_ram(ram)
                        ram_capacity = re.sub(r'\u00A0', ' ', ram_capacity)
                        if ram_capacity[len(ram_capacity) - 1] == " ":
                            ram_capacity = ram_capacity[:len(ram_capacity) - 1]
                        print(ram_capacity)
                        print(ram_type)
                        if ram_type == "":
                            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                            browser.get(absolute_link)
                            time.sleep(2)
                            try:
                                WebDriverWait(browser, 20).until(
                                    EC.presence_of_element_located((By.ID, "template-product"))
                                )
                            except TimeoutException:
                                print("Timeout: Element with tag 'main' not found within the specified time.")
                            xpath = "/html/body/section[2]/section[3]/div/div/div[2]/div/div[3]/a"
                            try:
                                configuration_button = WebDriverWait(browser, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "#template-product > section.product.details-main > section.section.sec_tab > div > div > div.col-12.col-xl-4.product_sidebar.pl-0.pl-sm-3.pr-0 > div > div.ega-pro__seemore.text-center.pos-relative.mt-3.js-show-specifications > a"))
                                )
                                browser.execute_script("arguments[0].scrollIntoView();", configuration_button)
                                time.sleep(1)  # Give time for any dynamic effects
                                configuration_button.click()
                                try:
                                    table = browser.find_element(By.XPATH,
                                                                 '/html/body/section[2]/section[3]/div/div/div[2]/div/div[4]/div/div/div[2]/table/tbody')
                                    # print("Table found.")
                                    rows = table.find_elements(By.TAG_NAME, 'tr')
                                    table_data = []
                                    for row in rows:
                                        cells = row.find_elements(By.TAG_NAME, "td")
                                        row_data = [cell.text.strip() for cell in cells if cell.text.strip()]
                                        # print(row_data)
                                        if row_data:  # Only add non-empty rows
                                            table_data.append(row_data)
                                    for i, row in enumerate(table_data):
                                        # print(row)
                                        # print(len(row))
                                        if len(row) == 2:
                                            key = row[0]
                                            value = row[1]
                                            # print("HERE is key:", key)
                                            if key == "Loại RAM":
                                                ram_type = value
                                except Exception as e:
                                    print("Error:", e)
                                browser.quit()
                            except:
                                print("Lack of specific information")
                                continue
                        time.sleep(1)
                        print(ram_capacity)
                        print(ram_type)
                        print(card)
                        card = re.sub(r'\u00A0', ' ', card)
                        hard_drive_capacity = handle_hard_drive(hard_drive)
                        hard_drive_type = "SSD"
                        screen_size, screen_type = handle_screen(screen_size, screen_type)
                        card_type = handle_card(card)
                        print(screen_size)
                        print(screen_type)
                        # print(ram)
                        # print(hard_drive)
                        # print(screen_size)
                        # print(screen_type)
                statistic = [
                    "Memoryzone", name, brand, absolute_link, absolute_image, price, old, new,
                    cpu, cpu_brand, ram_capacity, ram_type,
                    hard_drive_type, hard_drive_capacity,
                    card, card_type, screen_size, screen_type
                ]
                writer.writerow(statistic)
                    # print(price)



asyncio.run(main())