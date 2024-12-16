from django.db import models

class Laptop(models.Model):
    brand = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    old = models.IntegerField(null=True, blank=True)
    new = models.IntegerField(null=True, blank=True)
    cpu = models.CharField(max_length=100, null=True, blank=True)
    cpu_brand = models.CharField(max_length=50, null=True, blank=True)
    ram_capacity = models.CharField(max_length=50, null=True, blank=True)
    ram_brand = models.CharField(max_length=50, null=True, blank=True)
    hard_drive_type = models.CharField(max_length=50, null=True, blank=True)
    hard_drive_capacity = models.CharField(max_length=50, null=True, blank=True)
    card = models.CharField(max_length=100, null=True, blank=True)
    card_brand = models.CharField(max_length=50, null=True, blank=True)
    screen_size = models.CharField(max_length=100, null=True, blank=True)
    screen_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'laptops'
