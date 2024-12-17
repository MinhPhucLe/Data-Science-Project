from django import forms
from sklearn.preprocessing import LabelEncoder
from app.models import Laptop

fields_to_check = [
    "brand", "cpu", "cpu_brand", "ram_capacity", "ram_brand",
    "hard_drive_type", "hard_drive_capacity", "card", "card_brand",
    "screen_size", "screen_type"
]

# Function to get unique values and their encoded labels
def get_unique_values_with_encoding():
    unique_values_with_encoding = {}

    for field in fields_to_check:
        # Exclude null and blank values and retrieve distinct values
        values = (
            Laptop.objects.exclude(**{f"{field}__isnull": True})
            .exclude(**{f"{field}": ""})
            .values_list(field, flat=True)
            .distinct()
        )

        encoded_values = values

        if field in ["brand", "cpu", "cpu_brand", "ram_brand", "hard_drive_type", "card", "card_brand", "screen_type"]:
            # Apply Label Encoding
            label_encoder = LabelEncoder()
            encoded_values = label_encoder.fit_transform(list(values))

        # Store the original value along with its encoded value
        unique_values_with_encoding[field] = list(zip(encoded_values, values))

        if field in ["ram_capacity", "hard_drive_capacity"]:
            unique_values_with_encoding[field] = sorted(
                zip(encoded_values, values), key=lambda x: float(x[1])
            )

    return unique_values_with_encoding

class LaptopPredictionForm(forms.Form):
    # Fetch unique values
    unique_values = get_unique_values_with_encoding()

    BRAND_CHOICES = unique_values["brand"]
    AGE_CHOICES = [('Old', 'Old'), ('New', 'New')]
    CPU_CHOICES = unique_values["cpu"]
    CPU_BRAND_CHOICES = unique_values["cpu_brand"]
    RAM_CAPACITY_CHOICES = unique_values["ram_capacity"]
    RAM_BRAND_CHOICES = unique_values["ram_brand"]
    HARD_DRIVE_TYPE_CHOICES = unique_values["hard_drive_type"]
    HARD_DRIVE_CAPACITY_CHOICES = unique_values["hard_drive_capacity"]
    CARD_CHOICES = unique_values["card"]
    CARD_BRAND_CHOICES = unique_values["card_brand"]
    SCREEN_TYPE_CHOICES = unique_values["screen_type"]

    brand = forms.ChoiceField(choices=BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    age = forms.ChoiceField(choices=AGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    cpu_brand = forms.ChoiceField(choices=CPU_BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    cpu = forms.ChoiceField(choices=CPU_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    ram_capacity = forms.ChoiceField(choices=RAM_CAPACITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    ram_brand = forms.ChoiceField(choices=RAM_BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    hard_drive_type = forms.ChoiceField(choices=HARD_DRIVE_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    hard_drive_capacity = forms.ChoiceField(choices=HARD_DRIVE_CAPACITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    card_brand = forms.ChoiceField(choices=CARD_BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    card = forms.ChoiceField(choices=CARD_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    screen_size = forms.DecimalField(
    widget=forms.NumberInput(attrs={'class': 'form-control form-number-input', 'min': '0', 'step': '0.1'}),
    decimal_places=2,
    required=False )
    screen_type = forms.ChoiceField(choices=SCREEN_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
