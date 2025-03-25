from django import forms
from .models import Asset
from django.core.validators import MinLengthValidator,MaxLengthValidator,ProhibitNullCharactersValidator,RegexValidator,EmailValidator
from django.core.exceptions import ValidationError

class AssetMainForm(forms.ModelForm):
    
    name = forms.CharField(
        label='Nombre', 
        max_length=100, 
        required=True,
        help_text='Nombre completo del Asset',
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            ProhibitNullCharactersValidator,
            RegexValidator(regex='^[a-zA-Z- ]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    type = forms.ChoiceField(
        label='Tipo',
        help_text='Proveedor/Cliente',
        choices=Asset.AssetTypes.choices,
        required=True,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    document_type = forms.ChoiceField(
        label='Tipo de documento',
        help_text='NIT/CC',
        choices=Asset.AssetDocumentTypes.choices,
        required=True,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    document_id = forms.CharField(
        label='Numero de documento', 
        max_length=100, 
        required=True,
        help_text='# de documento',
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            ProhibitNullCharactersValidator,
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    email = forms.EmailField(
        label='Correo electrónico', 
        max_length=200, 
        required=True,
        help_text='Jonh@doe.com',
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            ProhibitNullCharactersValidator,
            EmailValidator()
        ]
    )
    
    phone = forms.CharField(
        label='Teléfono de contacto', 
        max_length=100, 
        required=True,
        help_text='333 333 333',
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control'
        }),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(20),
            ProhibitNullCharactersValidator,
            RegexValidator(regex='^[0-9]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    extra_info = forms.CharField(
        label='Información adicional', 
        max_length=300, 
        required=False, 
        help_text='Puedes anotar cualquier información relevante',
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
            RegexValidator(regex='^[a-zA-Z0-9 ,.\n\r]+$',message='This field contains invalid characters.'),
        ]
    )
    
    class Meta:
        model = Asset
        fields = ['name','type','document_type','document_id','email','phone','extra_info']
    
    def clean_document_id(self):
        document_id = self.cleaned_data.get('document_id')
        id = self.instance.id if self.instance else None
        if Asset.objects.filter(document_id__iexact=document_id).exclude(id=id).exists():
            raise ValidationError('Actualmente ya tienes un Asset registrado con ese numero de documento, por favor validalo e intentalo nuevamente.')
        return document_id

class AssetFilterForm(forms.Form):
    
    document_id = forms.CharField(
        max_length=200, 
        required=False,
        strip=True,
        help_text='filter_option',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Numero del documento(CC/NIT)',
        }),
        validators=[
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    name = forms.CharField(
        max_length=100, 
        required=False,
        strip=True,
        help_text='filter_option',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Nombre completo del Asset'
        }),
        validators=[
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z- ]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )
    
    type = forms.ChoiceField(
        label='Tipo',
        choices=Asset.AssetTypes.choices,
        required=False,
        help_text='filter_option',
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='Esta campo contiene caracteres invalidos')
        ]
    )