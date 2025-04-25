from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        VENDOR = 'VENDOR', _('Vendor')
        CUSTOMER = 'CUSTOMER', _('Customer')
        
    role = models.CharField(_('Role'),
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    
    # Add any extra fields as needed
    phone_number = models.CharField(_('Phone Number'),max_length=15, blank=True, null=True)
    address = models.TextField(_('Adress'), blank=True, null=True)
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    
    def is_vendor(self):
        return self.role == self.Role.VENDOR
        
    def is_customer(self):
        return self.role == self.Role.CUSTOMER