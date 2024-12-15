from django import forms

class LaptopPredictionForm(forms.Form):
    """ brand, cpu, cpu_brand, ram_capacity, ram_brand, hard_drive_type, hard_drive_capacity, card,
    card_brand, screen_size, screen_type """
    BRAND_CHOICES = [
        ('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')
    ]
    AGE_CHOICES = [('Old', 'Old'), ('New', 'New')]
    CPU_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    CPU_BRAND_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    RAM_CAPACITY_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    RAM_BRAND_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    HARD_DRIVE_TYPE_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    HARD_DRIVE_CAPACITY_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    CARD_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    CARD_BRAND_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]
    SCREEN_TYPE_CHOICES = [('Dell', 'Dell'), ('HP', 'HP'), ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'), ('Asus', 'Asus'), ('Acer', 'Acer')]

    brand = forms.ChoiceField(choices=BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    age = forms.ChoiceField(choices=AGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    cpu = forms.ChoiceField(choices=CPU_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    cpu_brand = forms.ChoiceField(choices=CPU_BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    ram_capacity = forms.ChoiceField(choices=RAM_CAPACITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    ram_brand = forms.ChoiceField(choices=RAM_BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    hard_drive_type = forms.ChoiceField(choices=HARD_DRIVE_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    hard_drive_capacity = forms.ChoiceField(choices=HARD_DRIVE_CAPACITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    card = forms.ChoiceField(choices=CARD_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    card_brand = forms.ChoiceField(choices=CARD_BRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
    screen_size = forms.DecimalField(
    widget=forms.NumberInput(attrs={'class': 'form-control form-number-input', 'min': '0', 'step': '0.1'}),
    decimal_places=2,
    required=False )
    screen_type = forms.ChoiceField(choices=SCREEN_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control select2'}))
