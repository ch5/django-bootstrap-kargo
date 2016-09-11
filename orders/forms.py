from django import forms
from django.utils.translation import ugettext_lazy as _
from orders.models import ODOrder, Vehicle


class ODOrderForm(forms.ModelForm):
    """
    Form to manage Order data-entry
    """
    name = forms.CharField(label=_('Nama Produk'))

    class Meta:
        model = ODOrder
        fields = ('name', 'phone', 'price')

########################################################################
#                       My Form task                                   #
########################################################################
class VehicleCreateForm(forms.ModelForm):
    """
    Form to manage Vehicle data-entry
    """
    class Meta:
        model = Vehicle
        fields = [
        'name',
        'driver',
        'number',
        'photo',
        'capacity'
        ]

########################################################################
#                       End Task                                       #
########################################################################
