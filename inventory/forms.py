from django import forms
from .models import Inventory, InventoryCodes, InventoryMovement, MovementsTypes, InventoryCategory
from assets.models import Asset
from django.core.validators import MaxLengthValidator,MinLengthValidator,RegexValidator,ProhibitNullCharactersValidator,MaxValueValidator,MinValueValidator,FileExtensionValidator
from django.core.exceptions import ValidationError

def imagesTotalSize_validator(image):
    imageSize = round(image.size/1024,2)
    if imageSize > 400:
        raise ValidationError('La imagen adjunta supera el limite de peso permitido(400KB) por favor verificar.')
    return image

class InventoryCodeMainForm(forms.ModelForm):
    code = forms.CharField(
        label='Código', 
        max_length=100, 
        required=True,
        help_text='Identificador en el inventario.',
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
    
    name = forms.CharField(
        label='Nombre', 
        max_length=100, 
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(100),
            ProhibitNullCharactersValidator,
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    category = forms.ModelChoiceField(
        label='Categoría',
        required=True,
        queryset=InventoryCategory.objects.filter(status=1),
        empty_label='-- Selecciona --',
        widget=forms.Select(attrs={
            'class':'form-control'
        })
    )
      
    supplier = forms.ModelChoiceField(
        label='Proveedor',
        required=True,
        queryset=Asset.objects.filter(status=1,type=2),
        empty_label='-- Selecciona --',
        widget=forms.Select(attrs={
            'class':'form-control'
        })
    )
    
    inbound_price = forms.FloatField(
        label='Precio compra', 
        required=True,
        min_value=0,
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
    
    outbound_price = forms.FloatField(
        label='Precio venta', 
        required=True,
        min_value=0,
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
    
    related_image = forms.ImageField(
        label='Imagen de referencia', 
        required=True,
        help_text='Imagen de referencia para tus productos.',
        widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        ),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpeg','jpg','png'],message='Invalid file extension, valid file extensions are .jpeg .jpg .pgn'),
            imagesTotalSize_validator
        ]
    )
    
    extra_info = forms.CharField(
        label='Información adicional', 
        max_length=300, 
        required=False, 
        help_text='Puedes anotar cualquier información relevante.',
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
    
    class Meta:
        model = InventoryCodes
        fields = ['code','name','category','supplier','inbound_price','outbound_price','related_image','extra_info']
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        id = self.instance.id if self.instance else None
        if InventoryCodes.objects.filter(code=code).exclude(id=id).exists():
            raise ValidationError('El código que estas intentado ingresar ya existe en el listado de códigos, Por favor cambialo e intentalo nuevamente.')
        return code

class InventoryCodeFilterForm(forms.Form):
    code = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=100, 
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Código'
        }),
        validators=[
            MaxLengthValidator(50),
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    name = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=100, 
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Nombre'
        }),
        validators=[
            MaxLengthValidator(100),
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
    
    supplier = forms.ModelChoiceField(
        help_text='filter_option',
        required=False,
        queryset=Asset.objects.filter(status=1,type=2),
        empty_label='-- Proveedor --',
        widget=forms.Select(attrs={
            'class':'form-control',
        })
    )

class InventoryMainForm(forms.ModelForm):
    code = forms.ModelChoiceField(
        label='Código',
        required=True,
        queryset=InventoryCodes.objects.filter(status=1),
        empty_label='-- Selecciona  --',
        widget=forms.Select(attrs={
            'class':'form-control',
        })
    )
    
    extra_info = forms.CharField(
        label='Información adicional', 
        max_length=300, 
        required=False, 
        help_text='Puedes anotar cualquier información relevante.',
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
        model = Inventory
        fields=  ['code','extra_info']
        
    def clean_code(self):
        code = self.cleaned_data.get('code')
        id = self.instance.id if self.instance else None
        if Inventory.objects.filter(code=code).exclude(id=id).exists():
            raise ValidationError('El código que estas intentado ingresar ya existe en el inventario, Por favor verificarlo e intentalo nuevamente.')
        return code
    
class InventoryFilterForm(forms.Form):
    code = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=100, 
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Código'
        }),
        validators=[
            MaxLengthValidator(50),
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )

class InventoryMovement_MainForm(forms.ModelForm):
    quantity = forms.IntegerField(
        label='Cantidad involucrada',
        required=True,
        widget=forms.NumberInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999),
            RegexValidator(regex='^[0-9]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )
        
    description = forms.CharField(
        label='Información adicional', 
        max_length=300, 
        required=False, 
        help_text='Puedes anotar cualquier información relevante al movimiento.',
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
        model = InventoryMovement
        fields=  ['quantity','description']

class InventoryMovement_FilterForm(forms.Form):
    inventory_code=forms.ModelChoiceField(
        help_text='filter_option',
        required=False,
        queryset=Inventory.objects.filter(status=1),
        empty_label='-- Código de inventario  --',
        widget=forms.Select(attrs={
            'class':'form-control',
        })
    )

    type = forms.ChoiceField(
        help_text='filter_option',
        required=False,
        choices=MovementsTypes.choices,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='Esta campo contiene caracteres invalidos.')
        ]
    )