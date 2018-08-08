from django.forms import ModelForm, Textarea
from events.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }
from django import forms
from events.models import events


class NewEventForm(forms.Form):
    name = forms.CharField(max_length =100)
    keyword = forms.CharField(max_length =100)
    description = forms.CharField(max_length =100)
    city = forms.CharField(max_length =100)
    state = forms.CharField(max_length =100)
    address = forms.CharField(max_length =100)
    #    fields = ['name', 'keyword', 'description', 'city','state','address']



class searchForm(forms.Form):
    city = forms.CharField(max_length=50, required=True)
    keyword = forms.CharField(max_length=100, required=True)
