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

import re
import json
import os
import csv

from data_management.forms import ProfileForm, IVCurveForm, LoginForm, RegisterForm, ChipListSearchForm, AluminumEtchInputForm, AluminumEvaporationInputForm, ChipListForm, GlassDepositionInputForm, HFOxideEtchInputForm, PatterningInputForm, PlasmaCleanInputForm, PlasmaEtchInputForm
from data_management.models import Profile, SMU_capture, IVCurve, AluminumEtch, AluminumEvaporation, ChipList, GlassDeposition, HFOxideEtch, Patterning, PlasmaClean, PlasmaEtch
from data_management.forms import AluminumEtchSearchForm, AluminumEvaporationSearchForm, GlassDepositionSearchForm, HFOxideEtchSearchForm, PatterningSearchForm, PlasmaCleanSearchForm, PlasmaEtchSearchForm

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
        elif process == "HFOxideEtch":
            form = HFOxideEtchInputForm()
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
        elif process == "HFOxideEtch":
            form = HFOxideEtchSearchForm()
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
    elif process == "HFOxideEtch":
        p = get_object_or_404(HFOxideEtch, id=chip_id)
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
                AluminumEtch_time=request.POST['AluminumEtch_time'], 
                AluminumEtch_stir_rpm=request.POST['AluminumEtch_stir_rpm'], 
                AluminumEtch_metric_alum_etch_depth=request.POST['AluminumEtch_metric_alum_etch_depth'], 
                AluminumEtch_metric_photoresist_peeling=request.POST['AluminumEtch_metric_photoresist_peeling'], 
                AluminumEtch_metric_aluminum_peeling=request.POST['AluminumEtch_metric_aluminum_peeling'], 
                AluminumEtch_metrology_link=request.POST['AluminumEtch_metrology_link'], 
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
                AluminumEvaporation_time=request.POST['AluminumEvaporation_time'], 
                AluminumEvaporation_pressure_before_start_seq=request.POST['AluminumEvaporation_pressure_before_start_seq'], 
                AluminumEvaporation_pressure_before_evaporation=request.POST['AluminumEvaporation_pressure_before_evaporation'], 
                AluminumEvaporation_metric_layer_thickness=request.POST['AluminumEvaporation_metric_layer_thickness'], 
                AluminumEvaporation_metric_deposition_rate=request.POST['AluminumEvaporation_metric_deposition_rate'], 
                AluminumEvaporation_metrology_link=request.POST['AluminumEvaporation_metrology_link'], 
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
                GlassDeposition_bake_temp=request.POST['GlassDeposition_bake_temp'], 
                GlassDeposition_bake_time=request.POST['GlassDeposition_bake_time'], 
                GlassDeposition_amount_drops=request.POST['GlassDeposition_amount_drops'], 
                GlassDeposition_spin_rpm=request.POST['GlassDeposition_spin_rpm'], 
                GlassDeposition_spin_time=request.POST['GlassDeposition_spin_time'], 
                GlassDeposition_diffusion_temp=request.POST['GlassDeposition_diffusion_temp'], 
                GlassDeposition_diffusion_time=request.POST['GlassDeposition_diffusion_time'], 
                GlassDeposition_humidity=request.POST['GlassDeposition_humidity'], 
                GlassDeposition_metric_layer_thickness=request.POST['GlassDeposition_metric_layer_thickness'], 
                GlassDeposition_metric_cracking=request.POST['GlassDeposition_metric_cracking'], 
                GlassDeposition_metric_particles=request.POST['GlassDeposition_metric_particles'], 
                GlassDeposition_metrology_link=request.POST['GlassDeposition_metrology_link'], 
                GlassDeposition_notes=request.POST['GlassDeposition_notes'], 
                chip_owner=request.user, GlassDeposition_step_time=timezone.now()
            )
        if process == "HFOxideEtch":
            form = HFOxideEtchInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = HFOxideEtch(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                HFOxideEtch_max_temp_glass_reached=request.POST['HFOxideEtch_max_temp_glass_reached'], 
                HFOxideEtch_time=request.POST['HFOxideEtch_time'], 
                HFOxideEtch_temp=request.POST['HFOxideEtch_temp'], 
                HFOxideEtch_metric_oxide_etch_depth=request.POST['HFOxideEtch_metric_oxide_etch_depth'], 
                HFOxideEtch_metrology_link=request.POST['HFOxideEtch_metrology_link'], 
                HFOxideEtch_notes=request.POST['HFOxideEtch_notes'], 
                chip_owner=request.user, HFOxideEtch_step_time=timezone.now())
        if process == "Patterning":
            form = PatterningInputForm(request.POST, request.FILES)
            if not form.is_valid():
                return ["Invalid", form]
            new_model = Patterning(
                chip_number = ChipList.objects.get(chip_number=request.POST["chip_number"]),
                Patterning_underlying_material=request.POST['Patterning_underlying_material'], 
                Patterning_hdms_prebake_temp=request.POST['Patterning_hdms_prebake_temp'], 
                Patterning_hdms_prebake_time=request.POST['Patterning_hdms_prebake_time'], 
                Patterning_hdms_spin_rpm=request.POST['Patterning_hdms_spin_rpm'], 
                Patterning_hdms_spin_time=request.POST['Patterning_hdms_spin_time'], 
                Patterning_hdms_bake_temp=request.POST['Patterning_hdms_bake_temp'], 
                Patterning_hdms_bake_time=request.POST['Patterning_hdms_bake_time'], 
                Patterning_photoresist_spin_rpm=request.POST['Patterning_photoresist_spin_rpm'], 
                Patterning_photoresist_spin_time=request.POST['Patterning_photoresist_spin_time'], 
                Patterning_photoresist_bake_temp=request.POST['Patterning_photoresist_bake_temp'], 
                Patterning_photoresist_bake_time=request.POST['Patterning_photoresist_bake_time'], 
                Patterning_exposure_pattern=request.POST['Patterning_exposure_pattern'], 
                Patterning_exposure_time=request.POST['Patterning_exposure_time'], 
                Patterning_develop_time=request.POST['Patterning_develop_time'], 
                Patterning_metric_pattern_quality=request.POST['Patterning_metric_pattern_quality'], 
                Patterning_metric_leftover_photoresist=request.POST['Patterning_metric_leftover_photoresist'], 
                Patterning_metric_missing_photoresist=request.POST['Patterning_metric_missing_photoresist'], 
                Patterning_metric_contaminants=request.POST['Patterning_metric_contaminants'], 
                Patterning_metrology_link=request.POST['Patterning_metrology_link'], 
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
                PlasmaClean_clean_time=request.POST['PlasmaClean_clean_time'], 
                PlasmaClean_metric_contaminants=request.POST['PlasmaClean_metric_contaminants'], 
                PlasmaClean_metrology_link=request.POST['PlasmaClean_metrology_link'], 
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
                PlasmaEtch_etch_time=request.POST['PlasmaEtch_etch_time'], 
                PlasmaEtch_etch_depth=request.POST['PlasmaEtch_etch_depth'], 
                PlasmaEtch_metrology_link=request.POST['PlasmaEtch_metrology_link'], 
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
        if process == "HFOxideEtch":
            form = HFOxideEtchSearchForm(request.POST, request.FILES)
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

# create list of results for search queries
def filter_form(input_dict):
    q_list = []
    for proc in input_dict.keys():
        query = Q()
        for j in input_dict[proc]:
            query &= Q((j[0], j[1]))
        if proc == "ChipList":
            q_obj = (proc, ChipList.objects.filter(query).order_by('creation_time'))
        if proc == "AluminumEtch":
            q_obj = (proc, AluminumEtch.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        if proc == "AluminumEvaporation":
            q_obj = (proc, AluminumEvaporation.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        if proc == "GlassDeposition":
            q_obj = (proc, GlassDeposition.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        if proc == "HFOxideEtch":
            q_obj = (proc, HFOxideEtch.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        if proc == "Patterning":
            q_obj = (proc, Patterning.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        if proc == "PlasmaClean":
            q_obj = (proc, PlasmaClean.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        if proc == "PlasmaEtch":
            q_obj = (proc, PlasmaEtch.objects.filter(query).order_by('{0}_step_time'.format(proc)))
        q_list.append(q_obj)
    return q_list

# create csv and add values from query output to it
def create_csv(query_list):
    if not os.path.exists("csvfiles"):
        return 0, "Failed to generate CSV files: csvfiles directory does not exist."

    _, _, files = next(os.walk("csvfiles"))
    file_count = len(files)+1
    for i in query_list:
        queryset = i[1]
        with open(f'csvfiles/search{file_count}.csv', 'w') as file:
            write = csv.writer(file)
            write.writerows(queryset.values())
            write.writerows(queryset.values_list())
    return file_count, None

# create http response output for csv so people can click it to download
@login_required
def csv_output(request, csv_id):
    file = open(f'search{csv_id}.csv')
    response = HttpResponse(file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=webscraping_dataset.csv'
    return response
    
# start page, just displays  message now
@login_required
def start_page(request):
    context = {"message": "Welcome to the Hacker Fab Database"}
    return render(request, "home.html", context)

# get values from chip form to display but change soon
def display_chip(request, chip_id):
    context = {}
    context["chip_id"] = chip_id
    chip = get_object_or_404(ChipList, chip_number=chip_id)
    context["creation_time"] = chip.creation_time
    context["chip_owner"] = chip.chip_owner
    context["chip_number"] = chip.chip_number
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
    csv_link_id, err = create_csv(query_output)
    if err != None:
        # Raise an error if creating the csv fails
        messages.error(request, err)  # Add error message to messages framework
        context = {"message": err}
        return render(request, "search.html", context)
    array_of_dicts = []
    for i in query_output:
        for x in i[1].values():
            x["process"] = i[0]
            array_of_dicts.append(x)
    processes = get_processes()
    context = {"message": "Data Searched!","processes": processes,"link_id":csv_link_id,"output":array_of_dicts}
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
    return render(request, 'home.html', context)

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
