from django import forms
# from django.core.exceptions import ValidationError

class homeForm(forms.Form):
    rounds = forms.TypedChoiceField(choices = [(None,"Number of rounds"), (1,1), (8,8), (16, 16), (32,32)], coerce = int,  widget=forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}), required=True)
    length = forms.TypedChoiceField(choices = [(None, "Length of plaintext"), (32,32), (64,64), (128,128)], coerce = int, widget=forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}), required=True)
    block = forms.CharField(max_length=128, min_length=32, required=True, widget=forms.Textarea(attrs={'rows':5, 'placeholder':'Plaintext', 'class':"form-control", 'id':'block'}))
    key = forms.CharField(max_length=128, min_length=32, required=True, widget=forms.Textarea(attrs={'rows':5, 'placeholder':'Key', 'class':"form-control"}))
    option = forms.ChoiceField(choices=[(None,"Change 1 bit in"), ("p","Plaintext"), ("k","Key")], widget=forms.Select(attrs={'class':'custom-select my-1 mr-sm-2'}), required=True)