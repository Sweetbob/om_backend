from django import forms

from api import models


class ClientForm(forms.ModelForm):
    """
    Client的model_form
    """

    class Meta:
        model = models.Client
        fields = "__all__"

