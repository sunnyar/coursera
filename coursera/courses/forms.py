from django import forms
from .models import Category


CATEGORY_CHOICES = (('all', 'All Categories'),)
for category in Category.objects.all().values() :
    CATEGORY_CHOICES += ((category['short_name'], category['name']),)


LANGUAGE_CHOICES = (('all', 'All Languages'), ('en', 'English'), ('zh-cn', 'Chinese'),
                    ('es', 'Spainish'), ('fr', 'French'), ('ru', 'Russian'),
                    ('tr', 'Turkish'), ('it', 'Italian'), ('ar', 'Arabic'))

class CourseForm(forms.Form) :

    categories = forms.MultipleChoiceField(choices=CATEGORY_CHOICES,
                    widget=forms.CheckboxSelectMultiple)#, initial = ['all'])
    languages  = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                    choices=LANGUAGE_CHOICES)#, initial = ['all'])
