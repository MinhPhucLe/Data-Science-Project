from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException

urls = []

def handle_price(price):
    price = price.replace("₫", "")
    price = price.replace(".", "")
    return int(price)

def handle_cpu(cpu):
    comma_pos = cpu.find(",")
    if comma_pos != -1:
        cpu = cpu[:comma_pos]
    return cpu

def get_cpu_brand(cpu):
    space_pos = cpu.find(" ")
    if space_pos != -1:
        cpu_brand = cpu[:space_pos]
    else:
        cpu_brand = cpu
    return cpu_brand

def get_card_brand(card):
    space_pos = card.find(" ")
    if space_pos != -1:
        card_brand = card[:space_pos]
    else:
        card_brand = card
    return card_brand

def is_last_char_z(string):
    return string[-1].lower() == 'z' if string else False

def handle_ram(ram):
    if is_last_char_z(ram):
        bck_fnd = ram.rfind(' ')
        ram = ram[:bck_fnd]
    space_pos = ram.find(" ")
    if space_pos != -1:
        ram_capacity = ram[:space_pos]
        ram_type = ram[space_pos + 1:]
    else:
        GB_index = ram.find('GB')
        if GB_index != -1:
            ram_capacity = ram
            ram_type = " "
        else:
            ram_capacity = " "
            ram_type = ram
    return ram_capacity, ram_type

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
        screen = screen[:comma_pos]
        inch_pos = screen.find("inch")
        if inch_pos != -1:
            screen_size = screen[:inch_pos]
        else:
            screen_size = screen
    else:
        inch_pos = screen.find("inch")
        if inch_pos != -1:
            screen_size = screen[:inch_pos]
        else:
            screen_size = screen
    return screen_size

def get_width_screen(screen):
    multiply_pos = screen.find("x")
    if multiply_pos != -1:
        width = screen[(multiply_pos - 5):(multiply_pos - 1)]
    else:
        width = 0
    return int(width)

if __name__ == "__main__":
    f = open("thinkpro.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    name_column = ["page", "name", "brand", "link", "image", "price", "old", "new", "cpu", "cpu_brand", "ram_capacity", "ram_brand", "hard_drive_type", "hard_drive_capacity", "card", "card_brand", "screen_size", "screen_type"]
    writer.writerow(name_column)

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    browser.get("https://thinkpro.vn/laptop")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#__layout > div > main"))
    )

    for _ in range(20):
        try:
            see_more_button = WebDriverWait(browser, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#__layout > div > main > div.mt-8.container > div.mt-6.flex.justify-center > button"))
            )
            see_more_button.click()
            time.sleep(3)
            print("HERE")
        except StaleElementReferenceException:
            continue  # Retry on stale element
        except Exception as e:
            print("See More button not found or no longer clickable.", e)
            break

    for i in range(1, 125):
        try:
            elm = "#__layout > div > main > div:nth-child(4) > div.mt-4 > section > div > a:nth-child(" + str(i) + ")"
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, elm))
            )
            href = element.get_attribute("href")
            urls.append(href)
            print("The href attribute is: ", href, "with order of: ", i)
        except:
            print("this product could not be located.")
            continue

    print(f"Collected {len(urls)} URLs")
    browser.quit()

    for i, url in enumerate(urls, 1):
        print(i)
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        try:
            browser.get(url)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#__layout > div > main"))
            )
        except:
            print("Error: Page not found.")
            break
        try:
            image = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/div/div/div[2]/section/div[2]/div/div/div[1]/div[1]/img').get_attribute("src")
        except:
            image = ""
        # print(image)
        statistic = []
        try:
            name = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div/div[1]/div/section[1]/div/div[1]/div[2]/h1').text
        except:
            name = ""
        try:
            price_tmp = browser.find_element(By.XPATH, '//*[@id="__layout"]/div/main/div/div/div[1]/div/section[1]/div/div[3]/div[1]/span').text
            price = handle_price(price_tmp)
        except:
            price = ""
        old = 0
        new = 1
        # print("Product ",i, ": ", name, price)
        brand = handle_brand(name)
        print(brand)
        cpu = ""
        card = ""
        ram = ""
        hard_drive = ""
        screen = ""
        for k in range(2, 4):
            xpath = '/html/body/div[1]/div/div/main/div/div/div[2]/div[' + str(k) + ']/section[1]/div/button/span'
            try:
                configuration_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                configuration_button.click()
                time.sleep(6)

                try:
                    table = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table.w-full"))
                    )

                    rows = table.find_elements(By.TAG_NAME, "tr")

                    # Iterate through rows and extract text
                    table_data = []
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        row_data = [cell.text.strip() for cell in cells if cell.text.strip()]
                        if row_data:  # Only add non-empty rows
                            table_data.append(row_data)

                    # Print all extracted table data
                    for i, row in enumerate(table_data):
                        #print(f"Row {i + 1}: {row}")
                        check = 0
                        if len(row) == 2:
                            key = row[0]
                            value = row[1]
                            if (key == "Loại CPU"):
                                cpu = value.replace('®', '').replace('™', '')
                            if (key == "Card rời"):
                                if value != "Không" and value != "Card Onboard-roi":
                                    check = 1
                                    card = value.replace('®', '').replace('™', '')
                            if (key == "Card onboard"):
                                if check == 0:
                                    card = value.replace('®', '').replace('™', '')
                            if (key == "Dung lượng"):
                                ram = value
                            if (key == "Dung lượng SSD"):
                                hard_drive = value
                            if (key == "Màn hình"):
                                screen = value
                        else:
                            continue
                except Exception as e:
                    print("Error:", e)
                break
            except:
                print("Lack of specific information")
                continue
        #print("Statistic: ", cpu, card, ram, hard_drive, screen)
        cpu = handle_cpu(cpu)
        cpu_brand = get_cpu_brand(cpu)
        card_brand = get_card_brand(card)
        ram_capacity, ram_type = handle_ram(ram)
        # print("Statistic: ", ram)
        # print("Ram Capacity: ", ram_capacity)
        # print("Ram Type: ", ram_type)
        hard_drive_type = "SSD"
        hard_drive_capacity = handle_hard_drive(hard_drive)
        # print("Statistic: ", hard_drive)
        # print("Hard Drive Capacity: ", hard_drive_capacity)
        # print("Hard Drive Type: ", hard_drive_type)
        screen_width = get_width_screen(screen)
        screen_size = get_screen_size(screen)
        screen_type = get_resolution_name(screen_width)
        print("Statistic: ", screen)
        print("Screen Width: ", screen_width)
        print("Screen Size: ", screen_size)
        print("Screen Type: ", screen_type)
        statistic = [
            "Thinkpro", name, brand, url, image, price, old, new,
            cpu, cpu_brand, ram_capacity, ram_type,
            hard_drive_type, hard_drive_capacity,
            card, card_brand, screen_size, screen_type
        ]
        writer.writerow(statistic)
        browser.quit()
        time.sleep(3)

    # Close the browser

f.close()