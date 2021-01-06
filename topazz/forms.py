from django.forms import ModelForm
from .models import Client, Team


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'gender', 'email', 'phone_no', 'services']


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'role', 'description']
