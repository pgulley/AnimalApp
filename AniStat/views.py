# Create your views here.
from AniStat.models import Animal, FormDay, FormCheck, Profile
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

def Index(request,message=False,error=False): #no context-dependant info on this page. 
    return render_to_response("index.html",{'error':error,
                                            'message':message,
                                           },context_instance=RequestContext(request))
@login_required
def StudentList(request): #teacher only
    if request.user.get_profile().isteacher:
        studentlist = []
        for profile in User.objects.all():
            if profile.get_profile().isstudent:
                studentlist.append(profile)
        return render_to_response("studentlist.html",{"studentlist":studentlist,
                                                     },context_instance=RequestContext(request))
    else:
        return Index(request,error="You don't have permission to view this page")

@login_required
def AnimalList(request, error=False): #all animals for teachers, own only for students. 
    if request.user.get_profile().isteacher:
        animallist=Animal.objects.all()
    else:
        animallist = request.user.get_profile().animals.all()
    return render_to_response("animallist.html",{"animallist":animallist,"error":error,
                                                },context_instance=RequestContext(request))
@login_required
def FormList(request,error=False): #displays all forms for teacher, own only for student
    if request.user.get_profile().isteacher:
        formlist=[]
        for form in FormDay.objects.all():
            if not form.istemplate:
                formlist.append(form) 
    else:
        formlist=request.user.get_profile().form.all() 
    return render_to_response("formlist.html",{"formlist":formlist,
                                               "error":error}, context_instance=RequestContext(request))
@login_required
def FormDetail(request,form_id): #Shows all info for form, is editable if form date is today.
    form = FormDay.objects.get(pk=form_id)
    if form.student == request.user:
        if form.day == datetime.date.today():
            return render_to_response("formdetail.html",{'form':form,
                                                        },context_instance=RequestContext(request))
        else:
            return render_to_response("formdetail.html",{"uneditable":True,
                                                         "form":form},context_instance=RequestContext(request))
    else:
        return FormList(request, error="You don't have permission to fill out this form")

@login_required
def AnimalDetail(request,animal_id): #all information, most recent filled out form, form history. teachers can add students here?
    animal = Animal.objects.get(pk=animal_id)
    formslist = animal.formlist.all()
    if formslist:
        for form in formslist:
            if form.day==datetime.date.today():
               firstform = form
    else: 
        firstform=False
    studentlist = User.objects.all()
    print animal.caretakers.all()
    #Question here: do students see all forms for the animal, or only their own? it makes a difference, here. will inquire.
    return render_to_response("animaldetail.html",{'animal':animal,"formone":firstform,'students':studentlist,
                                                  },context_instance=RequestContext(request))
@login_required
def ConnectAnimal(request,animal_id):
    try:
        students = request.POST['students']
    except KeyError:
        return AnimalDetail(request,animal_id)
    animal = Animal.objects.get(pk=animal_id)
    for student in students:
       student = User.objects.get(pk=student)
       student.get_profile().animals.add(animal)
       animal.caretakers.add(student.get_profile())
       student.get_profile().save()
    animal.save()
    return AnimalDetail(request,animal_id)

@login_required
def NewAnimalForm(request,animal_id):#Only once per day per student per animal, creates a new form for the animal based off of the template at time 0
    #search all FormDays for forms for this animal by this user created today. if it finds one, don't pass this view.
    allforms = FormDay.objects.all() 
    animal = Animal.objects.get(pk=animal_id)
    for form in allforms:
        if form.animal == animal:
            if form.student == request.user:
                if form.day == datetime.date.today():
                    return FormDetail(request,form.pk)
    for form in allforms:
        if form.istemplate:
            if form.animal == animal:
                templateform=form
    formchecklist = []
    for formcheck in templateform.formchecks.all():
        formchecklist.append(FormCheck(name=formcheck.name, isdone=False)) 
    today = datetime.date.today()
    newform = FormDay(day=today,istemplate=False,student=request.user,animal=templateform.animal)
    newform.save()
    for formcheck in formchecklist:
        formcheck.save()
        newform.formchecks.add(formcheck)
    newform.save()
    animal.formlist.add(newform)
    print animal.formlist
    print newform
    animal.save()
    request.user.get_profile().form.add(newform)
    request.user.get_profile().save()
    return render_to_response("formdetail.html",{'form':newform,
                                                },context_instance=RequestContext(request))

@login_required
def SubmitAnimalForm(request):
    form = FormDay.objects.get(pk=request.POST['formname'])
    for formcheck in form.formchecks.all():
        formname = formcheck.name
        if " " in formname:
            place = formname.find(" ")
            formname = formname[:place]
        try:
            A = request.POST[formname]
            formcheck.isdone=True
            print formcheck
        except KeyError:
            print 'error',formcheck
        formcheck.save()
    observation = request.POST['observation']
    form.formobservation = observation
    form.save()
    #Save all the form info in the request
    return Index(request,message="Your form has been submitted")

@login_required
def StudentDetail(request,student_id): #Own only, unless teacher.teacher can add animals here. 
    if request.user.get_profile().isteacher or request.user == User.objects.get(pk=student_id):
        student = User.objects.get(pk=student_id)
        return render_to_response("studentdetail.html",{"student":student,
                                                       },context_instance=RequestContext(request))
@login_required
def NewAnimal(request): #all thickened with Javasript and madness. will be a page to create all of the things associated with an animal:
    #SO new animal name, species, etc. not much has to happen in the view though. I think just user validation.
    return render_to_response("newanimal.html",context_instance=RequestContext(request))

@login_required
def SubmitNewAnimal(request):#Where most of the magic of this app occurs: all of the connections between forms, formchecks and animals have to be made here
    species = request.POST['species']
    name = request.POST['name']
    category = request.POST['category']
    animal = Animal(species=species,name=name,category=category)
    animal.save()
    formchecklist = []
    numberofformchecks = request.POST['formnumber']
    for X in range(0,int(numberofformchecks)+1):
        formcheck = FormCheck(name=request.POST["formcheck{0}".format(X)])
        formcheck.save()
        formchecklist.append(formcheck)
    print formchecklist
    form = FormDay(day=datetime.date(year=1,month=1,day=1),animal=animal,istemplate=True)
    form.save()
    for formcheck in formchecklist:
        form.formchecks.add(formcheck)
    form.save()
    return AnimalDetail(request,animal.pk)

##Auth pages

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Index(request, message="you are now logged in")
    else:
        return Index(request, error="Invalid Login")

def Logout(request): 
    logout(request)
    return Index(request)

def NewUser(request): 
    return render_to_response("newuser.html", context_instance=RequestContext(request))

def CreateUser(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username=username,password=password,email=email)
    newprofile = Profile(isstudent=True, isteacher=False, user=user)
    newprofile.save()
    return Index(request)
