from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


options = webdriver.EdgeOptions()
options.add_argument("--headless")  # Run browser in headless mode (optional)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Specify the path to msedgedriver
driver = webdriver.Edge(
    #service=Service("edgedriver_mac64_m1/msedgedriver"),
    options=options
)

urls = []


def handle_brand(name):
    if name == "":
        return ""
    if name[0] == "\"":
        name = name[1:(len(name) - 1)]
    space_pos = name.find(" ")
    if space_pos != -1:
        check_name = name[:space_pos]
        if check_name.lower() == "gaming":
            name = name[space_pos + 1:]
    next_space = name.find(" ")
    if next_space != -1:
        brand = name[:next_space]
    else:
        brand = name
    return brand

def handle_price(price):
    price = price.replace("₫", "")
    price = price.replace(".", "")
    return int(price)

def handle_cpu(cpu):
    comma_pos = cpu.find("(")
    if comma_pos != -1:
        cpu = cpu[:comma_pos]
    return cpu

def get_cpu_brand(cpu):
    space_pos = cpu.find(" ")
    if space_pos != -1:
        return cpu[:space_pos]
    return cpu

def get_card_brand(card):
    space_pos = card.find(" ")
    if space_pos != -1:
        return card[:space_pos]
    return card

def handle_ram(ram):
    if ram[-2:].lower() == "gb":
        return ram, "GB"
    space_pos = ram.find(" ")
    if space_pos != -1:
        return ram[:space_pos], ram[space_pos + 1:]
    return ram, ""

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

resolution_map = {
    "FHD": 1920,
    "2K": 2048,
    "2.5K": 2560,
    "3K": 2880,
    "3.5K": 3440,
    "4K": 3840,
    "4K": 4096,
    "5K": 5120,
    "6K": 6144,
    "8K": 7680,
}

def get_resolution_name(width):
    if width == 0:
        return ""
    minn = 10000000000000
    resolution_name = ""
    for name, w in resolution_map.items():
        cmp_value = abs(w - width)
        if (cmp_value < minn):
            minn = cmp_value
            resolution_name = name
    return resolution_name

def get_screen_size(screen):
    comma_pos = screen.find(",")
    if comma_pos != -1:
        return screen[:comma_pos]
    return screen

def get_width_screen(screen):
    multiply_pos = screen.find("x")
    if multiply_pos != -1:
        return int(screen[:multiply_pos])
    return 0


if __name__ == "__main__":
    f = open("Crawl/cellphones.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    name_column = ["page", "name", "brand", "link", "image", "price", "old", "new", "cpu", "cpu_brand", "ram_capacity", "ram_brand", "hard_drive_type", "hard_drive_capacity", "card", "card_brand", "screen_size", "screen_type"]
    writer.writerow(name_column)

    driver = webdriver.Edge()
    driver.get("https://cellphones.com.vn/laptop.html")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#layout-desktop > div.cps-container.cps-body > div.cps-category > div > div.block-filter-sort > div.filter-sort__list-product > div"))
    )
    for _ in range(0):
        try:
            subscriber_popup_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#subscriberEmail > div.subscriber-popup.box-banner > div.subscriber-popup-body > button > div > svg"))
            )
            subscriber_popup_button.click()
            print("Clicked subscriber popup button.")
        except TimeoutException:
            pass  # If the popup does not appear, continue
        
        try:
            see_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-show-more.button__show-more-product"))
            )
            see_more_button.click()
            time.sleep(5)  # Allow time for products to load
            print("Clicked 'See More' button.")
        except StaleElementReferenceException:
            continue
        except Exception as e:
            print("Error occurred:", e)
            break

    for i in range(1, 5):
        try:
            elm = "#layout-desktop > div.cps-container.cps-body > div.cps-category > div > div.block-filter-sort > div.filter-sort__list-product > div > div.product-list-filter.is-flex.is-flex-wrap-wrap > div:nth-child(" + str(i) + ") > div.product-info > a"
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, elm))
            )
            href = element.get_attribute("href")
            urls.append(href)
            print("The href attribute is: ", href, "with order of: ", i)
        except:
            print("this product could not be located.")
            continue
    print(f"Collected {len(urls)} URLs")

    
    driver.quit()

    for i, url in enumerate(urls, 1):
        print(i)
        driver = webdriver.Edge()
        driver.get("https://cellphones.com.vn/laptop.html")
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#layout-desktop > div.cps-container.cps-body"))
            )
        except:
            print("Error: Page not found.")
            break
        
        try:
            image = driver.find_element(By.CSS_SELECTOR, "#v2Gallery > div > img").get_attribute("src")
        except:
            image = ""
        print(image)

        statistic = []
        try:
            name = driver.find_element(By.CSS_SELECTOR, "#productDetailV2 > section > div.product-detail__info > div.product-detail__info-left > h1").text
        except:
            name = ""

        try:
            price_tmp = driver.find_element(By.CSS_SELECTOR, "#productDetailV2 > section > div.product-detail__info > div.product-detail__info-right > div.product-detail__price > div.product-detail__price-new > p > span").text
            price = handle_price(price_tmp)
        except:
            price = ""

        old = 0
        new = 1

        brand = handle_brand(name)
        print(brand)
        cpu = ""
        card = ""
        ram = ""
        hard_drive = ""
        screen_size = ""
        screen_resolution = ""

        try:
            technical_info = driver.find_elements(By.CSS_SELECTOR, ".technical-content-item")
            for item in technical_info:
                key = item.find_element(By.TAG_NAME, "p").text
                value = item.find_element(By.TAG_NAME, "div").text
                if key == "Loại card đồ họa":
                    card = value.replace('®', '').replace('™', '')
                elif key == "Dung lượng RAM":
                    ram = value
                elif key == "Loại RAM":
                    ram_type = value
                elif key == "Ổ cứng":
                    hard_drive = value
                elif key == "Kích thước màn hình":
                    screen_size = value
                elif key == "Độ phân giải màn hình":
                    screen_resolution = value
                elif key == "Loại CPU":
                    cpu = value.replace('®', '').replace('™', '')
        except Exception as e:
            print("Error extracting technical info:", e)

        cpu = handle_cpu(cpu)
        cpu_brand = get_cpu_brand(cpu)
        card_brand = get_card_brand(card)
        ram_capacity, ram_brand = handle_ram(ram)
        hard_drive_type = "SSD"
        hard_drive_capacity = handle_hard_drive(hard_drive)
        screen_width = get_width_screen(screen_resolution)
        screen_type = get_resolution_name(screen_width)

        statistic = [
            "Cellphones", name, brand, url, image, price, old, new,
            cpu, cpu_brand, ram_capacity, ram_brand,
            hard_drive_type, hard_drive_capacity,
            card, card_brand, screen_size, screen_type
        ]
        writer.writerow(statistic)

        driver.quit()
        time.sleep(3)

f.close()


