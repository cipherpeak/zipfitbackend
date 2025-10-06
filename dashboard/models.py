from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from windows.models import CustomerEnquiry

class EmployeeManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('admin_type', 'superuser')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, phone, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    ADMIN_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    admin_type = models.CharField(max_length=10, choices=ADMIN_TYPE_CHOICES, default='admin')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = EmployeeManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    




class ProductionApproval(models.Model):
    customer_enquiry = models.ForeignKey(CustomerEnquiry, on_delete=models.CASCADE)
    actual_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Approval for {self.customer_enquiry.customer_name}"

    class Meta:
        unique_together = ('customer_enquiry',) 