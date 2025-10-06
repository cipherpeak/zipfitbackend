from django.db import models

# Create your models here.

class PuffingPriceOption(models.Model):
    price = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.price
    
class SurfaceTreatment(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    

class WoodLaminationType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True,null=True,blank=True)
    surface_treatment = models.ForeignKey('SurfaceTreatment',on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})" 


class PowderCoatingType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True,null=True,blank=True)
    surface_treatment = models.ForeignKey('SurfaceTreatment',on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class PowderCoatingColor(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True,null=True,blank=True)
    hex_value = models.CharField(max_length=7,null=True,blank=True)
    surface_treatment = models.ForeignKey('SurfaceTreatment',on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class WindowSeries(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True,null=True,blank=True)
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class WindowHeight(models.Model):
    name = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
class WindowWidth(models.Model):
    name = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"    
   

class FittingPriceOption(models.Model):
    price = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.price}"
    


class Finish(models.Model):
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"
    



class Infill(models.Model):
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"
    



class Hardware(models.Model):
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"
    



class Lock(models.Model):
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"



class Other(models.Model):
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"





class WindowType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True,null=True,blank=True)
    icon = models.CharField(max_length=10, null=True,blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WindowConfiguration(models.Model):
    width = models.ForeignKey('WindowWidth',on_delete=models.SET_NULL,null=True,blank=True)
    height = models.ForeignKey('WindowHeight',on_delete=models.SET_NULL,null=True,blank=True)
    window_type = models.ForeignKey('WindowType', on_delete=models.SET_NULL,null=True,blank=True)
    window_series = models.ForeignKey('WindowSeries', on_delete=models.SET_NULL,null=True,blank=True)

    image = models.ImageField(
        upload_to='window_configurations/',  
        null=True, 
        blank=True,
        help_text="Upload an image of this window configuration"
    )
    rate_per_Sq_Feet = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
   
    def __str__(self):
        return f"Config #{self.id} - {self.window_type}"
    



class CustomerEnquiry(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved for Production'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    approximate_amount = models.CharField(max_length=20,null=True, blank=True)
    customer_address = models.TextField()    
    window_model = models.ForeignKey('WindowConfiguration',on_delete=models.SET_NULL,null=True,blank=True)
    surface_treatment = models.ForeignKey('SurfaceTreatment', on_delete=models.SET_NULL, null=True, blank=True)
    wood_lamination_types = models.ManyToManyField('WoodLaminationType', blank=True,null=True)
    powder_coating_type = models.ForeignKey('PowderCoatingType', on_delete=models.SET_NULL, null=True, blank=True)
    powder_coating_color = models.ForeignKey('PowderCoatingColor', on_delete=models.SET_NULL, null=True, blank=True)
    mosquito_net_needed = models.BooleanField(default=False)
    has_mosquito_net = models.ForeignKey('WindowWidth', on_delete=models.SET_NULL, null=True, blank=True)
    fitting_price = models.ForeignKey('FittingPriceOption', on_delete=models.SET_NULL, null=True, blank=True)
    puffing_price = models.ForeignKey('PuffingPriceOption', on_delete=models.SET_NULL, null=True, blank=True)

    finish = models.ForeignKey('Finish',on_delete=models.SET_NULL,null=True,blank=True)
    infill = models.ForeignKey('Infill',on_delete=models.SET_NULL,null=True,blank=True)
    hardware = models.ForeignKey('Hardware',on_delete=models.SET_NULL,null=True,blank=True)
    lock = models.ForeignKey('Lock',on_delete=models.SET_NULL,null=True,blank=True)
    other = models.ForeignKey('Other',on_delete=models.SET_NULL,null=True,blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config #{self.customer_name} - {self.window_model}"
    
    
    class Meta:
        ordering = ['-created_at']






