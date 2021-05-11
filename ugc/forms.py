from django import forms

from ugc.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
            'button_value'
        )
        widgets = {
            'name': forms.TextInput
        }
