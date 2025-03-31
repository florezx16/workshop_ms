from django.db import models

# Create your models here.
class CoreInformation(models.Model):
    company_name = models.CharField(verbose_name='Nombre', max_length=50)
    company_address = models.CharField(verbose_name='Dirección', max_length=50)
    company_id = models.CharField(verbose_name='NIT', max_length=50)
    company_contact_phone = models.CharField(verbose_name='Teléfonos de contacto', max_length=50)
    company_location = models.TextField(verbose_name='Ubicación', max_length=100)
    company_email = models.EmailField(verbose_name='Correo electrónico', max_length=50)
    company_logo = models.ImageField(verbose_name='Logo', upload_to='CoreInfo/', height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = 'CoreInfo'
        verbose_name_plural = 'CoreInfo'

    def __str__(self):
        return str(self.id)
