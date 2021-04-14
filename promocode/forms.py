from django import forms


class GetParamsForm(forms.Form):
    group_name = forms.CharField(label='Название группы')
    amount = forms.IntegerField(label='Количество промо-кодов')

    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')
        if not group_name:
            raise forms.ValidationError('Введите название группы')
        return group_name

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount or amount < 1:
            raise forms.ValidationError('Количество кодов должно быть больше 1')
        return amount

    def clean(self):
        return self.cleaned_data
