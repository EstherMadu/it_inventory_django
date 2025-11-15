from django.db import models
from django.contrib.auth.models import User

class AssetStatus(models.TextChoices):
    INVENTORY = "inventory", "Inventory"
    ASSIGNED = "assigned", "Assigned"
    REPAIR = "repair", "Repair"
    RETIRED = "retired", "Retired"




class Profile(models.Model):
    class UserTypeEnums(models.TextChoices):
        ADMIN = "admin", "Admin"
        Vendor = "vendor", "Vendor"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=150, default=UserTypeEnums.ADMIN.value, choices=UserTypeEnums)
    email = models.EmailField()
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email

class AssetCategory(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=140)
    serial_number = models.CharField(max_length=140, unique=True)
    model_number = models.CharField(max_length=140, blank=True, null=True)
    make = models.CharField(max_length=140, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    picture = models.ImageField(upload_to='asset_images/', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="assets")
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, related_name="assets")
    current_status = models.CharField(max_length=20, choices=AssetStatus.choices, default=AssetStatus.INVENTORY)
    current_holder = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.CharField(max_length=128)
    assigned_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(blank=True, null=True)

class AssetStatusHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=AssetStatus.choices)
    changed_by = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=256, blank=True, null=True)

class Admin(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
