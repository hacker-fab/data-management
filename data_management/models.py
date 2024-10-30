# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from data_management.common import MATERIAL_CHOICES, GLASS_CHOICES, QUALITY_CHOICES, BINARY_CHOICES



class ChipList(models.Model):
    chip_number = models.IntegerField(primary_key=True, blank=False)
    chip_owner    = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    creation_time = models.DateTimeField(blank=True)
    notes = models.CharField(max_length=400, blank=True, null=True)  # This field type is a guess.
    IVCurrents_CSV = models.FileField(blank=True)
    IVVoltages_CSV = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, blank=True)
    #uni  = models.CharField(blank=True, max_length=300)

class Profile(models.Model):
    text  = models.CharField(blank=True, max_length=300)
    user    = models.OneToOneField(User, on_delete=models.PROTECT, related_name="entry_creators")
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    followers = models.ManyToManyField(User, related_name="followers")
    #uni  = models.CharField(blank=True, max_length=300)

class ChipListSearch(models.Model):
    chip_number = models.IntegerField(blank=True)
    chip_owner    = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    creation_time = models.DateTimeField(blank=True)
    notes = models.CharField(max_length=400, blank=True, null=True)  # This field type is a guess.

class SMU_capture(models.Model):
    csv_current = models.FileField(blank=True)
    csv_voltage = models.FileField(blank=True)
    plot = models.ImageField(blank=True)

class IVCurve(models.Model):
    chip_number = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=True)
    chip_owner    = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    drain_resistance = models.IntegerField(blank=False, default=100)
    gate_resistance =  models.IntegerField(blank=False, default=100)
    device_id = models.CharField(max_length=50, blank=False)
    gate_voltages = models.CharField(max_length=500, blank=False)
    captures = models.ManyToManyField(SMU_capture)
class AluminumEtch(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    AluminumEtch_step_time                  = models.DateTimeField(blank=False)
    AluminumEtch_temp                       = models.IntegerField(blank=False, null=True, verbose_name="Etch temp (°C) *")
    AluminumEtch_time                       = models.PositiveIntegerField(blank=False, null=True, verbose_name="Etch time (sec) *")
    AluminumEtch_stir_rpm                   = models.PositiveIntegerField(blank=False, null=True, verbose_name="Stir speed (rpm) *")
    AluminumEtch_metric_alum_etch_depth     = models.PositiveIntegerField(blank=False, null=True, verbose_name="Etch depth (nm) *")
    AluminumEtch_metric_photoresist_peeling = models.CharField(max_length=400, blank=True, null=True, choices=BINARY_CHOICES, verbose_name="PR peeling?")
    AluminumEtch_metric_aluminum_peeling    = models.CharField(max_length=400, blank=True, null=True, choices=BINARY_CHOICES, verbose_name="Aluminum peeling?")
    AluminumEtch_metrology_link             = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    AluminumEtch_notes                      = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")

class AluminumEvaporation(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    AluminumEvaporation_step_time           = models.DateTimeField(blank=False)
    AluminumEvaporation_temp                = models.CharField(max_length=400, blank=True, null=True, verbose_name="Evaporation temp (°C)")
    AluminumEvaporation_time                = models.CharField(max_length=400, blank=True, null=True, verbose_name="Evaporation time (sec)")
    AluminumEvaporation_pressure_before_start_seq   = models.CharField(max_length=400, blank=True, null=True, verbose_name="Pressure before start (torr)")
    AluminumEvaporation_pressure_before_evaporation = models.CharField(max_length=400, blank=True, null=True, verbose_name="Pressure before evaporation (torr)")
    AluminumEvaporation_metric_layer_thickness      = models.CharField(max_length=400, blank=True, null=True, verbose_name="Layer thickness by profilometer (Å)")
    AluminumEvaporation_metric_layer_thick_qcm      = models.CharField(max_length=400, blank=True, null=True, verbose_name="Layer thickness by QCM (Å)")
    AluminumEvaporation_metric_deposition_rate      = models.CharField(max_length=400, blank=True, null=True, verbose_name="Deposition rate (Å/sec)")
    AluminumEvaporation_metrology_link      = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    AluminumEvaporation_notes               = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")

class GlassDeposition(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    GlassDeposition_step_time               = models.DateTimeField(blank=False)
    GlassDeposition_glass_type              = models.CharField(max_length=400, blank=False, choices=GLASS_CHOICES, default='P504', verbose_name="Glass type *")
    GlassDeposition_cleaning_step           = models.CharField(max_length=400, blank=True, null=True, default="Acetone + IPA", verbose_name="Cleaning step")
    GlassDeposition_days_glass_at_room_temp = models.CharField(max_length=400, blank=True, null=True, verbose_name="Days at room temp")
    GlassDeposition_prebake_temp            = models.CharField(max_length=400, blank=True, null=True, verbose_name="Prebake temp (°C)")
    GlassDeposition_prebake_time            = models.CharField(max_length=400, blank=True, null=True, verbose_name="Prebake time (sec)")
    GlassDeposition_amount_drops            = models.PositiveIntegerField(blank=False, null=True, verbose_name="Number of drops *")
    GlassDeposition_spin_rpm                = models.PositiveIntegerField(blank=False, default="4000", verbose_name="Spin speed (rpm) *")
    GlassDeposition_spin_time               = models.PositiveIntegerField(blank=False, default="20", verbose_name="Spin time (sec) *")
    GlassDeposition_bake_temp               = models.IntegerField(blank=False, null=True, verbose_name="Bake temp (°C) *")
    GlassDeposition_bake_time               = models.PositiveIntegerField(blank=False, null=True, verbose_name="Bake time (sec) *")
    GlassDeposition_diffusion_temp          = models.CharField(max_length=400, blank=True, null=True, verbose_name="Diffusion temp (°C)")
    GlassDeposition_diffusion_time          = models.CharField(max_length=400, blank=True, null=True, verbose_name="Diffusion time (sec)")
    GlassDeposition_humidity                = models.CharField(max_length=400, blank=True, null=True, verbose_name="Humidity")
    GlassDeposition_metric_layer_thickness  = models.CharField(max_length=400, blank=True, null=True, verbose_name="Layer thickness (um)")
    GlassDeposition_metric_cracking         = models.CharField(max_length=400, blank=True, null=True, choices=BINARY_CHOICES, verbose_name="Cracking?")
    GlassDeposition_metric_particles        = models.CharField(max_length=400, blank=True, null=True, choices=BINARY_CHOICES, verbose_name="Particles?")
    GlassDeposition_metrology_link          = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    GlassDeposition_notes                   = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")

class HFOxideEtch(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    HFOxideEtch_step_time                     = models.DateTimeField(blank=False)
    HFOxideEtch_max_temp_glass_reached        = models.CharField(max_length=400, blank=True, null=True, verbose_name="Max glass temp (°C)")
    HFOxideEtch_temp                          = models.IntegerField(blank=False, null=True, verbose_name="Etch temp (°C) *")
    HFOxideEtch_time                          = models.PositiveIntegerField(blank=False, null=True, verbose_name="Etch time (sec) *")
    HFOxideEtch_metric_oxide_etch_depth       = models.PositiveIntegerField(blank=False, null=True, verbose_name="Etch depth (nm) *")
    HFOxideEtch_metrology_link                = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    HFOxideEtch_notes                         = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")

class Patterning(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    Patterning_step_time                    = models.DateTimeField(blank=False)
    Patterning_underlying_material          = models.CharField(max_length=400, blank=False, choices=MATERIAL_CHOICES, default='PolySilicon', verbose_name="Underlying material *")
    Patterning_hdms_prebake_temp            = models.CharField(max_length=400, blank=True, null=True, verbose_name="HMDS prebake temp (°C)")
    Patterning_hdms_prebake_time            = models.CharField(max_length=400, blank=True, null=True, verbose_name="HMDS prebake time (sec)")
    Patterning_hdms_spin_rpm                = models.PositiveIntegerField(blank=False, default="3000", verbose_name="HMDS spin speed (rpm) *")
    Patterning_hdms_spin_time               = models.PositiveIntegerField(blank=False, default="20", verbose_name="HMDS spin time (sec) *")
    Patterning_hdms_bake_temp               = models.IntegerField(blank=False, default="100", verbose_name="HMDS bake temp (°C) *")
    Patterning_hdms_bake_time               = models.PositiveIntegerField(blank=False, default="20", verbose_name="HMDS bake time (sec) *")
    Patterning_photoresist_spin_rpm         = models.PositiveIntegerField(blank=False, default="4000", verbose_name="PR spin speed (rpm) *")
    Patterning_photoresist_spin_time        = models.PositiveIntegerField(blank=False, default="30", verbose_name="PR spin time (sec) *")
    Patterning_photoresist_bake_temp        = models.IntegerField(blank=False, default="100", verbose_name="PR bake temp (°C) *")
    Patterning_photoresist_bake_time        = models.PositiveIntegerField(blank=False, default="90", verbose_name="PR bake time (sec) *")
    Patterning_exposure_pattern             = models.CharField(max_length=400, blank=False, null=True, verbose_name="Exposure pattern *")
    Patterning_exposure_time                = models.PositiveIntegerField(blank=False, default="8000", verbose_name="Exposure time (sec) *")
    Patterning_develop_time                 = models.PositiveIntegerField(blank=False, default="60", verbose_name="Develop time (sec) *")
    Patterning_metric_pattern_quality       = models.CharField(max_length=400, blank=True, null=True, choices=QUALITY_CHOICES, verbose_name="Pattern quality")
    Patterning_metric_leftover_photoresist  = models.CharField(max_length=400, blank=True, null=True, choices=BINARY_CHOICES, verbose_name="Leftover PR?")
    Patterning_metric_missing_photoresist   = models.CharField(max_length=400, blank=True, null=True, choices=BINARY_CHOICES, verbose_name="Missing PR?")
    Patterning_metric_contaminants          = models.CharField(max_length=400, blank=True, null=True, verbose_name="Contaminants")
    Patterning_metrology_link               = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    Patterning_notes                        = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")

class PlasmaClean(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    PlasmaClean_step_time                   = models.DateTimeField(blank=False)
    PlasmaClean_o2_flow                     = models.CharField(max_length=400, blank=True, null=True, verbose_name="O2 flow (sccm)")
    PlasmaClean_rf_power                    = models.CharField(max_length=400, blank=True, null=True, verbose_name="RF power (Watts)")
    PlasmaClean_clean_time                  = models.CharField(max_length=400, blank=True, null=True, verbose_name="Clean time (sec)")
    PlasmaClean_metric_contaminants         = models.CharField(max_length=400, blank=True, null=True, verbose_name="Contaminants")
    PlasmaClean_metrology_link              = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    PlasmaClean_notes                       = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")

class PlasmaEtch(models.Model):
    chip_number                             = models.ForeignKey(ChipList, on_delete=models.PROTECT, blank=False, verbose_name="Chip number *")
    chip_owner                              = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    picture                                 = models.FileField(blank=True)
    content_type                            = models.CharField(max_length=50, blank=True)
    PlasmaEtch_step_time                    = models.DateTimeField(blank=False)
    PlasmaEtch_o2_flow                      = models.CharField(max_length=400, blank=True, null=True, verbose_name="O2 flow (sccm)")
    PlasmaEtch_sf6_flow                     = models.CharField(max_length=400, blank=True, null=True, default="10", verbose_name="SF6 flow (sccm)")
    PlasmaEtch_rf_power                     = models.PositiveIntegerField(blank=False, default="100", verbose_name="RF power (Watts) *")
    PlasmaEtch_etch_time                    = models.PositiveIntegerField(blank=False, default="100", verbose_name="Etch time (sec) *")
    PlasmaEtch_etch_depth                   = models.PositiveIntegerField(blank=False, default="500", verbose_name="Etch depth (nm) *")
    PlasmaEtch_metrology_link               = models.CharField(max_length=400, blank=True, null=True, verbose_name="Metrology link")
    PlasmaEtch_notes                        = models.CharField(max_length=400, blank=True, null=True, verbose_name="Notes")
