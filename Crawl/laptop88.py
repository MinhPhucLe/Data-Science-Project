import asyncio
import csv

import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start_urls = ['https://laptop88.vn/laptop-moi.html?sort=new']
baseurl = 'https://laptop88.vn/laptop-moi.html?sort=new&page='
base_link = 'body > main > div > div > div.product-list.d-flex.flex-wrap > div:nth-child('

# Generating URLs for pagination
for i in range(2, 16):
    url = baseurl + str(i)
    start_urls.append(url)


def handle_name(name):
    index = name.rfind('Laptop')
    if index == -1:
        bck_index = name.rfind(']')
        if bck_index == -1:
            hrz_index = name.find(' - ')
            if hrz_index == -1:
                vrt_index = name.find(' | ')
                if vrt_index == -1:
                    return name
                else:
                    return name[:vrt_index + 1]
            else:
                vrt_index = name.find('|')
                if vrt_index == -1:
                    return name[:hrz_index]
                else:
                    if hrz_index < vrt_index:
                        return name[:hrz_index + 1]
                    else:
                        pos = min(hrz_index, vrt_index)
                        return name[:pos + 1]
        else:
            bck_index += 2
            hrz_index = name.find(' - ')
            res = ""
            if hrz_index == -1:
                vrt_index = name.find(' | ')
                if vrt_index == -1:
                    return name[bck_index:]
                else:
                    return name[bck_index:(vrt_index + 1)]
            else:
                vrt_index = name.find(' | ')
                if vrt_index == -1:
                    return name[bck_index:(hrz_index + 1)]
                else:
                    if hrz_index < vrt_index:
                        return name[bck_index:(hrz_index + 1)]
                    else:
                        pos = min(hrz_index, vrt_index)
                        return name[bck_index:(pos + 1)]

    else:
        hrz_index = name.find(' - ')
        if hrz_index == -1:
            vrt_index = name.find(' | ')
            if vrt_index == -1:
                res = name[index:]
            else:
                res = name[index:(vrt_index + 1)]
        else:
            vrt_index = name.find(' | ')
            if vrt_index == -1:
                res = name[index:(hrz_index + 1)]
            else:
                if hrz_index < vrt_index:
                    res = name[index:(hrz_index + 1)]
                else:
                    pos = min(hrz_index, vrt_index)
                    res = name[index:(pos + 1)]
        old_index = res.lower().find('cũ')
        if old_index == -1:
            return res[7:]
        else:
            return res[10:]

def handle_brand(name):
    space_index = name.find(' ')
    if space_index == -1:
        return ""
    else:
        return name[:space_index]

def handle_price(price):
    cleaned_price = price.replace('.', '')
    cleaned_price = cleaned_price[:-2]
    if cleaned_price.find("Liên") != -1:
        return None
    else:
        return int(cleaned_price)

def handle_status(name):
    old_index = name.lower().find('cũ')
    if old_index != -1:
        return "old"
    else:
        open_index = name.find('[')
        close_index = name.find(']')
        return name[(open_index + 1): close_index]

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

def handle_type_cpu(cpu):
    first_space = cpu.find(' ')
    tmp_cpu = cpu[first_space + 1:]
    second_space = tmp_cpu.find(' ')
    return tmp_cpu[:second_space]

def is_last_char_z(string):
    return string[-1].lower() == 'z' if string else False

def handle_ram(ram):
    if is_last_char_z(ram):
        bck_fnd = ram.rfind(' ')
        ram = ram[:bck_fnd]
    open_brck = ram.find('(')
    if open_brck != -1:
        ram = ram[:(open_brck - 1)]
    ram_index = ram.rfind('ram')
    ram_capacity = ""
    ram_type = ""
    if ram_index == -1:
        space_bck = ram.rfind(' ')
        GB_index = ram.find('GB')
        tmp_ram = ram[:(GB_index + 2)]
        spc_index = tmp_ram.rfind(' ')
        if spc_index != -1:
            ram_capacity =  tmp_ram[spc_index + 1:]
        if space_bck != -1:
            ram_type = ram[space_bck + 1:]
        if ram_type.find("GB") != -1:
            ram_type = ""
        return ram_capacity, ram_type
    else:
        ram_tmp = ram[(ram_index + 5):]
        spc_index = ram_tmp.find(' ')
        if spc_index != -1:
            ram_capacity = ram_tmp[:spc_index]
        space_bck = ram.rfind(' ')
        if space_bck != -1:
            ram_type = ram[space_bck + 1:]
        if ram_type.find("GB") != -1:
            ram_type = ""
        return ram_capacity, ram_type

def handle_hard_drive(hard_drive):
    hard_drive_type = hard_drive[:3]
    tmp_hard_drive = hard_drive[4:]
    spc_index = tmp_hard_drive.find(' ')
    # print("Space Index: ", spc_index)
    if spc_index == -1:
        return hard_drive_type, ""
    else:
        hard_drive_capacity = tmp_hard_drive[:spc_index]
    return hard_drive_type, hard_drive_capacity

def handle_card_brand(card):
    spc_index = card.find(' ')
    if spc_index == -1:
        return card
    else:
        return card[:spc_index]

def handle_screen(screen):
    inch_index = screen.find('nch')
    screen_size = ""
    screen_type = ""
    if inch_index != -1:
        screen_size = screen[:inch_index - 2]
    if screen.find("FHD") != -1 or screen.find("Full HD") != -1:
        screen_type = "FHD"
    else:
        if screen.find("2560") != -1:
            screen_type = "2.5K"
        else:
            K_index = screen.find('K')
            if K_index != -1:
                screen_tmp = screen[:(K_index + 1)]
                print("Temp Screen: ", screen_tmp)
                bck_spc = screen_tmp.rfind(' ')
                if bck_spc != -1:
                    screen_type = screen_tmp[(bck_spc + 1):]
                else:
                    screen_type = screen_tmp
    return screen_size, screen_type

async def main():
    f = open("laptop88.csv", "w", newline="", encoding="utf-8")
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

            for j in range(1, 25):
                link_selector = f'{base_link}{j}) > div.product-img > a'
                image_selector = f'{base_link}{j}) > div.product-img > a > img'  # Adjusted to correctly select the <img> tag
                price_link = f'{base_link}{j}) > div.product-info > div.product-price > div.price-bottom > span'
                #print(f"Link Selector: {link_selector}")
                #print(f"Image Selector: {image_selector}")
                #print(f"Price Selector: {price_link}")

                # Get the product link
                try:
                    product_element = html.select_one(link_selector)
                    selected_link = product_element.get('href') if product_element else None
                    # print("Product element: ", selected_link)
                except Exception as e:
                    print(f"Error getting link for item {j}: {e}")
                    selected_link = None

                # Get the image link
                try:
                    image_element = html.select_one(image_selector)
                    ss = image_element.get('src')
                    # print("Image element: ", ss)
                    image_link = image_element.get('src') if image_element else ""
                except Exception as e:
                    print(f"Error getting image for item {j}: {e}")
                    image_link = ""

                if image_link:
                    absolute_image_link = urljoin(url, image_link)
                    # print(f"Absolute Image Link: {absolute_image_link}")

                if selected_link:
                    absolute_link = urljoin(url, selected_link)
                    # print(f"Absolute Link: {absolute_link}")

                    # Fetch product page
                    access_link = await fetch_page(client, absolute_link)
                    if access_link is None:
                        continue

                    soup = BeautifulSoup(access_link, 'html.parser')

                    try:
                        product_name_tmp = soup.select_one('h2.name-product').text
                        #print(f"Product Name: {product_name_tmp}")
                    except Exception as e:
                        print(f"Error getting product name: {e}")
                        product_name_tmp = ""

                    product_name = handle_name(product_name_tmp)
                    print("Product Name: ", product_name)
                    brand = handle_brand(product_name)
                    #print("Brand: ", brand)
                    # print("Price link: ", price_link)
                    try:
                        price_tmp = html.select_one(price_link).text
                        #print(price)
                    except Exception as e:
                        price_tmp = ""
                    price = handle_price(price_tmp)
                    # print(price)

                    status = handle_status(product_name_tmp)
                    # print("Status: ", status)
                    if status != "old":
                        old = 0
                        new = 1
                    else:
                        new = 0
                        old = 1

                    tr_element = soup.find('tr', {'data-key': 'cpu'})
                    if tr_element:
                        text_content = tr_element.get_text(separator=" ").strip()
                        cpu = text_content.replace('®', '').replace('™', '')
                        # print(cpu)
                        cpu_type = handle_type_cpu(cpu)
                    else:
                        cpu = ""
                        cpu_type = ""
                    # print(cpu_type)
                    tr_element = soup.find('tr', {'data-key': 'ram'})
                    if tr_element:
                        ram = tr_element.get_text(separator=" ").strip()
                        ram = ram.replace("(*)", "")
                    else:
                        ram = ""

                    print("Ram: ", ram)
                    ram_capacity, ram_type = handle_ram(ram)
                    print("Ram capacity: ", ram_capacity)
                    print("Ram type: ", ram_type)

                    tr_element = soup.find('tr', {'data-key': 'o-cung'})
                    if tr_element:
                        hard_drive = tr_element.get_text(separator=" ").strip()
                        hard_drive = hard_drive[7:]
                        print(hard_drive)
                    else:
                        hard_drive = ""
                    hard_drive_type, hard_drive_capacity = handle_hard_drive(hard_drive)
                    # print(hard_drive)
                    # print("Type of Hard Drive: ", hard_drive_type)
                    # print("Capacity of Hard Drive: ", hard_drive_capacity)

                    tr_element = soup.find('tr', {'data-key': 'card-do-hoa'})
                    if tr_element:
                        card = tr_element.get_text(separator=" ").strip()
                        card = card.replace('®', '').replace('™', '')
                        card = card[12:]
                        # print(card)
                    else:
                        card = ""
                    card_brand = handle_card_brand(card)
                    # print("Card: ", card)
                    # print("Card Brand: ", card_brand)

                    tr_element = soup.find('tr', {'data-key': 'man-hinh'})
                    if tr_element:
                        screen = tr_element.get_text(separator=" ").strip()
                        screen = screen[9:]
                    else:
                        screen = ""

                    screen_size, screen_type = handle_screen(screen)
                    statistics =  ["laptop88", product_name, brand, absolute_link, absolute_image_link, price, old, new, cpu, cpu_type, ram_capacity, ram_type, hard_drive_type, hard_drive_capacity, card, card_brand, screen_size, screen_type]
                    writer.writerow(statistics)

                    # print("Screen: ", screen)
                    # print("Screen Size: ", screen_size)
                    # print("Screen Type: ", screen_type)

                    # Further processing can be done here
                else:
                    print(f"No valid link found for item {j}.")
                    break
    f.close()
# Run the main function
asyncio.run(main())
