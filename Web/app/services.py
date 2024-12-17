import numpy as np
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import lightgbm as lgb

def load_models():
    try:
        # Use absolute paths or ensure correct encoding
        catboost_model = CatBoostRegressor()
        catboost_model.load_model(r"../model/catboost_model.cbm")

        # For XGBoost, convert to a NumPy array and ensure proper encoding
        xgboost_model = XGBRegressor()
        xgboost_model.load_model(r"../model/xgboost_model.json")

        lightgbm_model = lgb.Booster(model_file=r"../model/lightgbm_model.txt")

        return catboost_model, xgboost_model, lightgbm_model
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None, None


# Load models globally
catboost_model, xgboost_model, lightgbm_model = load_models()

def predict_laptop_price(form_data):
    age_value = form_data.get('age')
    if age_value == "Old":
        old = 1
        new = 0
    elif age_value == "New":
        old = 0
        new = 1
    else:
        old = ''
        new = ''

    input_data = [
        form_data.get('brand') or '',
        old,
        new,
        form_data.get('cpu') or '',
        form_data.get('cpu_brand') or '',
        form_data.get('ram_capacity') or '',
        form_data.get('ram_brand') or '',
        form_data.get('hard_drive_type') or '',
        form_data.get('hard_drive_capacity') or '',
        form_data.get('card') or '',
        form_data.get('card_brand') or '',
        str(form_data.get('screen_size')) or '',
        form_data.get('screen_type') or ''
    ]

    input_data = ['' if x == 'None' else str(x) for x in input_data]

    processed_data = [0 if x == '' else float(x) for x in input_data]

    print("Cat boost input")
    print(input_data)
    print("XGB and LGBM input")
    print(processed_data)

    predictions = [
        catboost_model.predict([input_data])[0],
        xgboost_model.predict([processed_data])[0],
        lightgbm_model.predict([processed_data])[0]
    ]

    print(predictions)

    return f"{round(np.mean(predictions),3)}VND"

