from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from data_management.models import Profile, IVCurve, AluminumEtch, AluminumEvaporation, ChipList, ChipListSearch, GlassDeposition, Diffusion, HFOxideEtch, KOHEtch, NickelPlating, Patterning, PlasmaClean, PlasmaEtch

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
    AluminumEtch_step_time_max                  = forms.DateTimeField(required=False, label="Max AluminumEtch step time")
    AluminumEtch_temp_max                       = forms.DecimalField(required=False, decimal_places=3, label="Max Etch temp (°C) *")
    AluminumEtch_duration_max                   = forms.IntegerField(required=False, label="Max Etch duration (sec) *")
    AluminumEtch_stir_rpm_max                   = forms.IntegerField(required=False, label="Max Stir speed (rpm) *")
    AluminumEtch_metric_alum_etch_depth_max     = forms.IntegerField(required=False, label="Max Etch depth (nm) *")

    class Meta:
        model = AluminumEtch
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
            'AluminumEtch_step_time': "Min "+AluminumEtch._meta.get_field('AluminumEtch_step_time').verbose_name, 
            'AluminumEtch_temp': "Min "+AluminumEtch._meta.get_field('AluminumEtch_temp').verbose_name, 
            'AluminumEtch_duration': "Min "+AluminumEtch._meta.get_field('AluminumEtch_duration').verbose_name, 
            'AluminumEtch_stir_rpm': "Min "+AluminumEtch._meta.get_field('AluminumEtch_stir_rpm').verbose_name, 
            'AluminumEtch_metric_alum_etch_depth': "Min "+AluminumEtch._meta.get_field('AluminumEtch_metric_alum_etch_depth').verbose_name, 
        }

class AluminumEvaporationSearchForm(forms.ModelForm):
    AluminumEvaporation_step_time_max                   = forms.DateTimeField(required=False,label="Max AluminumEvaporation step time")
    AluminumEvaporation_duration_max                    = forms.IntegerField(required=False, label="Max Evaporation duration (sec) *")
    AluminumEvaporation_pressure_before_start_seq_max   = forms.DecimalField(required=False, decimal_places=3, label="Max Pressure before start (torr E-6) *")
    AluminumEvaporation_pressure_before_evaporation_max = forms.DecimalField(required=False, decimal_places=3, label="Max Pressure before evaporation (torr E-6) *")
    AluminumEvaporation_metric_layer_thickness_max      = forms.DecimalField(required=False, decimal_places=3, label="Max Layer thickness by profilometer (Å) *")
    AluminumEvaporation_metric_layer_thick_qcm_max      = forms.DecimalField(required=False, decimal_places=3, label="Max Layer thickness by QCM (Å) *")
    AluminumEvaporation_metric_deposition_rate_max      = forms.DecimalField(required=False, decimal_places=3, label="Max Deposition rate (Å/sec) *")

    class Meta:
        model = AluminumEvaporation
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
            'AluminumEvaporation_step_time': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_step_time').verbose_name,
            'AluminumEvaporation_duration': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_duration').verbose_name,
            'AluminumEvaporation_pressure_before_start_seq': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_pressure_before_start_seq').verbose_name,
            'AluminumEvaporation_pressure_before_evaporation': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_pressure_before_evaporation').verbose_name,
            'AluminumEvaporation_metric_layer_thickness': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_metric_layer_thickness').verbose_name,
            'AluminumEvaporation_metric_layer_thick_qcm': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_metric_layer_thick_qcm').verbose_name,
            'AluminumEvaporation_metric_deposition_rate': "Min "+AluminumEvaporation._meta.get_field('AluminumEvaporation_metric_deposition_rate').verbose_name,
        }

class ChipListSearchForm(forms.ModelForm):
    class Meta:
        model = ChipListSearch
        exclude = ()
        labels = {
        }

class GlassDepositionSearchForm(forms.ModelForm):
    GlassDeposition_step_time_max               = forms.DateTimeField(required=False, label="Max GlassDeposition step time")
    GlassDeposition_prebake_temp_max            = forms.DecimalField(required=False, decimal_places=3, label="Max Prebake temp (°C) *")
    GlassDeposition_prebake_duration_max        = forms.IntegerField(required=False,  label="Max Prebake duration (sec) *")
    GlassDeposition_amount_drops_max            = forms.IntegerField(required=False,  label="Max Number of drops *")
    GlassDeposition_spin_rpm_max                = forms.IntegerField(required=False,  label="Max Spin speed (rpm) *")
    GlassDeposition_spin_duration_max           = forms.IntegerField(required=False,  label="Max Spin duration (sec) *")
    GlassDeposition_bake_temp_max               = forms.DecimalField(required=False, decimal_places=3, label="Max Bake temp (°C) *")
    GlassDeposition_bake_duration_max           = forms.IntegerField(required=False,  label="Max Bake duration (sec) *")

    class Meta:
        model = GlassDeposition
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
            'GlassDeposition_step_time': "Min " + GlassDeposition._meta.get_field('GlassDeposition_step_time').verbose_name,
            'GlassDeposition_prebake_temp': "Min " + GlassDeposition._meta.get_field('GlassDeposition_prebake_temp').verbose_name,
            'GlassDeposition_prebake_duration': "Min " + GlassDeposition._meta.get_field('GlassDeposition_prebake_duration').verbose_name,
            'GlassDeposition_amount_drops': "Min " + GlassDeposition._meta.get_field('GlassDeposition_amount_drops').verbose_name,
            'GlassDeposition_spin_rpm': "Min " + GlassDeposition._meta.get_field('GlassDeposition_spin_rpm').verbose_name,
            'GlassDeposition_spin_duration': "Min " + GlassDeposition._meta.get_field('GlassDeposition_spin_duration').verbose_name,
            'GlassDeposition_bake_temp': "Min " + GlassDeposition._meta.get_field('GlassDeposition_bake_temp').verbose_name,
            'GlassDeposition_bake_duration': "Min " + GlassDeposition._meta.get_field('GlassDeposition_bake_duration').verbose_name,
        }

class DiffusionSearchForm(forms.ModelForm):
    Diffusion_step_time_max                     = forms.DateTimeField(required=False, label="Max Diffusion step time")
    Diffusion_temp_max                          = forms.DecimalField(required=False, decimal_places=3, null=True, label="Max Diffusion temp (°C) *")
    Diffusion_duration_max                      = forms.IntegerField(required=False, label="Max Diffusion duration (sec) *")

    class Meta:
        model = Diffusion
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
            'Diffusion_step_time': "Min" + Diffusion._meta.get_field('Diffusion_step_time').verbose_name,
            'Diffusion_temp': "Min" + Diffusion._meta.get_field('Diffusion_temp').verbose_name,
            'Diffusion_duration': "Min" + Diffusion._meta.get_field('Diffusion_duration').verbose_name,
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

class KOHEtchSearchForm(forms.ModelForm):
    class Meta:
        model = KOHEtch
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class NickelPlatingSearchForm(forms.ModelForm):
    class Meta:
        model = NickelPlating
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
        }

class PatterningSearchForm(forms.ModelForm):
    Patterning_step_time_max                    = forms.DateTimeField(required=False, label="Max Patterning step time")
    Patterning_hdms_prebake_temp_max            = forms.DecimalField(decimal_places=3, required=False,label="Max HMDS prebake temp (°C) *")
    Patterning_hdms_prebake_duration_max        = forms.IntegerField(required=False,label="Max HMDS prebake duration (sec) *")
    Patterning_hdms_spin_rpm_max                = forms.IntegerField(required=False,label="Max HMDS spin speed (rpm) *")
    Patterning_hdms_spin_duration_max           = forms.IntegerField(required=False,label="Max HMDS spin duration (sec) *")
    Patterning_hdms_bake_temp_max               = forms.DecimalField(decimal_places=3, required=False,label="Max HMDS bake temp (°C) *")
    Patterning_hdms_bake_duration_max           = forms.IntegerField(required=False,label="Max HMDS bake duration (sec) *")
    Patterning_photoresist_spin_rpm_max         = forms.IntegerField(required=False,label="Max PR spin speed (rpm) *")
    Patterning_photoresist_spin_duration_max    = forms.IntegerField(required=False,label="Max PR spin duration (sec) *")
    Patterning_photoresist_bake_temp_max        = forms.DecimalField(decimal_places=3, required=False,label="Max PR bake temp (°C) *")
    Patterning_photoresist_bake_duration_max    = forms.IntegerField(required=False,label="Max PR bake duration (sec) *")
    Patterning_exposure_duration_max            = forms.IntegerField(required=False,label="Max Exposure duration (ms) *")
    Patterning_develop_duration_max             = forms.IntegerField(required=False,label="Max Develop duration (sec) *")
    
    class Meta:
        model = Patterning
        exclude = (
            'picture',
            'content_type',
        )
        labels = {
            'chip_owner': "Enter Username",
            'Patterning_step_time': "Min" + Patterning._meta.get_field('Patterning_step_time').verbose_name,
            'Patterning_hdms_prebake_temp': "Min" + Patterning._meta.get_field('Patterning_hdms_prebake_temp').verbose_name,
            'Patterning_hdms_prebake_duration': "Min" + Patterning._meta.get_field('Patterning_hdms_prebake_duration').verbose_name,
            'Patterning_hdms_spin_rpm': "Min" + Patterning._meta.get_field('Patterning_hdms_spin_rpm').verbose_name,
            'Patterning_hdms_spin_duration': "Min" + Patterning._meta.get_field('Patterning_hdms_spin_duration').verbose_name,
            'Patterning_hdms_bake_temp': "Min" + Patterning._meta.get_field('Patterning_hdms_bake_temp').verbose_name,
            'Patterning_hdms_bake_duration': "Min" + Patterning._meta.get_field('Patterning_hdms_bake_duration').verbose_name,
            'Patterning_photoresist_spin_rpm': "Min" + Patterning._meta.get_field('Patterning_photoresist_spin_rpm').verbose_name,
            'Patterning_photoresist_spin_duration': "Min" + Patterning._meta.get_field('Patterning_photoresist_spin_duration').verbose_name,
            'Patterning_photoresist_bake_temp': "Min" + Patterning._meta.get_field('Patterning_photoresist_bake_temp').verbose_name,
            'Patterning_photoresist_bake_duration': "Min" + Patterning._meta.get_field('Patterning_photoresist_bake_duration').verbose_name,
            'Patterning_exposure_duration': "Min" + Patterning._meta.get_field('Patterning_exposure_duration').verbose_name,
            'Patterning_develop_duration': "Min" + Patterning._meta.get_field('Patterning_develop_duration').verbose_name,
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

class KOHEtchInputForm(forms.ModelForm):
    class Meta:
        model = KOHEtch
        exclude = (
            'chip_owner',
            'KOHEtch_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['chip_number'].required = True
        self.fields['KOHEtch_concentration'].required = True
        self.fields['KOHEtch_temp'].required = True
        self.fields['KOHEtch_duration'].required = True
        self.fields['KOHEtch_rpm'].required = True

class NickelPlatingInputForm(forms.ModelForm):
    class Meta:
        model = NickelPlating
        exclude = (
            'chip_owner',
            'NickelPlating_step_time',
            'content_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['chip_number'].required = True
        self.fields['NickelPlating_solution'].required = True
        self.fields['NickelPlating_temp'].required = True
        self.fields['NickelPlating_duration'].required = True

        self.fields['NickelPlating_solution'].initial = "Nickelex"
        self.fields['NickelPlating_duration'].initial = 300
        self.fields['NickelPlating_temp'].initial = 290

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