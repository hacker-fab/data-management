from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from data_management.models import Profile, IVCurve, AluminumEtch, AluminumEvaporation, ChipList, ChipListSearch, GlassDeposition, Diffusion, HFOxideEtch, Patterning, PlasmaClean, PlasmaEtch

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

class GlassDepositionSearchForm(forms.ModelForm):
    class Meta:
        model = GlassDeposition
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class DiffusionSearchForm(forms.ModelForm):
    class Meta:
        model = Diffusion
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['AluminumEtch_temp'].required = True
        self.fields['AluminumEtch_duration'].required = True
        self.fields['AluminumEtch_stir_rpm'].required = True
        self.fields['AluminumEtch_metric_alum_etch_depth'].required = True
        self.fields['AluminumEtch_metric_photoresist_peeling'].required = True
        self.fields['AluminumEtch_metric_aluminum_peeling'].required = True

        self.fields['AluminumEtch_temp'].initial = 40
        self.fields['AluminumEtch_stir_rpm'].initial = 350

class AluminumEvaporationInputForm(forms.ModelForm):
    class Meta:
        model = AluminumEvaporation
        exclude = (
            'chip_owner',
            'AluminumEvaporation_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['AluminumEvaporation_duration'].required = True
        self.fields['AluminumEvaporation_pressure_before_start_seq'].required = True
        self.fields['AluminumEvaporation_pressure_before_evaporation'].required = True
        self.fields['AluminumEvaporation_metric_layer_thickness'].required = True
        self.fields['AluminumEvaporation_metric_layer_thick_qcm'].required = True
        self.fields['AluminumEvaporation_metric_deposition_rate'].required = True

        self.fields['AluminumEvaporation_pressure_before_start_seq'].initial = 1.5
        self.fields['AluminumEvaporation_pressure_before_evaporation'].initial = 6.4

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


class GlassDepositionInputForm(forms.ModelForm):
    class Meta:
        model = GlassDeposition
        exclude = (
            'chip_owner',
            'GlassDeposition_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['GlassDeposition_glass_type'].required = True
        self.fields['GlassDeposition_cleaning_step'].required = True
        self.fields['GlassDeposition_prebake_temp'].required = True
        self.fields['GlassDeposition_prebake_duration'].required = True
        self.fields['GlassDeposition_amount_drops'].required = True
        self.fields['GlassDeposition_spin_rpm'].required = True
        self.fields['GlassDeposition_spin_duration'].required = True
        self.fields['GlassDeposition_bake_temp'].required = True
        self.fields['GlassDeposition_bake_duration'].required = True
        self.fields['GlassDeposition_metric_cracking'].required = True
        self.fields['GlassDeposition_metric_particles'].required = True

        self.fields['GlassDeposition_glass_type'].initial = "P504"
        self.fields['GlassDeposition_cleaning_step'].initial = "Acetone + IPA"
        self.fields['GlassDeposition_prebake_temp'].initial = 100
        self.fields['GlassDeposition_prebake_duration'].initial = 20
        self.fields['GlassDeposition_amount_drops'].initial = 3
        self.fields['GlassDeposition_spin_rpm'].initial = 4000
        self.fields['GlassDeposition_spin_duration'].initial = 20

class DiffusionInputForm(forms.ModelForm):
    class Meta:
        model = Diffusion
        exclude = (
            'chip_owner',
            'Diffusion_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['Diffusion_temp'].required = True
        self.fields['Diffusion_duration'].required = True

        self.fields['Diffusion_temp'].initial = 1100
        self.fields['Diffusion_duration'].initial = 1800

class HFOxideEtchInputForm(forms.ModelForm):
    class Meta:
        model = HFOxideEtch
        exclude = (
            'chip_owner',
            'HFOxideEtch_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['HFOxideEtch_temp'].required = True
        self.fields['HFOxideEtch_duration'].required = True
        self.fields['HFOxideEtch_metric_oxide_etch_depth'].required = True

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['Patterning_underlying_material'].required = True
        self.fields['Patterning_cleaning_step'].required = True
        self.fields['Patterning_hdms_prebake_temp'].required = True
        self.fields['Patterning_hdms_prebake_duration'].required = True
        self.fields['Patterning_hdms_spin_rpm'].required = True
        self.fields['Patterning_hdms_spin_duration'].required = True
        self.fields['Patterning_hdms_bake_temp'].required = True
        self.fields['Patterning_hdms_bake_duration'].required = True
        self.fields['Patterning_photoresist_spin_rpm'].required = True
        self.fields['Patterning_photoresist_spin_duration'].required = True
        self.fields['Patterning_photoresist_bake_temp'].required = True
        self.fields['Patterning_photoresist_bake_duration'].required = True
        self.fields['Patterning_exposure_pattern'].required = True
        self.fields['Patterning_exposure_duration'].required = True
        self.fields['Patterning_develop_duration'].required = True
        self.fields['Patterning_metric_pattern_quality'].required = True
        self.fields['Patterning_metric_development'].required = True
        self.fields['Patterning_metric_contaminants'].required = True

        self.fields['Patterning_underlying_material'].initial = "PolySilicon"
        self.fields['Patterning_cleaning_step'].initial = "Acetone + IPA"
        self.fields['Patterning_hdms_prebake_temp'].initial = 100
        self.fields['Patterning_hdms_prebake_duration'].initial = 60
        self.fields['Patterning_hdms_spin_rpm'].initial = 3000
        self.fields['Patterning_hdms_spin_duration'].initial = 20
        self.fields['Patterning_hdms_bake_temp'].initial = 100
        self.fields['Patterning_hdms_bake_duration'].initial = 20
        self.fields['Patterning_photoresist_spin_rpm'].initial = 4000
        self.fields['Patterning_photoresist_spin_duration'].initial = 30
        self.fields['Patterning_photoresist_bake_temp'].initial = 100
        self.fields['Patterning_photoresist_bake_duration'].initial = 90
        self.fields['Patterning_exposure_duration'].initial = 8000
        self.fields['Patterning_develop_duration'].initial = 60

class PlasmaCleanInputForm(forms.ModelForm):
    class Meta:
        model = PlasmaClean
        exclude = (
            'chip_owner',
            'PlasmaClean_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['PlasmaClean_o2_flow'].required = True
        self.fields['PlasmaClean_rf_power'].required = True
        self.fields['PlasmaClean_clean_duration'].required = True

        self.fields['PlasmaClean_o2_flow'].initial = 10
        self.fields['PlasmaClean_rf_power'].initial = 100

class PlasmaEtchInputForm(forms.ModelForm):
    class Meta:
        model = PlasmaEtch
        exclude = (
            'chip_owner',
            'PlasmaEtch_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chip_number'].required = True
        self.fields['PlasmaEtch_rf_power'].required = True
        self.fields['PlasmaEtch_etch_duration'].required = True
        self.fields['PlasmaEtch_etch_depth'].required = True

        self.fields['PlasmaEtch_sf6_flow'].initial = 10
        self.fields['PlasmaEtch_rf_power'].initial = 100
        self.fields['PlasmaEtch_etch_duration'].initial = 100
        self.fields['PlasmaEtch_etch_depth'].initial = 500


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