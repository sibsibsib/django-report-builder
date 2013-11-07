from django import forms
from django.conf import settings

from report_builder.utils import javascript_date_format
from report_builder.models import Report, DisplayField, FilterField


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            'name',
            'distinct',
            'root_model',
        )


class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            'name',
            'distinct',
            'description',
        )
        widgets = {
            'description': forms.TextInput(
                attrs={'style': 'width:99%;', 'placeholder': 'Description'}),
        }


class DisplayFieldForm(forms.ModelForm):

    class Meta:
        model = DisplayField
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly': 'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly': 'readonly'}),
            'field': forms.HiddenInput(),
            'width': forms.TextInput(attrs={'class': 'small_input'}),
            'total': forms.CheckboxInput(attrs={'class': 'small_input'}),
            'sort': forms.TextInput(attrs={'class': 'small_input'}),
        }


class DisplayFieldAdminForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = DisplayField


class FilterFieldForm(forms.ModelForm):
    class Meta:
        model = FilterField
        widgets = {
            'path': forms.HiddenInput(),
            'path_verbose': forms.TextInput(attrs={'readonly': 'readonly'}),
            'field_verbose': forms.TextInput(attrs={'readonly': 'readonly'}),
            'field': forms.HiddenInput(),
            'filter_type': forms.Select(attrs={'onchange': 'check_filter_type(event.target)'})
        }

    def __init__(self, *args, **kwargs):
        super(FilterFieldForm, self).__init__(*args, **kwargs)
        # override the filter_value field with the models native ChoiceField
        if self.instance.choices:
            self.fields['filter_value'].widget = forms.Select(choices=self.instance.choices)
        if 'DateField' in self.instance.field_verbose or 'DateTimeField' in self.instance.field_verbose:
            widget = self.fields['filter_value'].widget
            widget.attrs['class'] = 'datepicker'
            widget.attrs['data-date-format'] = javascript_date_format(settings.DATE_FORMAT)


class FilterFieldAdminForm(forms.ModelForm):
    position = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = FilterField
