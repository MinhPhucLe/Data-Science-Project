def predict_laptop_price(form_data):
    brand = form_data.get('brand')
    processor = form_data.get('processor')
    ram_size = form_data.get('ram_size')
    storage_type = form_data.get('storage_type')

    if brand == 'Dell' and processor == 'i7' and ram_size == '16':
        print("HELLO")
        return "1000 USD"
    elif brand == 'HP' and processor == 'i5' and ram_size == '8':
        return "700 USD"
    else:
        return "500 USD"
