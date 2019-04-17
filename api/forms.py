from django import forms

from . import models


class ChargerForm(forms.ModelForm):
    """
    Charger的model_form
    """

    class Meta:
        model = models.Charger
        fields = "__all__"


class RoomForm(forms.ModelForm):
    """
    Room的model_form
    """

    class Meta:
        model = models.Room
        fields = "__all__"


class CabinetForm(forms.ModelForm):
    """
    Cabinet的model_form
    """

    class Meta:
        model = models.Cabinet
        fields = "__all__"