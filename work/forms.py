from django import forms
from .models import WorkTime, WorkPlace


class CreateWorkTimeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        time_start = cleaned_data.get('time_start')
        time_end = cleaned_data.get('time_end')

        if time_start and time_end:
            if time_start >= time_end:
                raise forms.ValidationError('Incorrect time values.')

    class Meta:
        model = WorkTime
        fields = ('date', 'time_start', 'time_end')


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = []


class CreateWorkPlace(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        manager = cleaned_data.get('manager')
        work = cleaned_data.get('work')

        if manager.company != work.company:
            raise forms.ValidationError('Should belong to the same company.')

    class Meta:
        model = WorkPlace
        fields = ('manager', 'work', 'worker', 'week_limit')
