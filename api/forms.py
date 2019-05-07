from django import forms

from . import models


class ChargerForm(forms.ModelForm):
    """
    Charger的model_form
    """

    class Meta:
        model = models.Charger
        fields = "__all__"


class CollectiveForm(forms.ModelForm):

    class Meta:
        model = models.Collective
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



class ProductLineForm(forms.ModelForm):

    class Meta:
        model = models.ProductLine
        fields = "__all__"

class ProjectForm(forms.ModelForm):

    class Meta:
        model = models.Project
        fields = "__all__"


class AuthCenterForm(forms.ModelForm):

    class Meta:
        model = models.AuthCenter
        fields = "__all__"


class IntervalForm(forms.ModelForm):

    class Meta:
        model = models.Interval
        fields = "__all__"


class MissionForm(forms.ModelForm):

    class Meta:
        model = models.Mission
        fields = "__all__"


class CxfbForm(forms.ModelForm):

    class Meta:
        model = models.Cxfb
        fields = "__all__"


class CrontabForm(forms.ModelForm):

    class Meta:
        model = models.Crontab
        fields = "__all__"


