from .models import Deposit, Book, RatingModel
from django import forms

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class RatingForm(forms.ModelForm):
    class Meta:
        model = RatingModel
        fields = ['rate']