    for i in range(1, 789):
        try:
            elm = "#layout-desktop > div.cps-container.cps-body > div.cps-category > div > div.block-filter-sort > div.filter-sort__list-product > div > div.product-list-filter.is-flex.is-flex-wrap-wrap > div:nth-child(" + str(i) + ") > div.product-info > a"
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