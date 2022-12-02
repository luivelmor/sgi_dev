from django import forms
from .models import Device
from .models import Invoice
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _


class DeviceForm(forms.ModelForm):
    quantity = forms.CharField(label="Cantidad", initial=1)

    def save(self, commit=True):
        quantity = self.cleaned_data.get('quantity', None)
        device = super(DeviceForm, self).save(commit=False)
        for i in range(1, int(quantity)):
            device.save()
            device.pk = None

        return device

    class Meta:
        model = Device
        fields = ('room', 'deviceModel', 'notes')


class InvoiceForm(forms.ModelForm):

    # Si descomentamos las siguientes líneas, las opciones "filter_vertical" ó "filter_horizontal" no tienen efecto
    #devices = forms.ModelMultipleChoiceField(
    #    queryset=Device.objects.all(),
    #    widget=forms.CheckboxSelectMultiple,
    #    required=True,
    #    label='Dispositivos',
    #)

    def save(self, commit=True):
        invoice = super(InvoiceForm, self).save(commit=False)
        if commit:
            invoice.save()
            self.save_m2m()
        return invoice

    class Meta:
        model = Invoice
        fields = '__all__'
        # Si descomentamos las siguientes líneas, las opciones "filter_vertical" ó "filter_horizontal" no tienen efecto
        #widgets = {
        #    'devices': forms.SelectMultiple(attrs={'size': 30})
        #}
