from dataclasses import asdict
import json
from profiles.models import Profile
from .functions import handle_uploaded_experiment_file, handle_uploaded_publication_file, handle_uploaded_file, handle_bibtex
from django.shortcuts import render, redirect, get_object_or_404
from profiles.models import Profile
from .models import Samples, Publications
from .forms import ContactForm, InsertSampleForm, InsertPublicationForm, UploadFileForm
from .forms import ExperimentGeolocation, ExperimentMultipleSections, ExperimentIntro, ExperimentParameterInstrument
from .forms import ExperimentSpectra
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from xml_parser.xlm_parsers import generateXMLPublication, generateXMLSample, generateXMLExperiment
from django.http.response import JsonResponse



@login_required
def insert_sample(request):
    """ 
    A view to return the insert sample page 
    From input it constructs the dictionary needed for the xml parser
    """

    user_profile = get_object_or_404(Profile, user=request.user)

    # if not 'sample_added_fields' in request.session:
    #     request.session['sample_added_fields'] = []

    template = 'frontend/insert_sample.html'

    if request.method == 'GET':
        request.session['sample_added_fields'] = []
        session = request.session['sample_added_fields']
        form = InsertSampleForm(session=session)
    else:
        session = request.session['sample_added_fields']
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['sample_added_fields'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = InsertSampleForm(request.POST, session=session)
            if form.is_valid():
            
                input_dict = {}

                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)

                values = []
                for field in form:

                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)

                    if array[0] == "sample" and array[1] == "uid":
                        if not Samples.objects.get(sample_uid=array[2]):
                            Samples.objects.create(sample_uid=array[2])
                        else:
                            Samples.objects.get(sample_uid=array[2])
                    #if array[0] == "sample" and array[1] == "name":

                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]

                request.session['sample_added_fields'] = []
                session = []
                
                generateXMLSample("xml_sample.xml", input_dict)
                
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                return render(request, template, {'form': form})

    if 'uploaded_sample_data' in request.session:
        if request.session['uploaded_sample_data'] != None:
            uploaded_data = request.session['uploaded_sample_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None

    session_list = []
    for s in session:
        session_list.append(s)

    # user_profile = get_object_or_404(Profile, user=request.user)

    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        'profile': user_profile,
        'session_json': json.dumps(session_list),
    }

    return render(request, template, context)


@login_required
def insert_publication(request):
    """ 
    A view to return the insert experiment page 
    From input it constructs the dictionary needed for the xml parser
    """

    user_profile = get_object_or_404(Profile, user=request.user)

    # if not 'publication_added_fields' in request.session:
    #     request.session['publication_added_fields'] = []

    template = 'frontend/insert_publication.html'
    # session = request.session['publication_added_fields']

    if request.method == 'GET':
        request.session['publication_added_fields'] = []
        session = request.session['publication_added_fields']
        form = InsertPublicationForm(session=session)
    else:
        session = request.session['publication_added_fields']
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['publication_added_fields'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = InsertPublicationForm(request.POST, session=session)
            if form.is_valid():
                

                input_dict = {}

                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)

                values = []
                for field in form:
                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)
                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]

                request.session['publication_added_fields'] = []
                session = []

                generateXMLPublication("xml_publication.xml", input_dict)
                
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                return render(request, template, {'form': form})

    if 'uploaded_experiment_data' in request.session:
        if request.session['uploaded_experiment_data'] != None:
            uploaded_data = request.session['uploaded_experiment_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None
    
    session_list = []
    for s in session:
        session_list.append(s)

    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        'profile': user_profile,
        'session_json': json.dumps(session_list),
    }

    return render(request, template, context)


@login_required
def add_experiment_intro(request):
    
    user_profile = get_object_or_404(Profile, user=request.user)
    
    if not 'experiment_add_intro' in request.session:
        request.session['experiment_add_intro'] = []

    template = 'frontend/add_experiment_intro.html'
    session = request.session['experiment_add_intro']

    if request.method == 'GET':
        request.session['experiment_add_intro'] = []
        form = ExperimentIntro(session=session)
    else:
        session = request.session['experiment_add_intro']
        print(session)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['experiment_add_intro'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = ExperimentIntro(request.POST, session=session)
            if form.is_valid():
                
                # creates the dictionary
                input_dict = {}
                # creates an array of the keys to be used in dict
                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)
                # creates an array of arrays for the dict
                # each array includes parent_tag, name of tag, and content
                # if there is an autofill attribute, then autofill content will be used,
                # unless field has been altered by researcher
                values = []
                for field in form:
                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)
                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]
                request.session['posted_experiment_intro'] = input_dict
                request.session['experiment_add_intro'] = []
                session = []
                
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                return render(request, template, {'form': form})

    if 'uploaded_experiment_data' in request.session:
        if request.session['uploaded_experiment_data'] != None:
            uploaded_data = request.session['uploaded_experiment_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None
    
    session_list = []
    for s in session:
        session_list.append(s)

    # user_profile = get_object_or_404(Profile, user=request.user)

    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        'profile': user_profile,
        'session_json': json.dumps(session_list),
        # 'posted_session_json': json.dumps(posted_session)
    }

    return render(request, template, context)


@login_required
def add_experiment_geolocation(request):
    if not 'experiment_add_geolocation' in request.session:
        request.session['experiment_add_geolocation'] = []

    template = 'frontend/add_experiment_geolocation.html'
    session = request.session['experiment_add_geolocation']

    if request.method == 'GET':
        form = ExperimentGeolocation(session=session)
    else:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['experiment_add_geolocation'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = ExperimentGeolocation(request.POST, session=session)
            if form.is_valid():
                # creates the dictionary
                input_dict = {}
                # creates an array of the keys to be used in dict
                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)
                # creates an array of arrays for the dict
                # each array includes parent_tag, name of tag, and content
                # if there is an autofill attribute, then autofill content will be used,
                # unless field has been altered by researcher
                values = []
                for field in form:
                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)
                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]
                request.session['posted_experiment_geolocation'] = input_dict
                request.session['experiment_add_geolocation'] = []
                session = []
                
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                return render(request, template, {'form': form})

    if 'uploaded_experiment_data' in request.session:
        if request.session['uploaded_experiment_data'] != None:
            uploaded_data = request.session['uploaded_experiment_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None
    
    session_list = []
    for s in session:
        session_list.append(s)

    # user_profile = get_object_or_404(Profile, user=request.user)

    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        # 'profile': user_profile,
        'session_json': json.dumps(session_list),
    }

    return render(request, template, context)


@login_required
def add_experiment_parameters_instrument(request):
    if not 'experiment_add_parameters_instrument' in request.session:
        request.session['experiment_add_parameters_instrument'] = []

    template = 'frontend/add_experiment_parameters_instrument.html'
    session = request.session['experiment_add_parameters_instrument']

    if request.method == 'GET':
        form = ExperimentParameterInstrument(session=session)
    else:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['experiment_add_parameters_instrument'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = ExperimentParameterInstrument(request.POST, session=session)
            if form.is_valid():
                # creates the dictionary
                input_dict = {}
                # creates an array of the keys to be used in dict
                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)
                # creates an array of arrays for the dict
                # each array includes parent_tag, name of tag, and content
                # if there is an autofill attribute, then autofill content will be used,
                # unless field has been altered by researcher
                values = []
                for field in form:
                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)
                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]
                request.session['posted_experiment_parameters_instrument'] = input_dict
                request.session['experiment_add_parameters_instrument'] = []
                session = []
                
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                return render(request, template, {'form': form})

    if 'uploaded_experiment_data' in request.session:
        if request.session['uploaded_experiment_data'] != None:
            uploaded_data = request.session['uploaded_experiment_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None
    
    session_list = []
    for s in session:
        session_list.append(s)

    # user_profile = get_object_or_404(Profile, user=request.user)

    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        # 'profile': user_profile,
        'session_json': json.dumps(session_list),
    }

    return render(request, template, context)


@login_required
def add_experiment_multiple_sections(request):
    
    if not 'experiment_add_multiple' in request.session:
        request.session['experiment_add_multiple'] = []

    template = 'frontend/add_experiment_multiple_sections.html'
    session = request.session['experiment_add_multiple']

    if request.method == 'GET':
        form = ExperimentMultipleSections(session=session)
    else:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['experiment_add_multiple'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = ExperimentMultipleSections(request.POST, session=session)
            if form.is_valid():
                # creates the dictionary
                input_dict = {}
                # creates an array of the keys to be used in dict
                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)
                # creates an array of arrays for the dict
                # each array includes parent_tag, name of tag, and content
                # if there is an autofill attribute, then autofill content will be used,
                # unless field has been altered by researcher
                values = []
                for field in form:
                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)
                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]
                request.session['posted_experiment_multiple_sections'] = input_dict
                request.session['experiment_add_multiple'] = []
                session = []
                
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                return render(request, template, {'form': form})

    if 'uploaded_experiment_data' in request.session:
        if request.session['uploaded_experiment_data'] != None:
            uploaded_data = request.session['uploaded_experiment_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None
    
    session_list = []
    for s in session:
        session_list.append(s)

    # user_profile = get_object_or_404(Profile, user=request.user)

    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        # 'profile': user_profile,
        'session_json': json.dumps(session_list),
    }

    return render(request, template, context)


@login_required
def add_experiment_spectra(request):
    
    if not 'experiment_add_spectra' in request.session:
        request.session['experiment_add_spectra'] = []

    template = 'frontend/add_experiment_spectra.html'
    session = request.session['experiment_add_spectra']

    if request.method == 'GET':
        form = ExperimentSpectra(session=session)
    else:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = json.load(request)
            ajax_session = data.get('session')
            request.session['experiment_add_spectra'] = ajax_session
            return JsonResponse({'status': ajax_session})
        else:
            form = ExperimentSpectra(request.POST, session=session)
            if form.is_valid():
                # creates the dictionary
                input_dict = {}
                # creates an array of the keys to be used in dict
                keys = []
                for i in range(1, len(form.fields)+1):
                    keys.append(i)
                # creates an array of arrays for the dict
                # each array includes parent_tag, name of tag, and content
                # if there is an autofill attribute, then autofill content will be used,
                # unless field has been altered by researcher
                values = []
                for field in form:
                    array = []
                    array.append(field.name[0:field.name.index("_x")])
                    array.append(field.name[field.name.index("x_")+2:])

                    if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
                        array.append(field.field.widget.attrs['auto_fill'])
                    else:
                        array.append(form.cleaned_data[field.name])
                    values.append(array)
                # keys and values are inserted in dict
                for i in range(len(keys)):
                    input_dict[keys[i]] = values[i]

                request.session['posted_experiment_spectra'] = input_dict 
                request.session['experiment_add_spectra'] = []
                session = []
                               
                messages.success(request, 'Your data has been inserted!')

            else:
                messages.error(
                    request, "Please correct any errors")
                print(form.errors)
                return render(request, template, {'form': form})

    if 'uploaded_experiment_data' in request.session:
        if request.session['uploaded_experiment_data'] != None:
            uploaded_data = request.session['uploaded_experiment_data']
        else:
            uploaded_data = None
    else:
        uploaded_data = None
    
    session_list = []
    for s in session:
        session_list.append(s)

    # user_profile = get_object_or_404(Profile, user=request.user)
    samples = Samples.objects.all()
    context = {
        'uploaded_data': json.dumps(uploaded_data),
        'form': form,
        # 'profile': user_profile,
        'session_json': json.dumps(session_list),
        'samples': samples
    }

    return render(request, template, context)


@login_required
def add_experiment_finish(request):
    """
    View that displays all the sessions of inserted data
    If post then collects all into one dictionary and passes to parser function
    """
    # try to get the session or create empty dictionary
    sessions = [
        request.session.get('posted_experiment_intro', {}),
        request.session.get('posted_experiment_geolocation', {}),
        request.session.get('posted_experiment_parameters_instrument', {}),
        request.session.get('posted_experiment_multiple_sections', {}),
        request.session.get('posted_experiment_spectra', {})
    ]

    # calc full length of combined dictionary
    full_length = 0
    for session in sessions:
        full_length += len(session)

    keys = []
    for i in range(1, full_length+1):
        keys.append(i)

    values = []

    for session in sessions:
        if len(session) != 0:
            for key in session.keys():
                value = session[key]
                values.append(value)
    
    input_dict = {}
    for i in range(len(keys)):
        input_dict[keys[i]] = values[i]
    
    if request.method == 'POST':
        generateXMLExperiment("xml_experiment.xml", input_dict)
        messages.success(request, 'Your XML file has been created')

    template = 'frontend/add_exeriment_finish.html'

    context = {
        'experiment_intro': sessions[0],
        'experiment_geolocation': sessions[1],
        'experiment_parameters_instrument': sessions[2],
        'experiment_multiple_sections': sessions[3],
        'experiment_add_spectra': sessions[4],
        'input_dict': input_dict

    }

    return render(request, template, context)


@login_required
def delete_experiment_intro(request):

    if 'posted_experiment_intro' in request.session:
        request.session['posted_experiment_intro'] = []
    
    messages.info(request, 'Your data has been removed')

    return redirect('frontend:add_experiment_intro')


@login_required
def delete_experiment_geolocation(request):
    
    if 'posted_experiment_geolocation' in request.session:
        request.session['posted_experiment_geolocation'] = []
    
    messages.info(request, 'Your data has been removed')

    return redirect('frontend:add_experiment_geolocation')


@login_required
def delete_experiment_parameters_instrument(request):
    
    if 'posted_experiment_parameters_instrument' in request.session:
        request.session['posted_experiment_parameters_instrument'] = []
    
    messages.info(request, 'Your data has been removed')

    return redirect('frontend:add_parameters_instrument')


@login_required
def delete_experiment_multiple_sections(request):
    
    if 'posted_experiment_multiple_sections' in request.session:
        request.session['posted_experiment_multiple_sections'] = []
    
    messages.info(request, 'Your data has been removed')

    return redirect('frontend:add_experiment_multiple_sections')


@login_required
def delete_experiment_spectra(request):
    
    if 'posted_experiment_spectra' in request.session:
        request.session['posted_experiment_spectra'] = []
    
    messages.info(request, 'Your data has been removed')

    return redirect('frontend:add_experiment_spectra')

    
def index(request):
    """ A view to return the index page """

    return render(request, 'frontend/index.html')



# @login_required
# def insert_experiment(request):
#     """ 
#     A view to return the insert experiment page 
#     From input it constructs the dictionary needed for the xml parser
#     """
#     if not 'to_add' in request.session:
#         request.session['to_add'] = []
    
#     session = request.session['to_add']

#     if request.method == 'GET':
#         form = InsertExperimentForm(session=session)
#     else:
#         is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#         if is_ajax:
#             data = json.load(request)
#             ajax_session = data.get('session')
#             request.session['to_add'] = ajax_session
#             return JsonResponse({'status': ajax_session})
#         else:
#             session = request.session['to_add']
#             form = InsertExperimentForm(request.POST, session=session)
#             if form.is_valid():
#                 # creates the dictionary
#                 input_dict = {}
#                 # creates an array of the keys to be used in dict
#                 keys = []
#                 for i in range(1, len(form.fields)+1):
#                     keys.append(i)
#                 # creates an array of arrays for the dict
#                 # each array includes parent_tag, name of tag, and content
#                 # if there is an autofill attribute, then autofill content will be used,
#                 # unless field has been altered by researcher
#                 values = []
#                 for field in form:
#                     array = []
#                     array.append(field.name[0:field.name.index("_x")])
#                     array.append(field.name[field.name.index("x_")+2:])

#                     if 'auto_fill' in field.field.widget.attrs and len(form.cleaned_data[field.name]) == 0:
#                         array.append(field.field.widget.attrs['auto_fill'])
#                     else:
#                         array.append(form.cleaned_data[field.name])
#                     values.append(array)
#                 # keys and values are inserted in dict
#                 for i in range(len(keys)):
#                     input_dict[keys[i]] = values[i]

#                 request.session['to_add'] = []
#                 session = []
                
#                 messages.success(request, 'Your data has been inserted!')

#                 # function to generate XML sample is called, and files goes in django folder
#                 # generateXMLExperiment("xml_experiment.xml", input_dict)

#             else:
#                 messages.error(
#                     request, "Please correct any errors")
#                 return render(request, 'frontend/insert_experiment.html', {'form': form})

#     if 'uploaded_experiment_data' in request.session:
#         if request.session['uploaded_experiment_data'] != None:
#             uploaded_data = request.session['uploaded_experiment_data']
#         else:
#             uploaded_data = None
#     else:
#         uploaded_data = None
    
#     session_list = []
#     for s in session:
#         session_list.append(s)

#     # user_profile = get_object_or_404(Profile, user=request.user)

#     context = {
#         'uploaded_data': json.dumps(uploaded_data),
#         'form': form,
#         # 'profile': user_profile,
#         'session_json': json.dumps(session_list),
#     }

#     return render(request, 'frontend/insert_experiment.html', context)


def contact(request):
    """
    Contact view for submission of form
    """
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            body = {
                'message': form.cleaned_data['message'],
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email_address']
            }
            message = "\n".join(body.values())
            messages.success(request, 'Your message has been sent!')

            send_mail(
                "REAP",
                'Bonjour ' + form.cleaned_data['name'] +
                ', Merci de nous avoir contactés.' '\n\n'
                'Nous avons reçu ce message de votre part:\n\n"' +
                form.cleaned_data['message'] + '"\n\n'
                'Nous vous répondrons dans les plus brefs délais \n\n'
                'Cordialement,\nXXX',
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email_address'],
                 'salarystruggle@gmail.com'],
                fail_silently=False
            )

        else:
            messages.error(
                request, "Please correct any errors")
            return render(request, 'frontend/contact.html', {'form': form})

    form = ContactForm()

    return render(request, 'frontend/contact.html', {'form': form})


# @login_required
def upload_sample_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_data = handle_uploaded_file(request.FILES['file'])
            request.session['uploaded_sample_data'] = uploaded_data
            return redirect('frontend:insert_sample')
    else:
        form = UploadFileForm()

    context = {
        'form': form,
    }

    return render(request, 'frontend/upload_sample.html', context)

# @login_required
def upload_experiment_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_data = handle_uploaded_file(request.FILES['file'])
            request.session['uploaded_experiment_data'] = uploaded_data
            return redirect('frontend:insert_experiment')
    else:
        form = UploadFileForm()

    context = {
        'form': form,
    }

    return render(request, 'frontend/upload_experiment.html', context)


# @login_required
def upload_publication_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():

            if str(request.FILES['file'])[-3:] == "xml":
                uploaded_data = handle_uploaded_file(request.FILES['file'])
            elif str(request.FILES['file'])[-3:] == "bib":
                uploaded_data = handle_bibtex(request.FILES['file'])
            else:
                messages.warning(request, "File type not supported")
                return redirect('frontend:upload_publication')

            request.session['uploaded_publication_data'] = uploaded_data
            return redirect('frontend:insert_publication')
    else:
        form = UploadFileForm()

    context = {
        'form': form,
    }

    return render(request, 'frontend/upload_publication.html', context)


def clear_publication_data(request):
    """
    View that sets the sessions's upload_data to None
    """
    request.session['uploaded_publication_data'] = None
    messages.info(request, 'Your uploaded data has been removed')

    return redirect('frontend:insert_publication')


def clear_sample_data(request):
    """
    View that sets the sessions's upload_data to None
    """
    request.session['uploaded_sample_data'] = None
    messages.info(request, 'Your uploaded data has been removed')

    return redirect('frontend:insert_sample')


def clear_experiment_data(request):
    """
    View that sets the sessions's upload_data to None
    """
    request.session['uploaded_experiment_data'] = None
    messages.info(request, 'Your uploaded data has been removed')

    return redirect('frontend:insert_experiment')


def custom_page_not_found_view(request, exception):
    """
    View that renders 404 page
    """
    return render(request, "frontend/404.html", {})
