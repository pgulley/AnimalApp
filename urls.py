from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^index$','AniStat.views.Index'),
     url(r'^students$','AniStat.views.StudentList'),
     url(r'^students/(?P<student_id>\d+)/$','AniStat.views.StudentDetail'),
     url(r'^forms$','AniStat.views.FormList'),
     url(r'^forms/(?P<form_id>\d+)/$','AniStat.views.FormDetail'),
     url(r'^animals$','AniStat.views.AnimalList'),
     url(r'^animals/(?P<animal_id>\d+)/$','AniStat.views.AnimalDetail'),
     url(r'^newanimal$','AniStat.views.NewAnimal'),
     url(r'^newanimal/submit$','AniStat.views.SubmitNewAnimal'),
     url(r'^animals/(?P<animal_id>\d+)/newform$','AniStat.views.NewAnimalForm'),
     url(r'submit','AniStat.views.SubmitAnimalForm'),
    # Examples:
    # url(r'^$', 'AnimalApp.views.home', name='home'),
    # url(r'^AnimalApp/', include('AnimalApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
