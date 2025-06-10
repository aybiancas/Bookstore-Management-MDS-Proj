from django import forms
from .models import Sale, Book

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['book', 'qty']
        labels = {
            'book': 'Carte',
            'qty': 'Cantitate',
        }

class StockForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label='Carte')
    class Meta:
        model = Book
        fields = ['stock']
        labels = {
            'stock': 'Cantitate',
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'category', 'isbn', 'price', 'stock']
        labels = {
            'title': 'Carte',
            'authors': 'Autori',
            'category': 'Categorie',
            'isbn': 'ISBN',
            'price': 'Pret',
            'stock': 'Stoc',
        }