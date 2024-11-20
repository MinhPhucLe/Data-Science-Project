from django import forms

class LaptopPredictionForm(forms.Form):
    BRAND_CHOICES = [
        ('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')
    ]
    PROCESSOR_CHOICES = [
        ('i3', 'Intel i3'), ('i5', 'Intel i5'), ('i7', 'Intel i7'),
        ('i9', 'Intel i9'), ('Ryzen 5', 'AMD Ryzen 5'), ('Ryzen 7', 'AMD Ryzen 7')
    ]
    RAM_CHOICES = [(4, '4GB'), (8, '8GB'), (16, '16GB'), (32, '32GB'), (64, '64GB'), (128, '128GB'), (256, '256GB')]
    STORAGE_CHOICES = [
        ('SSD', 'SSD'), ('HDD', 'HDD')
    ]

    brand = forms.ChoiceField(choices=BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    processor = forms.ChoiceField(choices=PROCESSOR_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    ram_size = forms.ChoiceField(choices=RAM_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    storage_type = forms.ChoiceField(choices=STORAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
