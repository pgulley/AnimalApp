# Create your views here.
from AniStat.models import Animal, FormDay, FormCheck, Profile
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
import copy

# Index
#     CurrentForm
#     PastFormIndex
#
# Teacher
#   StudentIndex 
#     StudentDetail (Displays forms from this student, plus any other info)
#   FormIndex (Displays All forms)
#   AnimalIndex (Displays ALL forms for this animal plus any other info)
#

#So  basically the teacher can do anything the student can do, but without viewing restrictions (can see ALL forms for an animal and ALL animals)
# in addition to that, a index of all the students, then an index of all forms, independant of student or animal
# Also an easy form generation interface- whenever an animal is created, a template form (time 0:0:0:0) will be created, with default values. must be edited and added to from the admin interface. 

def Index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))
