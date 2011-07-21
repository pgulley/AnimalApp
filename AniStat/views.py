# Create your views here.
from AniStat.models import Animal, FormDay, FormCheck, Profile
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
import copy

# Index X
#     CurrentForm
#     PastFormIndex
#
# Teacher 
#   StudentIndex X
#     StudentDetail (Displays forms from this student, plus any other info)
#   FormIndex (Displays All forms) X
#   AnimalIndex (Displays ALL forms for this animal plus any other info) X
#

#So  basically the teacher can do anything the student can do, but without viewing restrictions (can see ALL forms for an animal and ALL animals)
# in addition to that, a index of all the students, then an index of all forms, independant of student or animal
# Also an easy form generation interface- whenever an animal is created, a template form (time 0:0:0:0) will be created, with default values. must be edited and added to from the admin interface. 
#
# STILL MISSING:
#  Form submission
#  Student-Animal link submission (it is two way, but could be done through just one view

def Index(request,error=False): #no context-dependant info on this page. 
    return render_to_response("index.html",{'error':error,
                                           },context_instance=RequestContext(request))

def StudentList(request): #teacher only
    if request.user.get_profile.isteacher:
        studentlist = []
        for profile in User.objects.all():
            if User.get_profile.isstudent:
                studentlist.append(profile)
        return render_to_response("studentlist.html",{"studentlist":studentlist,
                                                     },context_instance=RequestContext(request))
    else:
        return Index(request,error="You don't have permission to view this page")

def AnimalList(request): #all animals for teachers, own only for students. 
    if request.user.get_profile.isteacher:
        animallist=Animal.objects.all()
    else:
        animallist=[]
        for animal in Animal.objects.all():
            if request.user in animal.caretakers:
                animallist.append(animal)
 
    return render_to_response("animallist.html",{"animallist":animallist,
                                                },context_instance=RequestContext(request))

def FormList(request,error=False): #displays all forms for teacher, own only for student
    if request.user.get_profile.isteacher:
        formlist=FormDay.objects.all()
    else:
        formlist=request.user.get_profile.forms.all() 
    return render_to_response("formlist.html",{"formlist":formlist,
                                               "error":error}, context_instance=RequestContext(request))

def FormDetail(request,form_id): #Shows all info for form, is editable if form date is today.
    form = FormDay.objects.get(pk=form_id)
    if form.student == request.user:
        if form.day.date() == datetime.date.today():
            return render_to_response("formdetail.html",{'form':form,
                                                        },context_instance=RequestContext(request))
        else:
            return FormList(request,error="You can't edit past forms")
    else:
        return FormList(request, error="You don't have permission to fill out this form")

def AnimalDetail(request,animal_id): #all information, most recent filled out form, form history. teachers can add students here?
    animal = Animal.objects.get(pk=animal_id)
    #Question here: do students see all forms for the animal, or only their own? it makes a difference, here. will inquire.
    return render_to_response("animaldetail.html",context_instance=RequestContext(request))

def NewAnimalForm(request,animal_id):#Only once a day per student per animal, creates a new form for the animal based off of the template at time 0
    #search all FormDays for forms for this animal by this user created today. if it finds one, don't pass this view.
    return render_to_response("formdetail.html",context_instance=RequestContext(request))

def StudentDetail(request,student_id): #Own only, unless teacher. teacher can add animals here. 
    if request.user.get_profile.isteacher:
        student = User.objects.get(pk=student_id)
        return render_to_response("studentdetail.html",{"student":student,
                                                       }context_instance=RequestContext(request))

def NewAnimal(request): #all thickened with Javasript and madness. will be a page to create all of the things associated with an animal:
    #SO new animal name, species, etc. not much has to happen in the view though. I think just user validation.
    return render_to_response("newanimal.html",context_instance=RequestContext(request))

def SubmitNewAnimal(request):#Where most of the magic of this app occurs: all of the connections between forms, formchecks and animals have to be made here
    return render_to_response("animaldetail.html",context_instance=RequestContext(request))
