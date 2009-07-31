from django import forms

class PlayerForm(forms.Form):
	Position = forms.Charfield()
