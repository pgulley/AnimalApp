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

def Index(request): #no context-dependant info on this page. 
    return render_to_response("index.html", context_instance=RequestContext(request))

def StudentList(request): #teacher only
    return render_to_response("studentlist.html",context_instance=RequestContext(request))

def AnimalList(request): #all animals for teachers, own only for students
    return render_to_response("animallist.html",context_instance=RequestContext(request))

def FormList(request): #displays all forms for teacher, own only for student
    return render_to_response("formlist.html", context_instance=RequestContext(request))

def FormDetail(request,form_id): #Shows all info for form, is editable if form date is today.
    return render_to_response("formdetail.html",context_instance=RequestContext(request))

def AnimalDetail(request,animal_id): #all information, most recent filled out form, form history
    return render_to_response("animaldetail.html",context_instance=RequestContext(request))

def NewAnimalForm(request):#Only once a day per student per animal, creates a new form for the animal based off of the template at time 0
    return render_to_response("formdetail.html",context_instance=RequestContext(request))

def StudentDetail(request,student_id): #Own only, unless teacher. 
    return render_to_response("studentdetail.html",context_instance=RequestContext(request))

def NewAnimal(request): #all thickened with Javasript and madness. will be a page to create all of the things associated with an animal:
    #SO new animal name, species
    return render_to_response("newanimal.html",context_instance=RequestContext(request))

def SubmitNewAnimal(request):
    return render_to_response("animaldetail.html",context_instance=RequestContext(request))
