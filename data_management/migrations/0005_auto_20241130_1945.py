# Generated by Django 3.2.25 on 2024-11-30 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_management', '0004_auto_20241130_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='glassdeposition',
            name='GlassDeposition_glass_type',
            field=models.CharField(blank=True, choices=[('P504', 'P504'), ('700B', '700B')], max_length=400, null=True, verbose_name='Glass type *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Etch duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_metric_alum_etch_depth',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Etch depth (nm) *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_metric_aluminum_peeling',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=400, null=True, verbose_name='Aluminum peeling? *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_metric_photoresist_peeling',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=400, null=True, verbose_name='PR peeling? *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_stir_rpm',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Stir speed (rpm) *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='AluminumEtch_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Etch temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='aluminumetch',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Evaporation duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_metric_deposition_rate',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Deposition rate (Å/sec) *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_metric_layer_thick_qcm',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Layer thickness by QCM (Å) *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_metric_layer_thickness',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Layer thickness by profilometer (Å) *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_pressure_before_evaporation',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Pressure before evaporation (torr E-6) *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_pressure_before_start_seq',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Pressure before start (torr E-6) *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='AluminumEvaporation_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='aluminumevaporation',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_amount_drops',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Number of drops *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_bake_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Bake duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_bake_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Bake temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_cleaning_step',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Cleaning step *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_metric_cracking',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=400, null=True, verbose_name='Cracking? *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_metric_particles',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=400, null=True, verbose_name='Particles? *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_prebake_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Prebake duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_prebake_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Prebake temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_spin_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Spin duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_spin_rpm',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Spin speed (rpm) *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='GlassDeposition_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='glassdeposition',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hfoxideetch',
            name='HFOxideEtch_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Etch duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='hfoxideetch',
            name='HFOxideEtch_metric_oxide_etch_depth',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Etch depth (nm) *'),
        ),
        migrations.AlterField(
            model_name='hfoxideetch',
            name='HFOxideEtch_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='hfoxideetch',
            name='HFOxideEtch_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Etch temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='hfoxideetch',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='hfoxideetch',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_cleaning_step',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Cleaning step *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_develop_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Develop duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_exposure_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Exposure duration (ms) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_exposure_pattern',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Exposure pattern *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_hdms_bake_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='HMDS bake duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_hdms_bake_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='HMDS bake temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_hdms_prebake_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='HMDS prebake duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_hdms_prebake_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='HMDS prebake temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_hdms_spin_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='HMDS spin duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_hdms_spin_rpm',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='HMDS spin speed (rpm) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_metric_contaminants',
            field=models.CharField(blank=True, choices=[('1', '1 (Little to none)'), ('2', '2'), ('3', '3 (Significant amounts)')], max_length=400, null=True, verbose_name='Level of contamination *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_metric_development',
            field=models.CharField(blank=True, choices=[('Well-developed', 'Well-developed'), ('Underdeveloped', 'Underdeveloped'), ('Overdeveloped', 'Overdeveloped')], max_length=400, null=True, verbose_name='Development quality *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_metric_pattern_quality',
            field=models.CharField(blank=True, choices=[('1', '1 (Worst)'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 (Best)')], max_length=400, null=True, verbose_name='Pattern quality *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_photoresist_bake_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='PR bake duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_photoresist_bake_temp',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='PR bake temp (°C) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_photoresist_spin_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='PR spin duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_photoresist_spin_rpm',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='PR spin speed (rpm) *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='Patterning_underlying_material',
            field=models.CharField(blank=True, choices=[('PolySilicon', 'PolySi'), ('P504', 'Spin-on Glass (P504)'), ('700B', 'Spin-on Glass (700B)'), ('Aluminum', 'Aluminum')], max_length=400, null=True, verbose_name='Underlying material *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='patterning',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='plasmaclean',
            name='PlasmaClean_clean_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Clean duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='plasmaclean',
            name='PlasmaClean_o2_flow',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='O2 flow (sccm) *'),
        ),
        migrations.AlterField(
            model_name='plasmaclean',
            name='PlasmaClean_rf_power',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='RF power (Watts) *'),
        ),
        migrations.AlterField(
            model_name='plasmaclean',
            name='PlasmaClean_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='plasmaclean',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='plasmaclean',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='PlasmaEtch_etch_depth',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Etch depth (nm) *'),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='PlasmaEtch_etch_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Etch duration (sec) *'),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='PlasmaEtch_rf_power',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='RF power (Watts) *'),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='PlasmaEtch_sf6_flow',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='SF6 flow (sccm)'),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='PlasmaEtch_step_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='chip_number',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.chiplist', verbose_name='Chip number *'),
        ),
        migrations.AlterField(
            model_name='plasmaetch',
            name='chip_owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]