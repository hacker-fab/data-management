from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from data_management.models import Profile, IVCurve, AluminumEtch, AluminumEvaporation, ChipList, ChipListSearch, GlassDeposition_P504, HFOxideEtch, Patterning, PlasmaClean, PlasmaEtch

UNIVERSITY_CHOICES =( 
    ("CMU", "Carnegie Mellon University"), 
)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('text', 'picture')
        widgets = {
            'text': forms.Textarea(attrs={'id': 'id_bio_input_text', 'rows': '3'}),
            'picture': forms.FileInput(attrs={'id': 'id_profile_picture'})
        }
        labels = {
            'text': "",
            'picture': "Upload Image"
        }

class IVCurveForm(forms.ModelForm):
    class Meta:
        model = IVCurve
        exclude = (
            'chip_owner',
            'device_id',
            'gate_voltages',
            'captures'
        )

    device_id = forms.CharField(max_length=50, required=True, 
                                widget=forms.TextInput(
            attrs={"placeholder": "ex. 2b1",}
        ))
    gate_voltages = forms.CharField(max_length=500, required=True, 
                                    widget=forms.TextInput(
            attrs={"placeholder": "ex. 1, 2, 3, 4, 5",}
        ))

class AluminumEtchSearchForm(forms.ModelForm):
    class Meta:
        model = AluminumEtch
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class AluminumEvaporationSearchForm(forms.ModelForm):
    class Meta:
        model = AluminumEvaporation
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class ChipListSearchForm(forms.ModelForm):
    class Meta:
        model = ChipListSearch
        exclude = ()
        labels = {
        }

class GlassDeposition_P504SearchForm(forms.ModelForm):
    class Meta:
        model = GlassDeposition_P504
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class HFOxideEtchSearchForm(forms.ModelForm):
    class Meta:
        model = HFOxideEtch
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class PatterningSearchForm(forms.ModelForm):
    class Meta:
        model = Patterning
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class PlasmaCleanSearchForm(forms.ModelForm):
    class Meta:
        model = PlasmaClean
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class PlasmaEtchSearchForm(forms.ModelForm):
    class Meta:
        model = PlasmaEtch
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class AluminumEtchInputForm(forms.ModelForm):
    class Meta:
        model = AluminumEtch
        exclude = (
            'chip_owner',
            'AluminumEtch_step_time',
            'content_type',
        )

class AluminumEvaporationInputForm(forms.ModelForm):
    class Meta:
        model = AluminumEvaporation
        exclude = (
            'chip_owner',
            'AluminumEvaporation_step_time',
            'content_type',
        )

class ChipListForm(forms.ModelForm):
    #university = forms.ChoiceField(choices = UNIVERSITY_CHOICES,
    #                              label="University:", 
    #                              required=False)
    class Meta:
        model = ChipList
        exclude = (
            'chip_owner',
            'chip_number',
            'creation_time',
            'picture',
            'content_type',
            #'uni'
        )


class GlassDeposition_P504InputForm(forms.ModelForm):
    class Meta:
        model = GlassDeposition_P504
        exclude = (
            'chip_owner',
            'GlassDeposition_P504_step_time',
            'content_type',
        )

class HFOxideEtchInputForm(forms.ModelForm):
    class Meta:
        model = HFOxideEtch
        exclude = (
            'chip_owner',
            'HFOxideEtch_step_time',
            'content_type',
        )

class PatterningInputForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Patterning
        exclude = (
            'chip_owner',
            'Patterning_step_time',
            'content_type',
        )

class PlasmaCleanInputForm(forms.ModelForm):
    class Meta:
        model = PlasmaClean
        exclude = (
            'chip_owner',
            'PlasmaClean_step_time',
            'content_type',
        )

class PlasmaEtchInputForm(forms.ModelForm):
    class Meta:
        model = PlasmaEtch
        exclude = (
            'chip_owner',
            'PlasmaEtch_step_time',
            'content_type',
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    
class RegisterForm(forms.Form):
    username   = forms.CharField(max_length=20)
    password  = forms.CharField(max_length=200,
                                 label='Password', 
                                 widget=forms.PasswordInput())
    confirm_password  = forms.CharField(max_length=200,
                                 label='Confirm',  
                                 widget=forms.PasswordInput())
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username