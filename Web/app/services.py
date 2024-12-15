def predict_laptop_price(form_data):
    brand = form_data.get('brand') or ""
    age = form_data.get('age') or ""
    cpu = form_data.get('cpu') or ""
    cpu_brand = form_data.get('cpu_brand') or ""
    ram_capacity = form_data.get('ram_capacity') or ""
    ram_brand = form_data.get('ram_brand') or ""
    hard_drive_type = form_data.get('hard_drive_type') or ""
    hard_drive_capacity = form_data.get('hard_drive_capacity') or ""
    card = form_data.get('card') or ""
    card_brand = form_data.get('card_brand') or ""
    screen_size = form_data.get('screen_size') or ""
    screen_type = form_data.get('screen_type') or ""

    result = " VND"
    if brand == 'Dell':
        result = "1000" + result
    elif brand == 'HP':
        result = "700" + result
    else:
        result = "500" + result

    return result
