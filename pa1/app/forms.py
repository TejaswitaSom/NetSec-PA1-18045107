from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class homeForm(forms.Form):
    rounds = forms.TypedChoiceField(error_messages={'invalid_choice':"Choose a correct field"}, choices = [(0,"Number of rounds"), (1,1), (8,8), (16, 16), (32,32)], coerce = int,  widget=forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}), required=True)
    length = forms.TypedChoiceField(choices = [(0, "Choose length of block"), (32,32), (64,64), (128,128)], coerce = int, widget=forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}), required=True)
    block = forms.CharField(max_length=128, min_length=32, required=True, widget=forms.TextInput(attrs={'placeholder':'Input block', 'class':"form-control"}))
    key = forms.CharField(max_length=128, min_length=32, required=True, widget=forms.TextInput(attrs={'placeholder':'Input key', 'class':"form-control"}))
    option = forms.ChoiceField(choices=[(0,"Select where to change 1 bit"), ("p","Change in 1 bit in plaintext"), ("k","Change in 1 bit in key")], widget=forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}), required=True)

    def clean(self):
        cleaned_data = super(homeForm, self).clean()
        r = cleaned_data.get("rounds")
        l = cleaned_data.get("length")
        o = cleaned_data.get("option")
        b = cleaned_data.get("block")
        k = cleaned_data.get("key")
        if r==0 or l==0 or o==0 or len(b)<l or len(k)<l:
            raise forms.ValidationError("Choose a correct field",)
