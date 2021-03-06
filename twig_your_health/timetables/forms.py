from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Doctor
from timetables.models import ShiftType, Shift, Visit


class ShiftTypeForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = ShiftType
        fields = ['title', 'start', 'doctor', 'end', 'gap']


class ShiftForm(forms.ModelForm):
    day = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = Shift
        fields = ['shift_type', 'day']

    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor')
        super(ShiftForm, self).__init__(*args, **kwargs)
        self.fields['shift_type'].queryset = ShiftType.objects.filter(doctor=self.doctor)

    def clean_shift_type(self):
        shift_type = self.cleaned_data['shift_type']
        if not shift_type.doctor == self.doctor:
            raise ValidationError("Shift type doesn't belong to the doctor")
        return shift_type


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['shift', 'start', 'end', 'patient']
