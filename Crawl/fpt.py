from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

urls = []

def handle_brand(ss):
    if ss == "":
        return ss
    space = ss.find(" ")
    if space == -1:
        return ss
    else:
        return ss[:space]

def handle_price(price):
    price = price.replace("₫", "")
    price = price.replace(".", "")
    return int(price)

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.get("https://fptshop.com.vn/may-tinh-xach-tay")

    # Wait for main layout to load
    try:
        WebDriverWait(browser, 20).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )
        print("Main layout loaded.")
    except TimeoutException:
        print("Main layout not loaded in time.")
        browser.quit()

    # Loop to click 'See More' button
    for _ in range(1):
        try:
            # Adjust the XPath based on page structure
            see_more_button = WebDriverWait(browser, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div[6]/div[2]/div[3]/div[3]/button"))
            )

            # Scroll into view and click the button
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", see_more_button)
            time.sleep(1)  # Small delay to ensure element visibility
            see_more_button.click()
            time.sleep(3)  # Wait for new content to load
            print("Clicked 'See More' button")

        except StaleElementReferenceException:
            print("Stale element reference. Retrying...")
            continue
        except Exception as e:
            print("Error clicking 'See More' button:", e)
            break

    # Loop to collect product URLs
    for i in range(1, 5):
        try:
            xpath_ele = "/html/body/main/div/div[6]/div[2]/div[3]/div[2]/div[" + str(i) + "]/div/div[1]/a"
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_ele))
            )
            href = element.get_attribute("href")
            urls.append(href)
            print(f"The href attribute is: {href} with order of: {i}")

        except Exception as e:
            print(f"This product could not be located at index {i}. Error: {e}")
            continue

    print(f"Collected {len(urls)} URLs")
    browser.quit()

    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            attempt += 1
            try:
                # Initialize the WebDriver
                browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

                # Try to access the page
                print(f"Attempt {attempt}: Accessing the page...")
                browser.get(url)
                WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "main"))
                )
                try:
                    image = browser.find_element(By.XPATH,
                                                 "/html/body/main/div[1]/section[2]/div[1]/div[1]/div/div[1]/div[1]/div[1]/div/div/div/div/img").get_attribute(
                        "src")
                except Exception as e:
                    image = ""
                    print("Error extracting image:", e)

                print("Image URL:", image)

                try:
                    h1_element = browser.find_element(By.CSS_SELECTOR,
                                                      "body > main > div.container > section.flex.justify-between.py-6 > div.w-\\[507px\\] > div.grid.gap-y-2.pb-2.pt-4.pc\\:gap-y-1.pc\\:pb-0.pc\\:pt-0 > h1")
                    name = browser.execute_script("""
                        var h1 = arguments[0];
                        var span = h1.querySelector('span'); 
                        if (span) {
                            var textBeforeSpan = h1.textContent.split(span.textContent)[0];  // Get text before the <span>
                            return textBeforeSpan.trim();  // Return the cleaned text
                        }
                        return h1.textContent.trim();  // Return the full text if there's no <span>
                    """, h1_element)
                except Exception as e:
                    name = ""
                    print("Error extracting product name:", e)

                print("Product name:", name)

                if not name:
                    print("Product name is empty. Retrying...")
                    browser.quit()
                    continue

                try:
                    price_tmp = browser.find_element(By.XPATH,
                                                     "/html/body/main/div[1]/section[2]/div[2]/div[3]/div[2]/div[1]/div[1]/span[2]").text
                    price = handle_price(price_tmp)
                except Exception as e:
                    price = ""
                    print("Error extracting price:", e)

                print("Price:", price)

                old = 0
                new = 1
                try:
                    ss = browser.find_elements(By.XPATH,
                                               "/html/body/main/div[1]/section[1]/nav/ol/li[3]").text
                except:
                    ss = ""
                brand = handle_brand(ss)
                print(brand)

                cpu = ""
                card = ""
                ram = ""
                hard_drive = ""
                screen = ""
                for k in range(1, 3):
                    xpath = "/html/body/main/div[" +str(k) + "]/section[2]/div[1]/div[2]/div[1]/button"
                    try:
                        configuration_button = WebDriverWait(browser, 10).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        configuration_button.click()
                        time.sleep(6)

                        # Find the table containing the specifications
                        try:
                            table = browser.find_element(By.CSS_SELECTOR,
                                                         '#drawer-container-body > div.px-5.pb-15.pt-15')
                            print("Table found.")

                            # Find all rows in the table with the class 'tab-content'
                            rows = table.find_elements(By.CLASS_NAME, 'tab-content')
                            print(f"Number of rows found: {len(rows)}")

                            spec_data = {}

                            # Iterate over each row and extract key-value pairs
                            for row in rows:
                                try:
                                    # Use CSS selectors for the key and value to be more specific
                                    key_element = row.find_element(By.CSS_SELECTOR,
                                                                   ".w-2\\/5.text-textOnWhiteSecondary.b2-regular")
                                    value_element = row.find_element(By.CSS_SELECTOR,
                                                                     ".flex-1.text-textOnWhitePrimary.b2-regular")

                                    key = key_element.text.strip()
                                    value = value_element.text.strip()

                                    print(f"Extracted key: {key}, value: {value}")

                                    # Add key-value pair to the dictionary
                                    spec_data[key] = value
                                except Exception as e:
                                    print("Error extracting key-value pair:", e)
                                    continue

                            print("Extracted Specifications:", spec_data)

                        except Exception as e:
                            print("Error locating table or rows:", e)
                        break
                    except:
                        print("Lack of specific information")
                        continue

                browser.quit()
                break

            except Exception as e:
                print(f"Attempt {attempt} failed with error: {e}")
                if attempt >= max_retries:
                    print("Max retries reached, breaking out of the loop.")
                    break
                else:
                    print(f"Retrying... ({attempt}/{max_retries})")
                    browser.quit()
                    time.sleep(3)
