from django.db import models
from django.contrib.auth.models import User
CATEGORY_CHOICES=(
("AM","Amphibian"),
("BI","Bird"),
("FI","Fish"),
("IN","Invertebrate"),
("MA","Mammal"),
("RE","Reptile"),
("RO","Rodent")
)


class Animal(models.Model):
    species = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    instructions = models.CharField(max_length=1000)
    caretakers = models.ManyToManyField("Profile", null=True, blank=True)
    formlist = models.ManyToManyField("FormDay", related_name="AniStat.FormDay", null=True, blank=True)
    def __unicode__(self):
        return "{0}: {1}".format(self.get_category_display(), self.name)
class FormCheck(models.Model):
    name = models.CharField(max_length=20)
    isdone = models.BooleanField()
    def __unicode__(self):
        return self.name
class Profile(models.Model):
    user=models.ForeignKey(User, unique=True)
    isstudent = models.BooleanField()
    isteacher = models.BooleanField()
    animals = models.ManyToManyField("Animal",null=True, blank=True)
    form = models.ManyToManyField("FormDay",null=True, blank=True)
    def __unicode__(self):
        return self.user.username+"'s profile"
class FormDay(models.Model):
    day = models.DateTimeField()
    formchecks = models.ManyToManyField("FormCheck")
    formobservation=models.CharField(max_length=1000, verbose_name="Observations")
    student = models.ForeignKey(User, related_name="AniStat.Profile")
    animal = models.ForeignKey(Animal,related_name="AniStat.Animal")
    def __unicode__(self):
        return "Form for {0} by {1} on {2}".format(self.animal.name, self.student.username, self.day)
