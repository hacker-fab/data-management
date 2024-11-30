# Generated by Django 3.2.25 on 2024-11-30 16:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_management', '0003_auto_20241130_1606'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GlassDeposition_P504',
            new_name='GlassDeposition',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_amount_drops',
            new_name='GlassDeposition_amount_drops',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_bake_duration',
            new_name='GlassDeposition_bake_duration',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_bake_temp',
            new_name='GlassDeposition_bake_temp',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_cleaning_step',
            new_name='GlassDeposition_cleaning_step',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_days_glass_at_room_temp',
            new_name='GlassDeposition_days_glass_at_room_temp',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_humidity',
            new_name='GlassDeposition_humidity',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_metric_cracking',
            new_name='GlassDeposition_metric_cracking',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_metric_layer_thickness',
            new_name='GlassDeposition_metric_layer_thickness',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_metric_particles',
            new_name='GlassDeposition_metric_particles',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_notes',
            new_name='GlassDeposition_notes',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_prebake_duration',
            new_name='GlassDeposition_prebake_duration',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_prebake_temp',
            new_name='GlassDeposition_prebake_temp',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_spin_duration',
            new_name='GlassDeposition_spin_duration',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_spin_rpm',
            new_name='GlassDeposition_spin_rpm',
        ),
        migrations.RenameField(
            model_name='glassdeposition',
            old_name='GlassDeposition_P504_step_time',
            new_name='GlassDeposition_step_time',
        ),
    ]
