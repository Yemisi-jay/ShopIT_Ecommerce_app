from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
