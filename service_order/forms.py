from django import forms
from .models import ServiceOrder, ServiceOrderConsumption
from assets.models import Asset
from django.core.validators import MaxLengthValidator,MinLengthValidator,RegexValidator,ProhibitNullCharactersValidator,MaxValueValidator,MinValueValidator,validate_image_file_extension,FileExtensionValidator
from django.core.exceptions import ValidationError

from inventory.models import Inventory

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
    
def imagesTotalSize_validator(image):
    imageSize = round(image.size/1024,2)
    if imageSize > 200:
        raise ValidationError('Actualmente tienes imagenes adjuntas que superan el peso limite(200KB por imagen) por favor verificar.')
    return image

def FileImagesChecking(files):
    #Check total images attach to the request
    if len(files) > 3:
        raise ValidationError('El maximo de archivos adjuntos ha sido superado(3 imagenes por solicitud), por favor verificar e intentarlo nuevamente.')
    
    #Check totalSize from the fileinput
    inputSize = sum(round(i.size/1024,2) for i in files)#generator comprehension
    if inputSize > 600:
        raise ValidationError('Los archivos adjuntos superan el peso recomendado(600KB), por favor verificar e intentarlo nuevamente.')
    
    return files
    
    
class serviceOrders_MainForm(forms.ModelForm):
    
    customer = forms.ModelChoiceField(
        label='Cliente',
        required=True,
        queryset=Asset.objects.filter(status=1,type=1),
        empty_label='-- Selecciona --',
        widget=forms.Select(attrs={
            'class':'form-control'
        })
    )    
    
    serial = forms.CharField(
        label='Serial', 
        max_length=100, 
        required=True,
        help_text='Numero de serie del equipo.',
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(4),
            MaxLengthValidator(50),
            ProhibitNullCharactersValidator,
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    model = forms.CharField(
        label='Modelo', 
        max_length=100, 
        required=True,
        help_text='Modelo relacionado al equipo.',
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(4),
            MaxLengthValidator(50),
            ProhibitNullCharactersValidator,
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    registry_comments = forms.CharField(
        label='Observaciones iniciales', 
        max_length=300, 
        required=False, 
        help_text='Información relevante al momento de recibir el equipo.',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
                'style':'max-width:500px;'
            }
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='Este campo contiene caracteres invalidos.'),
        ]
    )
    
    class Meta():
        model = ServiceOrder
        fields = ['customer','serial','model','registry_comments']
    
class ServiceOrderFilterForm(forms.Form):
    
    customer = forms.ModelChoiceField(
        label='Cliente',
        required=False,
        queryset=Asset.objects.filter(status=1,type=1),
        help_text='filter_option',
        empty_label='-- Cliente --',
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    serial = forms.CharField(
        max_length=100, 
        required=False,
        strip=True,
        help_text='filter_option',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Serial',
        }),
        validators=[
            MaxLengthValidator(100),
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    model = forms.CharField(
        max_length=100, 
        required=False,
        strip=True,
        help_text='filter_option',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Modelo',
        }),
        validators=[
            MaxLengthValidator(100),
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )    
      
class serviceOrders_DiagnoseForm(forms.ModelForm):
    diagnose_comments = forms.CharField(
        label='Observaciones', 
        max_length=300, 
        required=True, 
        help_text='Información relevante al momento del diagnostico.',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
                'style':'max-width:500px;'
            }
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='Este campo contiene caracteres invalidos.'),
        ]
    )
    
    images = MultipleFileField(
        label='Archivos adjuntos',
        required=False,
        help_text='Evidencias relacionas al diagnostico (Peso maximo 500KB - 3 imagenes)',
        widget=MultipleFileInput(
            attrs={
                'class':'form-control'
            }
        ),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpeg','jpg','png'],message='Invalid file extension, valid file extensions are .jpeg .jpg .pgn'),
            imagesTotalSize_validator
        ]
    )
        
    class Meta():
        model = ServiceOrder
        fields = ['diagnose_comments']
    
    def clean_images(self):
        files = self.cleaned_data.get('images')
        return FileImagesChecking(files)    
    
class serviceOrders_RepairForm(forms.ModelForm):
    repair_comments = forms.CharField(
        label='Observaciones', 
        max_length=300, 
        required=True, 
        help_text='Información relevante al momento de la reparación.',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
                'style':'max-width:500px;'
            }
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='Este campo contiene caracteres invalidos.'),
        ]
    )
    
    images = MultipleFileField(
        label='Archivos adjuntos',
        required=False,
        help_text='Evidencias relacionas a la reparación (Peso maximo 500KB - 3 imagenes)',
        widget=MultipleFileInput(
            attrs={
                'class':'form-control'
            }
        ),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpeg','jpg','png'],message='Invalid file extension, valid file extensions are .jpeg .jpg .pgn'),
            imagesTotalSize_validator
        ]
    )
        
    class Meta():
        model = ServiceOrder
        fields = ['repair_comments']
    
    def clean_images(self):
        files = self.cleaned_data.get('images')
        return FileImagesChecking(files)
    
class serviceOrders_CancelForm(forms.ModelForm):
    cancel_comments = forms.CharField(
        label='Motivo de cancelación', 
        max_length=300, 
        required=True, 
        help_text='Información relevante al momento de la cancelación.',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
                'style':'max-width:500px;'
            }
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='Este campo contiene caracteres invalidos.'),
        ]
    )
        
    class Meta():
        model = ServiceOrder
        fields = ['cancel_comments']
    
class ServiceOrderConsumptionFilterForm(forms.Form):
    inventory_code = forms.ModelChoiceField(
        label='Codigo de inventario',
        required=False,
        queryset=Inventory.objects.filter(status=1),
        help_text='filter_option',
        empty_label='-- Código de inventario --',
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 -()]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
class ServiceOrderConsumption_MainForm(forms.ModelForm):
    inventory_code = forms.ModelChoiceField(
        label='Código de inventario',
        required=True,
        queryset=Inventory.objects.filter(status=1,available_quantity__gt=0),
        help_text='Directamente desde las existencias actuales.',
        empty_label='-- Selecciona un código --',
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 -()]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    quantity = forms.IntegerField(
        label='Cantidad consumida',
        required=True,
        help_text='Relacionada a la orden de servicio.',
        widget=forms.NumberInput(attrs={
            'class':'form-control'
        }),
        min_value=1,
        max_value=999,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999),
            RegexValidator(regex='^[0-9 .]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
        
    class Meta():
        model = ServiceOrderConsumption
        fields = ['inventory_code','quantity']
            
    def clean_inventory_code(self):
        code = self.cleaned_data.get('inventory_code')
        id = self.instance.id if self.instance else None
        if ServiceOrderConsumption.objects.filter(inventory_code=code).exclude(id=id).exists():
            raise ValidationError('El código que estas intentado ingresar ya existe en el panel de consumo, Por favor verificarlo e intentalo nuevamente.')
        return code

    def clean_quantity(self):
        quantity2consume = self.cleaned_data.get('quantity')
        inventory_code = self.cleaned_data.get('inventory_code')
        if inventory_code is None:
            return quantity2consume

        if quantity2consume > inventory_code.available_quantity:
            available_quantity = Inventory.objects.get(id=inventory_code.id).available_quantity
            raise ValidationError(f'La cantidad a consumir supera la disponibilidad actual de tus existencias({available_quantity}).')
        return quantity2consume
    
class serviceOrders_ServiceConfigForm(forms.ModelForm):
    services_total = forms.FloatField(
        label='Total del servicio', 
        required=True,
        min_value=1000,
        max_value=1000000000,
        widget=forms.NumberInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000000),
            RegexValidator(regex='^[0-9 .]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    services_description = forms.CharField(
        label='Observaciones del servicio', 
        max_length=500, 
        required=True, 
        help_text='Breve descripción de los servicios dados en la orden.',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
                'style':'max-width:500px;'
            }
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(500),
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='Este campo contiene caracteres invalidos.'),
        ]
    )
        
    class Meta():
        model = ServiceOrder
        fields = ['services_total','services_description']