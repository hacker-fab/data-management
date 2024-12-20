from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.forms.models import model_to_dict
import re
import json
import os
import csv

from data_management.forms import ProfileForm, IVCurveForm, LoginForm, RegisterForm, ChipListSearchForm, AluminumEtchInputForm, AluminumEvaporationInputForm, ChipListForm, GlassDepositionInputForm, DiffusionInputForm, HFOxideEtchInputForm, KOHEtchInputForm, NickelPlatingInputForm, PatterningInputForm, PlasmaCleanInputForm, PlasmaEtchInputForm
from data_management.models import Profile, SMU_capture, IVCurve, AluminumEtch, AluminumEvaporation, ChipList, GlassDeposition, Diffusion, HFOxideEtch, KOHEtch, NickelPlating, Patterning, PlasmaClean, PlasmaEtch
from data_management.forms import AluminumEtchSearchForm, AluminumEvaporationSearchForm, GlassDepositionSearchForm, DiffusionSearchForm, HFOxideEtchSearchForm, KOHEtchSearchForm, NickelPlatingSearchForm, PatterningSearchForm, PlasmaCleanSearchForm, PlasmaEtchSearchForm

# gets a list of all processes from json file
def get_processes():
    processes = []
    with open('headers.json') as json_file:
        json_dict = json.load(json_file)
    for key in json_dict:
        process = {"id": f'{key}', "name": f'{key}'}
        processes.append(process)
    return processes

# creates forms for each process that info needs to be inputted for
def get_input_meas(processes):
    forms = []
    for process in processes:
        if process == "AluminumEtch":
            form = AluminumEtchInputForm()
        elif process == "AluminumEvaporation":
            form = AluminumEvaporationInputForm()
        elif process == "GlassDeposition":
            form = GlassDepositionInputForm()
        elif process == "Diffusion":
            form = DiffusionInputForm()
        elif process == "HFOxideEtch":
            form = HFOxideEtchInputForm()
        elif process == "KOHEtch":
            form = KOHEtchInputForm()
        elif process == "NickelPlating":
            form = NickelPlatingInputForm()
        elif process == "Patterning":
            form = PatterningInputForm()
        elif process == "PlasmaClean":
            form = PlasmaCleanInputForm()
        elif process == "PlasmaEtch":
            form = PlasmaEtchInputForm()
        else:
            continue
        f = {"name": f'{process}', "form": form}
        forms.append(f)
    return forms

# creates forms for each process that info needs to be used to search
def get_search_meas(processes):
    processes = processes.split(",")
    forms = []
    for process in processes:
        if process == "AluminumEtch":
            form = AluminumEtchSearchForm()
        elif process == "AluminumEvaporation":
            form = AluminumEvaporationSearchForm()
        elif process == "GlassDeposition":
            form = GlassDepositionSearchForm()
        elif process == "Diffusion":
            form = DiffusionSearchForm()
        elif process == "HFOxideEtch":
            form = HFOxideEtchSearchForm()
        elif process == "KOHEtch":
            form = KOHEtchSearchForm()
        elif process == "NickelPlating":
            form = NickelPlatingSearchForm()
        elif process == "Patterning":
            form = PatterningSearchForm()
        elif process == "PlasmaClean":
            form = PlasmaCleanSearchForm()
        elif process == "PlasmaEtch":
            form = PlasmaEtchSearchForm()
        elif process == "ChipList":
            form = ChipListSearchForm()
        else:
            continue
        f = {"name": f'{process}', "form": form}
        forms.append(f)
    return forms

# return http response of pictures
@login_required
def get_photo(request, chip_id, process):
    if process == "Patterning":
        p = get_object_or_404(Patterning, id=chip_id)
    elif process == "AluminumEtch":
        p = get_object_or_404(AluminumEtch, id=chip_id)
    elif process == "AluminumEvaporation":
        p = get_object_or_404(AluminumEvaporation, id=chip_id)
    elif process == "GlassDeposition":
        p = get_object_or_404(GlassDeposition, id=chip_id)
    elif process == "Diffusion":
        p = get_object_or_404(Diffusion, id=chip_id)
    elif process == "HFOxideEtch":
        p = get_object_or_404(HFOxideEtch, id=chip_id)
    elif process == "KOHEtch":
        p = get_object_or_404(KOHEtch, id=chip_id)
    elif process == "NickelPlating":
        p = get_object_or_404(NickelPlating, id=chip_id)
    elif process == "PlasmaClean":
        p = get_object_or_404(PlasmaClean, id=chip_id)
    elif process == "PlasmaEtch":
        p = get_object_or_404(PlasmaEtch, id=chip_id)
    elif process == "Profile":
        p = get_object_or_404(Profile, id=chip_id)
    # someone could have delete the picture leaving the DB with a bad references.
    if not p.picture:
        raise Http404
    return HttpResponse(p.picture, content_type=p.content_type)

# for all inputs, save the process information as a model
def save_form(processes, request):
    timezone.activate("US/Eastern")
    for process in processes:
        if process == "AluminumEtch":
            form = AluminumEtchInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = AluminumEtch(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                AluminumEtch_temp=request.POST['AluminumEtch_temp'], 
                AluminumEtch_duration=request.POST['AluminumEtch_duration'], 
                AluminumEtch_stir_rpm=request.POST['AluminumEtch_stir_rpm'], 
                AluminumEtch_metric_alum_etch_depth=request.POST['AluminumEtch_metric_alum_etch_depth'], 
                AluminumEtch_metric_photoresist_peeling=request.POST['AluminumEtch_metric_photoresist_peeling'], 
                AluminumEtch_metric_aluminum_peeling=request.POST['AluminumEtch_metric_aluminum_peeling'], 
                AluminumEtch_notes=request.POST['AluminumEtch_notes'], 
                chip_owner=request.user, AluminumEtch_step_time=timezone.now()
            )
        if process == "AluminumEvaporation":
            form = AluminumEvaporationInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = AluminumEvaporation(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                AluminumEvaporation_temp=request.POST['AluminumEvaporation_temp'], 
                AluminumEvaporation_duration=request.POST['AluminumEvaporation_duration'], 
                AluminumEvaporation_pressure_before_start_seq=request.POST['AluminumEvaporation_pressure_before_start_seq'], 
                AluminumEvaporation_pressure_before_evaporation=request.POST['AluminumEvaporation_pressure_before_evaporation'], 
                AluminumEvaporation_metric_layer_thickness=request.POST['AluminumEvaporation_metric_layer_thickness'], 
                AluminumEvaporation_metric_deposition_rate=request.POST['AluminumEvaporation_metric_deposition_rate'], 
                AluminumEvaporation_notes=request.POST['AluminumEvaporation_notes'], 
                chip_owner=request.user, AluminumEvaporation_step_time=timezone.now()
            )
        if process == "GlassDeposition":
            form = GlassDepositionInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = GlassDeposition(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                GlassDeposition_glass_type=request.POST['GlassDeposition_glass_type'],
                GlassDeposition_cleaning_step=request.POST['GlassDeposition_cleaning_step'], 
                GlassDeposition_days_glass_at_room_temp=request.POST['GlassDeposition_days_glass_at_room_temp'], 
                GlassDeposition_prebake_temp=request.POST['GlassDeposition_prebake_temp'], 
                GlassDeposition_prebake_duration=request.POST['GlassDeposition_prebake_duration'], 
                GlassDeposition_bake_temp=request.POST['GlassDeposition_bake_temp'], 
                GlassDeposition_bake_duration=request.POST['GlassDeposition_bake_duration'], 
                GlassDeposition_amount_drops=request.POST['GlassDeposition_amount_drops'], 
                GlassDeposition_spin_rpm=request.POST['GlassDeposition_spin_rpm'], 
                GlassDeposition_spin_duration=request.POST['GlassDeposition_spin_duration'], 
                GlassDeposition_humidity=request.POST['GlassDeposition_humidity'], 
                GlassDeposition_metric_layer_thickness=request.POST['GlassDeposition_metric_layer_thickness'], 
                GlassDeposition_metric_cracking=request.POST['GlassDeposition_metric_cracking'], 
                GlassDeposition_metric_particles=request.POST['GlassDeposition_metric_particles'], 
                GlassDeposition_notes=request.POST['GlassDeposition_notes'], 
                chip_owner=request.user, GlassDeposition_step_time=timezone.now()
            )
        if process == "Diffusion":
            form = DiffusionInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = Diffusion(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                Diffusion_temp=request.POST['Diffusion_temp'], 
                Diffusion_duration=request.POST['Diffusion_duration'], 
                Diffusion_notes=request.POST['Diffusion_notes'], 
                chip_owner=request.user, Diffusion_step_time=timezone.now()
            )
        if process == "HFOxideEtch":
            form = HFOxideEtchInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = HFOxideEtch(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                HFOxideEtch_duration=request.POST['HFOxideEtch_duration'], 
                HFOxideEtch_temp=request.POST['HFOxideEtch_temp'], 
                HFOxideEtch_metric_oxide_etch_depth=request.POST['HFOxideEtch_metric_oxide_etch_depth'], 
                HFOxideEtch_notes=request.POST['HFOxideEtch_notes'], 
                chip_owner=request.user, HFOxideEtch_step_time=timezone.now()
            )
        if process == "KOHEtch":
            form = KOHEtchInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = KOHEtch(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                KOHEtch_concentration=request.POST['KOHEtch_concentration'], 
                KOHEtch_temp=request.POST['KOHEtch_temp'], 
                KOHEtch_duration=request.POST['KOHEtch_duration'], 
                KOHEtch_rpm=request.POST['KOHEtch_rpm'], 
                KOHEtch_notes=request.POST['KOHEtch_notes'], 
                chip_owner=request.user, KOHEtch_step_time=timezone.now()
            )
        if process == "NickelPlating":
            form = NickelPlatingInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = NickelPlating(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                NickelPlating_solution=request.POST['NickelPlating_solution'], 
                NickelPlating_temp=request.POST['NickelPlating_temp'], 
                NickelPlating_duration=request.POST['NickelPlating_duration'], 
                NickelPlating_sensitizer=request.POST['NickelPlating_sensitizer'], 
                NickelPlating_activator=request.POST['NickelPlating_activator'], 
                NickelPlating_surfactant=request.POST['NickelPlating_surfactant'], 
                NickelPlating_notes=request.POST['NickelPlating_notes'], 
                chip_owner=request.user, NickelPlating_step_time=timezone.now()
            )
        if process == "Patterning":
            form = PatterningInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = Patterning(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                Patterning_underlying_material=request.POST['Patterning_underlying_material'], 
                Patterning_hdms_prebake_temp=request.POST['Patterning_hdms_prebake_temp'], 
                Patterning_hdms_prebake_duration=request.POST['Patterning_hdms_prebake_duration'], 
                Patterning_hdms_spin_rpm=request.POST['Patterning_hdms_spin_rpm'], 
                Patterning_hdms_spin_duration=request.POST['Patterning_hdms_spin_duration'], 
                Patterning_hdms_bake_temp=request.POST['Patterning_hdms_bake_temp'], 
                Patterning_hdms_bake_duration=request.POST['Patterning_hdms_bake_duration'], 
                Patterning_photoresist_spin_rpm=request.POST['Patterning_photoresist_spin_rpm'], 
                Patterning_photoresist_spin_duration=request.POST['Patterning_photoresist_spin_duration'], 
                Patterning_photoresist_bake_temp=request.POST['Patterning_photoresist_bake_temp'], 
                Patterning_photoresist_bake_duration=request.POST['Patterning_photoresist_bake_duration'], 
                Patterning_exposure_duration=request.POST['Patterning_exposure_duration'], 
                Patterning_develop_duration=request.POST['Patterning_develop_duration'], 
                Patterning_metric_pattern_quality=request.POST['Patterning_metric_pattern_quality'], 
                Patterning_metric_development=request.POST['Patterning_metric_development'], 
                Patterning_metric_contaminants=request.POST['Patterning_metric_contaminants'], 
                Patterning_notes=request.POST['Patterning_notes'], 
                chip_owner=request.user, Patterning_step_time=timezone.now()
            )
        if process == "PlasmaClean":
            form = PlasmaCleanInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = PlasmaClean(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                PlasmaClean_o2_flow=request.POST['PlasmaClean_o2_flow'], 
                PlasmaClean_rf_power=request.POST['PlasmaClean_rf_power'], 
                PlasmaClean_clean_duration=request.POST['PlasmaClean_clean_duration'], 
                PlasmaClean_metric_contaminants=request.POST['PlasmaClean_metric_contaminants'], 
                PlasmaClean_notes=request.POST['PlasmaClean_notes'], 
                chip_owner=request.user, PlasmaClean_step_time=timezone.now()
            )
        if process == "PlasmaEtch":
            form = PlasmaEtchInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = PlasmaEtch(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                PlasmaEtch_o2_flow=request.POST['PlasmaEtch_o2_flow'], 
                PlasmaEtch_sf6_flow=request.POST['PlasmaEtch_sf6_flow'], 
                PlasmaEtch_rf_power=request.POST['PlasmaEtch_rf_power'], 
                PlasmaEtch_etch_duration=request.POST['PlasmaEtch_etch_duration'], 
                PlasmaEtch_etch_depth=request.POST['PlasmaEtch_etch_depth'], 
                PlasmaEtch_notes=request.POST['PlasmaEtch_notes'], 
                chip_owner=request.user, PlasmaEtch_step_time=timezone.now()
            )
        new_model.save()
        if form.cleaned_data['picture'] != None:
            new_model.picture = form.cleaned_data['picture']
            new_model.content_type = form.cleaned_data['picture'].content_type
        new_model.save()
    return "Done"

# extract key value pairs from search forms in http POST 
def parse_forms(used_processes, request):
    invalid_form = False
    forms = []
    filters = {}
    used_processes = used_processes.split(",")
    for process in used_processes:
        process = re.sub("[^A-Za-z]","",process)
        if process == "ChipList":
            form = ChipListSearchForm(request.POST, request.FILES)
        if process == "AluminumEtch":
            form = AluminumEtchSearchForm(request.POST, request.FILES)
        if process == "AluminumEvaporation":
            form = AluminumEvaporationSearchForm(request.POST, request.FILES)
        if process == "GlassDeposition":
            form = GlassDepositionSearchForm(request.POST, request.FILES)
        if process == "Diffusion":
            form = DiffusionSearchForm(request.POST, request.FILES)
        if process == "HFOxideEtch":
            form = HFOxideEtchSearchForm(request.POST, request.FILES)
        if process == "KOHEtch":
            form = KOHEtchSearchForm(request.POST, request.FILES)
        if process == "NickelPlating":
            form = NickelPlatingSearchForm(request.POST, request.FILES)
        if process == "Patterning":
            form = PatterningSearchForm(request.POST, request.FILES)
        if process == "PlasmaClean":
            form = PlasmaCleanSearchForm(request.POST, request.FILES)
        if process == "PlasmaEtch":
            form = PlasmaEtchSearchForm(request.POST, request.FILES)
        if not form.is_valid():
            invalid_form = True
        forms.append(form)
        cleaned_data = form.cleaned_data
        filters[process] = []
        for key, value in cleaned_data.items():
            if value != None:
                filters[process].append((key, value))
    if invalid_form:
        return ["Invalid", forms]
    return [filters]

# Helper function to format range searches based on the input search form parameters
def format_range_filters(unformatted_filters):
    result = []
    max_fields = {key: value for key, value in unformatted_filters if key.endswith('_max')}
    base_fields = {key: value for key, value in unformatted_filters if not key.endswith('_max')}
    
    # Process _max fields and their corresponding base fields
    for key, value in max_fields.items():
        base_key = key[:-4]  # Remove the '_max' suffix to get the base key
        if base_key in base_fields:
            result.append((base_key, (base_fields[base_key], value)))  # Pair base with max
            del base_fields[base_key]  # Remove the used base field
        else:
            result.append((base_key, value))  # Add the max field as a regular field
    
    # Add remaining base fields (those without corresponding _max) to the result
    for key, value in base_fields.items():
        result.append((key, value))
    
    return result

# create list of results for search queries (append "pattern" column)
# returns an array of array dictionaries of the search queries
def filter_form(input_dict):
    """
    return:
    [
        { process_name_1: [{dictionary_representing_col_value_pairs_of_this_entry}, {dictionary_representing_col_value_pairs_of_this_entry}, ...]
        },
        { process_name_2: [{dictionary_representing_col_value_pairs_of_this_entry}, {dictionary_representing_col_value_pairs_of_this_entry}, ...]
        },
        ...
    ]
    """
    q_list = []
    for proc in input_dict.keys():
        if len(input_dict[proc]) == 0:
            # Retrieve all results with this process type
            if proc == "ChipList":
                queryset = ChipList.objects.all().order_by('-creation_time')
            elif proc == "AluminumEtch":
                queryset = AluminumEtch.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "AluminumEvaporation":
                queryset = AluminumEvaporation.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "GlassDeposition":
                queryset = GlassDeposition.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "Diffusion":
                queryset = Diffusion.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "HFOxideEtch":
                queryset = HFOxideEtch.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "Patterning":
                queryset = Patterning.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "PlasmaClean":
                queryset = PlasmaClean.objects.all().order_by(f'-{proc}_step_time')
            elif proc == "PlasmaEtch":
                queryset = PlasmaEtch.objects.all().order_by(f'-{proc}_step_time')

        else:
            query = Q()
            print("input_dict")
            print(input_dict)
            filter_list = format_range_filters(input_dict[proc])
            print("filter_list")
            print(filter_list)
            # filter_list = input_dict[proc]
            for j in filter_list:
                print("j")
                print(j)
                if isinstance(j[1], tuple):
                    # Handle search by range queries
                    # search_param_range is a tuple (min_val, max_val)
                    search_param_range = (j[1][0], j[1][1])
                    search_param = j[0]
                    query &= Q(**{f"{search_param}__range": search_param_range})
                else:
                    query &= Q((j[0], j[1]))

            if proc == "ChipList":
                queryset = ChipList.objects.filter(query).order_by('-creation_time')
            elif proc == "AluminumEtch":
                queryset = AluminumEtch.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "AluminumEvaporation":
                queryset = AluminumEvaporation.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "GlassDeposition":
                queryset = GlassDeposition.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "Diffusion":
                queryset = Diffusion.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "HFOxideEtch":
                queryset = HFOxideEtch.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "Patterning":
                queryset = Patterning.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "PlasmaClean":
                queryset = PlasmaClean.objects.filter(query).order_by(f'-{proc}_step_time')
            elif proc == "PlasmaEtch":
                queryset = PlasmaEtch.objects.filter(query).order_by(f'-{proc}_step_time')

        q_list.append((proc, queryset))
    return q_list

# create csv and add values from query output to it
def create_csv(query_list):
    if not os.path.exists("csvfiles"):
        try:
            # Create the 'csvfiles' directory
            os.makedirs("csvfiles")
        except Exception as e:
            return 0, f"Failed to generate CSV files: {str(e)}"

    _, _, files = next(os.walk("csvfiles"))
    file_count = len(files)+1
    for i in query_list:
        queryset = i[1]
        with open(f'csvfiles/search{file_count}.csv', 'w') as file:
            write = csv.writer(file)
            write.writerows(queryset.values())
            write.writerows(queryset.values_list())
    return file_count, None

# Create a CSV file from an array of arrays of dictionaries
# Data is grouped by process
def create_csv_include_process(array_of_array_of_dicts):
    if not os.path.exists("csvfiles"):
        try:
            # Create the 'csvfiles' directory
            os.makedirs("csvfiles")
        except Exception as e:
            return 0, f"Failed to generate CSV files: {str(e)}"

    _, _, files = next(os.walk("csvfiles"))
    file_count = len(files)+1

    try:
        with open(f'csvfiles/search{file_count}.csv', 'w') as file:

            last_process = None
            for array_of_process_entries in array_of_array_of_dicts:
                if len(array_of_process_entries) > 0:
                    writer = csv.DictWriter(file, fieldnames=array_of_process_entries[0].keys())
                    file.write('\n')
                    writer.writeheader()
                    for row in array_of_process_entries:
                        if last_process == None:
                            last_process = row["process"]
                        elif last_process != row["process"]:
                            last_process = row["process"]
                            file.write('\n')
                            writer = csv.DictWriter(file, fieldnames=row.keys())
                            writer.writeheader()
                        writer.writerow(row)

                    # Add a blank line between tables for clarity

    except Exception as e:
        return 0, f"Failed to write to CSV: {e}"

    return file_count, None


# Handles searching and downloading CSV from the search page
@login_required
def csv_output(request, csv_id):
    action = request.POST.get('action')
    if action == 'download_csv':
        # Prepare and return CSV response
        return download_csv(request, csv_id)
    else:
        return sort_search_output(request, csv_id)


# create http response output for csv so people can click it to download
@login_required
def download_csv(request, csv_id):
    # Create a CSV response with content type for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="webscraping_dataset.csv"'
    writer = csv.writer(response)
    
    selected_row_nums = request.POST.getlist('selected_items')
    selected_row_nums = list(map(int, selected_row_nums))
    num_selected_rows = len(selected_row_nums)

    # Open the source CSV file for reading and a temporary CSV file for writing
    with open(f'csvfiles/search{csv_id}.csv', mode='r') as data_src:
        reader = csv.reader(data_src)

        # write the headers
        headers = next(reader)
        writer.writerow(headers)

        # Find the index of the necessary columns to get the photo url
        chip_id_col_index = headers.index("id") if "id" in headers else -1
        process_col_index = headers.index("process") if "process" in headers else -1
        picture_col_index = headers.index("picture") if "picture" in headers else -1
        
        # Keep track of rows and skip any duplicate headers
        for i, row in enumerate(reader):
            # Skip data that hasn't been selected
            if num_selected_rows > 0 and i not in selected_row_nums:
                continue

            if not row:  # A newline indicates that the next line is going to be headers
                chip_id_col_index = -1
                process_col_index = -1
                picture_col_index = -1
                writer.writerow('\n')
                continue
            
            if "id" in row:
                chip_id_col_index = row.index("id")
            if "picture" in row:
                picture_col_index = row.index("picture")
            if "process" in row:
                process_col_index = row.index("process")
                
            # Generate the photo URL
            if picture_col_index != -1 and row[picture_col_index] != "picture" and row[picture_col_index] != "":
                try:
                    photo_url = reverse('photo', args=[row[process_col_index], row[chip_id_col_index]])
                    row[picture_col_index] = request.build_absolute_uri(photo_url)  # Add the full URL
                except Exception as e:
                    print(f"Failed to get photo url: {e}")

            writer.writerow(row)
        
    return response


# Sort the results of a search query based on process type or chip id
@login_required
def sort_search_output(request, csv_id):
    sort_by = request.POST.get('sort_by', 'process')  # Default to 'process' if not set

    print(f"SORTING BY: {sort_by}")
    sorted_data = {}

    with open(f'csvfiles/search{csv_id}.csv', mode='r') as data_src:
        reader = csv.reader(data_src)  # General CSV reader to process rows
        current_headers = None  # Keep track of headers for each table
        
        for row in reader:
            # Skip empty rows (which separate different tables in the CSV files)
            if not row:
                current_headers = None
                continue  

            # Process the header row (only for the first row of each table)
            if current_headers is None:
                current_headers = row  # Set the headers for the first table
                continue  # Skip adding the header row itself to the data

            # Create a dictionary for the row using the current headers
            row_dict = {current_headers[i]: row[i] for i in range(len(row))}
            # Group the data based on the selected field ('process' or 'id')
            # For some reason the chip number column is named 'chip_number' for the chiplist and named 
            # 'chip_number_id' for the processes, which is jank, which is why we have to do this:
            key = row_dict.get(sort_by, None)
            if key is None and sort_by == "chip_number_id":
                key = row_dict.get("chip_number")
                if key is None:
                    context = {"message": "Failed to sort by chip_id. Missing parameter chip_number_id or chip_number"}
                    return render(request, "search.html", context)

            if sort_by == "process":
                if key not in sorted_data:
                    sorted_data[key] = []
                sorted_data[key].append(row_dict)
            else:
                if key not in sorted_data:
                    sorted_data[key] = {}
                process = row_dict.get("process")
                if process not in sorted_data[key]:
                    sorted_data[key][process] = []
                sorted_data[key][process].append(row_dict)

    # Save the sorted results to a csv
    array_of_array_of_dicts_sorted = []
    if sort_by == "process":
        array_of_array_of_dicts_sorted = list(sorted_data.values())
    else:
        for chip_num in sorted_data.keys():
            array_of_array_of_dicts_sorted.extend(list(sorted_data[chip_num].values()))

    csv_link_id, err = create_csv_include_process(array_of_array_of_dicts_sorted)  
    if err != None:
        # Raise an error if creating the csv fails
        messages.error(request, err)  # Add error message to messages framework
        context = {"message": err}
        return render(request, "search.html", context)
    
    # Render the page with the sorted data
    processes = get_processes()
    context = {"message": "Data Searched!","processes": processes,"link_id":csv_link_id,"output":array_of_array_of_dicts_sorted}
    return render(request, "search.html", context)
    
    
# start page, just displays  message now
@login_required
def start_page(request):
    context = {"message": "Welcome to the Hacker Fab Database"}
    return render(request, "home.html", context)

# Page that displays information about a given chip_id
# Lists all the processes that have been recorded for this chip
def display_chip(request, chip_id):
    processes = get_processes()
    chip_id_filter = {}
    for p in processes:
        if "name" in p:
            process_name = p["name"]
        else:
            process_name = p["id"]
        # Don't display ChipList because it's technically not a process. 
        # It's just a summary of this chip's information.
        if process_name == "ChipList":
            continue
        chip_id_filter[process_name] = [('chip_number', chip_id)]
            
    query_results = filter_form(chip_id_filter)

    # Processes that have been recorded for this chip_id
    process_entries = remove_bad_query_results(query_results)
    context = {}
    context["chip_id"] = chip_id
    chip = get_object_or_404(ChipList, chip_number=chip_id)
    context["creation_time"] = chip.creation_time
    context["chip_owner"] = chip.chip_owner
    context["chip_number"] = chip.chip_number
    context["starting_material"] = chip.starting_material
    context["notes"] = chip.notes
    context["process_entries"] = process_entries
    # Figure out if any processes have been recorded for this chip
    has_processes = False
    for p in process_entries:
        if len(p) > 0:
            has_processes = True
            break
    context["has_processes"] = has_processes

    if request.method == 'GET':
        return render(request, "chipnum.html", context)

# chip page possibly change soon
@login_required
def chip_page(request):
    timezone.activate("US/Eastern")
    context = {}
    if request.method == 'GET':
        return render(request, "chip.html", context)
    context["chip_acquired"] = "yes"
    try:
        chip = ChipList.objects.get(chip_number=request.POST["chip_number"]) 
    except:
        chip = ChipList(chip_number=request.POST["chip_number"], creation_time=timezone.now(), chip_owner=request.user)
        chip.save()
    status = request.POST["status"]
    if status == "Initial":
        context['creation_time'] = chip.creation_time
        context['chip_owner'] = chip.chip_owner
        context['chip_number'] = chip.chip_number
        context['IVCurrents_CSV'] = ChipListForm(initial={'IVCurrents_CSV': chip.IVCurrents_CSV})
        context['IVVoltages_CSV'] = ChipListForm(initial={'IVVoltages_CSV': chip.IVVoltages_CSV})
        context['form'] = ChipListForm(initial={'notes': chip.notes})
        return render(request, 'chip.html', context)
    form = ChipListForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'chip.html', context)
    chip.notes = form.cleaned_data['notes']
    chip.IVCurrents_CSV = form.cleaned_data['IVCurrents_CSV']
    chip.IVVoltages_CSV = form.cleaned_data['IVVoltages_CSV']
    chip.save()
    context['creation_time'] = chip.creation_time
    context['chip_owner'] = chip.chip_owner
    context['chip_number'] = chip.chip_number
    context['IVCurrents_CSV'] = chip.IVCurrents_CSV
    context['IVVoltages_CSV'] = chip.IVVoltages_CSV
    context['form'] = ChipListForm(initial={'notes': chip.notes})
    return render(request, "chip.html", context)

# show profile page of person logged in, allow people to change stuff with form
@login_required
def mypfp_action(request):
    chips = ChipList.objects.all().filter(chip_owner = request.user).order_by('-creation_time')
    profile = Profile.objects.get(id=request.user.id) 
    context = {"chips": chips , "profile": profile}

    if request.method == 'GET': #if get request, just show form
        context['form'] = ProfileForm(initial={'text': profile.text})
        return render(request, 'myprofile.html', context)
    
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'myprofile.html', context)
        
    if form.cleaned_data['picture'] != None:
        profile.picture = form.cleaned_data['picture']
        profile.content_type = form.cleaned_data['picture'].content_type
    profile.text = form.cleaned_data['text']
    profile.save()

    # Handle password change
    password_form = PasswordChangeForm(request.user, request.POST)
    if password_form.is_valid():
        user = password_form.save()  # This changes the password
        update_session_auth_hash(request, user)  # Important! Keep the user logged in
        messages.success(request, 'Your password was successfully updated!')
    else:
        # Add password form errors to context to display in template
        messages.error(request, 'Please correct the error below.')
        for field, errors in password_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")

    # Refresh forms in context
    context['form'] = ProfileForm(initial={'text': profile.text})
    context['password_form'] = PasswordChangeForm(user=request.user)  # Reset password form
    return render(request, 'myprofile.html', context)

# view other people's profiles
@login_required
def otherpfp_action(request, user_id): #request is us, user_id is profile to view
    user = get_object_or_404(User, id=user_id)
    chips = ChipList.objects.all().filter(chip_owner = user).order_by('-creation_time')
    context = {"chips": chips}
    context['profile'] = Profile.objects.get(id=user_id)
    context['loggedin'] = Profile.objects.get(id=request.user.id)
    return render(request, 'otherprofile.html', context)


# NOTE: see issue #61 on GitHub for why the below lines are like this
def remove_bad_query_results(query_output):
    array_of_array_of_dicts = []
    for i in query_output:
        j = 0
        j_max = i[1].count()
        array_of_dicts = []
        while True:
            if j >= j_max:
                break
            try: 
                entry = model_to_dict(i[1][j])
                entry["process"] = i[0]
                array_of_dicts.append(entry)
                j+=1
            except Exception as e:
                # Ignore entries that have faulty formatting (raises err: argument must be int or float)
                j+=1
                continue
        array_of_array_of_dicts.append(array_of_dicts)
    return array_of_array_of_dicts

# display page to handle searches
@login_required
def search_page(request):
    if request.method == 'GET':
        processes = get_processes()
        context = {"message": "Search Data here", "processes": processes}
        return render(request, "search.html", context)
    status = request.POST["status"] #hidden field
    if status == "Initial": #after search processes clicked
        processes = get_processes()
        rel_processes = process_search(request.POST)
        measurements = get_search_meas(rel_processes)
        if not measurements:
            processes = get_processes()
            context = {"message": "Search Data here", "processes": processes}
            return render(request, "search.html", context)
        context = {"message": "Search Data here", "processes": processes, "forms": measurements, "used_process": rel_processes}
        return render(request, "search.html", context)
    used_processes = request.POST['used_process'] #after search values inputted
    parsed = parse_forms(used_processes, request)
    if parsed[0] == "Invalid":
        processes = get_processes()
        context = {"message": "Invalid Data Input", "processes": processes, "forms": parsed[1], "used_process": used_processes}
        return render(request, "search.html", context)

    query_output = filter_form(parsed[0])

    # NOTE: see issue #61 on GitHub for why the below lines are like this
    array_of_array_of_dicts = remove_bad_query_results(query_output)

    csv_link_id, err = create_csv_include_process(array_of_array_of_dicts)  
    if err != None:
        print(f"\nerr:{err}\n")
        # Raise an error if creating the csv fails
        messages.error(request, err)  # Add error message to messages framework
        context = {"message": err}
        return render(request, "search.html", context)
    processes = get_processes()
    context = {"message": "Data Searched!","processes": processes,"link_id":csv_link_id,"output":array_of_array_of_dicts}
    return render(request, "search.html", context)

# display page for input
@login_required
def input_page(request):
    if request.method == 'GET':
        processes = get_processes()
        processes.remove({'id': 'ChipList', 'name': 'ChipList'})
        context = {"message": "Input Data here","processes": processes}
        return render(request, "input.html", context)
    status = request.POST["status"] #hidden field
    if status == "Initial": #if process to input is clicked
        new_process = request.POST["Process"]
        measurements = get_input_meas([new_process])
        if not measurements:
            processes = get_processes()
            processes.remove({'id': 'ChipList', 'name': 'ChipList'})
            context = {"message": "Input Data here","processes": processes}
            return render(request, "input.html", context)
        processes = get_processes()
        context = {"processes": processes, "forms": measurements, "used_process": new_process}
        return render(request, "input.html", context)
    process = request.POST["used_process"] #after input measurements
    saved = save_form([process], request)
    if saved[0] == "Invalid":
        context = {"message": "Invalid Data Input", "processes": processes, "forms": [saved[1]], "used_process": process}
        return render(request, "input.html", context)
    all_entries = ChipList.objects.all().order_by('-creation_time')
    context = {"message": "Data Submitted!","all_entries": all_entries}
    return render(request, "central.html", context)

# go through search processes and parse into list
def process_search(request):
    rel_processes = ""
    for key, value in request.lists():
        if key != "status" and key != "csrfmiddlewaretoken":
            k = key[1:]
            if " " in k:
                k = k.split(" ")[0] + k.split(" ")[1]
            rel_processes += k + ','
    rel_processes = rel_processes[:-1]
    return rel_processes

#login page
def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
   
    login(request, new_user) #built in django function
    context = {"message": "Succesful Login! Welcome to the Hacker Fab Database"}
    return redirect(reverse('home'))

# page with list of all chips and data
def central_action(request):
    all_entries = ChipList.objects.all().order_by('-creation_time')
    context = {"all_entries": all_entries}
    return render(request, 'central.html', context)

# logout page
@login_required
def logout_action(request):
    logout(request) #built in django function
    return redirect(reverse('login'))

# register page
def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    
    new_profile = Profile(user=new_user)
    new_profile.save()

    context['Name'] = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
    login(request, new_user)
    context = {"message": "Succesful Registration! Welcome to the Hacker Fab Database"}
    return render(request, "home.html", context)
